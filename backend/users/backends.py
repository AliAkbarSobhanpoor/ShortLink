from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from users.models import User
from django.utils import timezone

class PhoneOrEmailAuthBackend(BaseBackend):
    # this is only for authenticate not user creation.
    
    def authenticate(self, request, username=None, password=None, otp_code=None, **kwargs):
        try:
            if not username:
                return None

            user:User = User.objects.get(
                Q(phone_number=username) | Q(email=username)
            )
            
            if not user.is_active:
                    return None
                                
            # password part
            if password and user.check_password(password):
                return user

            if otp_code and user.verification_code == otp_code and user.verification_expiry > timezone.now():
                user.verification_code= None
                user.verification_expiry= None
                user.save(update_fields=["verification_code", "verification_expiry"])
                return user
            
            
            
            return None
        
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            