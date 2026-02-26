from rest_framework.generics import CreateAPIView
from .serializers import RegisterPhoenNumberSerializer, RegisterEmailSerializer, ActiveEmailSerializer, ActivePhoneNumberSerializer
from .models import User

class RegisterUserStepOne(CreateAPIView):
    queryset = User.objects.none()
    def get_serializer_class(self):
        if "email" in self.request.data:
            return RegisterEmailSerializer
        elif "phone_number" in self.request.data:
            return RegisterPhoenNumberSerializer
        
        return RegisterEmailSerializer
    
    
class RegisterUserStepTwo(CreateAPIView):
    queryset = User.objects.none()
    def get_serializer_class(self):
        if "email" in self.request.data:
            return ActiveEmailSerializer
        elif "phone_number" in self.request.data:
            return ActivePhoneNumberSerializer
        
        return ActiveEmailSerializer
    