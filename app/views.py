from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action,permission_classes,api_view,authentication_classes

from .models import App,Customer,AppCustomer
from .serializers import AppsSerializer,CustomerSerializer,UserRegistrationSerializer
from .permissions import AppPermission
from .utils import upload_to_s3

from django.contrib.auth import login

from rest_framework import permissions

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication



class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            print(request.data)
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            print(user)
            login(request,user)
            response=super(LoginView, self).post(request, format=None)  
            if response.status_code>=400:
                return Response({
                    "Message":"Invalid Credentials"},status=401
                )
            return response
        except Exception as e:
            return Response({
                "message":e.__str__()
            },status=401)
    
    
@api_view(http_method_names=['POST'])
@permission_classes([permissions.AllowAny,])
def register(request):
    try:
        print(request.data)
        serializer=UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                    "message":"User Registered successsfully",
                },status=201)
    except Exception as e:
        return Response({
            "message":e.__str__()
        },status=400)


class AppViewSet(ModelViewSet):
    authentication_classes=[TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated,AppPermission]
    queryset=App.objects.all()
    serializer_class=AppsSerializer

    def perform_create(self, serializer):
        # Extract the uploaded image file
        image_file = self.request.data.get('image')
        # Check if an image file was provided
        if image_file:
            foldername='app_images'
            # Upload the image to S3
            s3_url = upload_to_s3(foldername,image_file)
            # Save the object with the S3 URL
            serializer.save(app_image=s3_url)
            
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)
    

class CustomerViewSet(ModelViewSet):
    authentication_classes=[TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated,]
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
            
    def perform_update(self, serializer):
        # Extract the uploaded image file
        image_file = self.request.data.get('image')
        # Check if an image file was provided
        if image_file:
            foldername='user_images'
            # Upload the image to S3
            s3_url = upload_to_s3(foldername,image_file)
            # Save the object with the S3 URL
            serializer.save(user_image=s3_url)
        serializer.save()
            
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(username=self.request.user)
        instance = queryset.first()  # Select the first instance from the queryset
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['get'])
    def apps(self, request):
        user = Customer.objects.get(username=request.user)
        user_app = AppCustomer.objects.filter(user=user.id)
        data = [{"id":app.app.id,"AppName":app.app.app_name,"Points":app.app.points} for app in user_app]
        return Response(data, status=200)
    
    @action(detail=False, methods=['get'])
    def points(self, request):
        user = Customer.objects.get(username=request.user)
        return Response({
            "points_earned": user.points_earned,
            "username": user.username
        }, status=200)
    
    @action(detail=False, methods=['get'])
    def tasks(self, request):
        user = Customer.objects.get(username=request.user)
        return Response({
            "tasks_completed": user.tasks_completed,
            "username": user.username
        }, status=200)
        
        
@api_view(http_method_names=['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((TokenAuthentication,))     
def task(request):
    try:
        user = Customer.objects.get(username=request.user)
        app_id = request.data.get("app")
        image = request.data['image']
        foldername = 'screenshots'
        app = App.objects.get(pk=app_id)

        # Check if the combination of user and app already exists in AppCustomer
        app_customer_exists = AppCustomer.objects.filter(user=user, app=app).exists()

        if not app_customer_exists:
            # Update user points and tasks
            user.points_earned += app.points
            user.tasks_completed += 1
            user.save()

            # Upload to S3 after the check
            url = upload_to_s3(foldername, image)

            # Create a new AppCustomer instance
            AppCustomer.objects.create(user=user, app=app, screenshot=url)

            return Response({
                "Message": "Task Completed",
                "screenshot": url
            }, status=200)
        else:
            return Response({
                "message": "User and App combination already exists"
            }, status=400)

    except Exception as e:
        return Response({
            "message": e.__str__()
        }, status=400)
