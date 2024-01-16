from rest_framework import serializers

from .models import App,Customer
from .utils import upload_to_s3 

class AppsSerializer(serializers.ModelSerializer):
    class Meta:
        model=App
        exclude=['created_at',"updated_at",]
        
    def update(self, instance, validated_data):
        points = validated_data.get('points')
        if points is not None:
            instance.points = points
            instance.save(update_fields=['points'])
            return instance
        else:
            raise serializers.ValidationError("Invalid or missing 'points' field in the request data.")
        
    
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id','username', 'email', 'gender', 'date_of_birth', 'points_earned', 'tasks_completed', 'is_admin', 'first_name', 'last_name', 'user_image')
        extra_kwargs = {'password': {'write_only': True}}

            
class UserRegistrationSerializer(CustomerSerializer):
    class Meta(CustomerSerializer.Meta):
        fields = ['username', 'email', 'password', 'is_admin']
            
    def create(self, validated_data):
        customer = Customer.objects.create_user(**validated_data)
        return customer