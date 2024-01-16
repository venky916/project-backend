from  rest_framework.permissions import BasePermission
from .models import Customer

class AppPermission(BasePermission):
    
    def has_permission(self, request, view):
        user=Customer.objects.get_by_natural_key(username=request.user.username)
        if request.method not in ['GET']:
            return user.is_admin
        return True