from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import App, AppCustomer, Customer

# @receiver(post_save, sender=App)
# def update_user_points(sender, instance, **kwargs):
#     """
#     Signal handler to update user points when an App is saved.
#     """
#     print(kwargs['update_fields'])
#     if kwargs.get('update_fields') and 'points' in kwargs['update_fields']:
#         print("called")
#         app_customers = AppCustomer.objects.filter(app=instance)
#         for app_customer in app_customers:
#             user = app_customer.user
#             before=user.points_earned
#             after=instance.points
#             x=before-after
#             if(x>0):
#                 user.points_earned -= x
#             else:
#                 user.points_earned -= x
#             user.save()

@receiver(pre_save, sender=App)
def get_old_points(sender, instance, **kwargs):
    """
    Signal handler to get the old points value before an App is saved.
    """
    if instance.pk:
        # If the instance has a primary key, it means it already exists in the database
        instance._old_points = App.objects.get(pk=instance.pk).points
    else:
        # If it's a new instance, set old points to 0
        instance._old_points = 0

@receiver(post_save, sender=App)
def update_user_points(sender, instance, **kwargs):
    """
    Signal handler to update user points when an App is saved.
    """
    # Check if 'points' is in the updated fields
    if kwargs.get('update_fields') and 'points' in kwargs['update_fields']:
        app_customers = AppCustomer.objects.filter(app=instance)
        for app_customer in app_customers:
            user = app_customer.user
            # Subtract the old points
            user.points_earned -= instance._old_points
            # Add the new points
            user.points_earned += instance.points
            user.save()