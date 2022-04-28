from wsgiref.validate import validator
from Parking.models import Bill, Car, Parking, Profile, Ticket,Payment
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

# ModelSerializer automatically generates validators for the serializer based on the model
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(
        write_only = True,
        required = True,
        style = {'input_type':'password'}
        )
    
    class Meta:
        model = User
        fields = ('username','email','password',)

    def create(self, validated_data):
        # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# class UserRegistrationSerailizer(serializers.Serializer):
#     username = serializers.CharField(max_length = 20, required = True)
#     email = serializers.EmailField(validators = [UniqueValidator(queryset = User.objects.all())])
#     password = serializers.CharField(
#         write_only = True,
#         required = True,
#         style = {'input_type': 'password'}
#     )
#     password2 = serializers.CharField(
#         required = True
#     )

#     def validate(self,data):
#         if not data.get('password') or not data.get('password2'):
#             raise serializers.ValidationError("Please enter password.")
#         elif data.get('password') != data.get('password2'):
#             raise serializers.ValidationError("Password does not match.")
#         return data

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Profile
        fields = "__all__"

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('slot_number', 'occupied',)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    # ticket = TicketSerializer(many = True, read_only = True)

    # ticket = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = Car
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bill
        fields = ['exit_time','total_bill','ticket']

class PaymentSerializer(serializers.ModelSerializer):
    bill = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Payment
        fields = ['bill','total_payment','status']
