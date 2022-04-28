from functools import partial
from multiprocessing import context
from urllib import request
from .serializers import BillSerializer, ParkingSerializer, ProfileSerializer,UserSerializer,RegisterSerializer,CarSerializer,TicketSerializer,PaymentSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import *
from datetime import datetime, timedelta

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import filters
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

# Create your views here.

# APIView is a base class. It doesn't assume much and will allow you to plug pretty much anything to it.
#  GenericAPIView is meant to work with Django's Models. 
# checked
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            # AuthToken.objects.create() return tuple of 2 values(model_instance, token)
            token= AuthToken.objects.create(user)[1]

            return Response({
                # get_serializer_context provides extra content to serializer class
                'user': UserSerializer(user, context = self.get_serializer_context()).data,
                'token': token,
                'status': status.HTTP_201_CREATED
            })
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)

# checked but couldnt login
# class UserRegistration(generics.GenericAPIView):
#     serializer_class = UserRegistrationSerailizer

#     def post(self,request,*args,**kwargs):
#         serializer = self.serializer_class(data = request.data)
#         if serializer.is_valid(raise_exception = True):
#             model_serializer = UserSerializer(data = serializer.data)
#             if model_serializer.is_valid(raise_exception = True):
#                 user = model_serializer.save()
#                 token = AuthToken.objects.create(user)[1]
#                 return Response({
#                     'user': UserSerializer(user, context = self.get_serializer_context()).data,
#                     'token': token,
#                     'status': status.HTTP_201_CREATED
#                 })
#         return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request,format = None):
        serializer = AuthTokenSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # also creates session based authentication with token based authentication
            login(request, user)
            return super(LoginAPI, self).post(request, format = None)
        else:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message': "Provided username does not exist"
            })

# checked
class ViewProfile(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = ProfileSerializer
    def get(self, request):
        queryset = Profile.objects.get(user = self.request.user)
        serializer = ProfileSerializer(queryset)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })

class UpdateProfile(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

# the difference between put and patch is that, in put request all the attribute defined in model(except model's attribute that has default
# value) otherwise it won't get updated while in patch request(partial = True) makes the difference i.e, we can change only one attribute or all attributes of model
    serializer_class = ProfileSerializer
    def put(self, request):
        try:
            queryset = Profile.objects.get(user = self.request.user)
            serializer = ProfileSerializer(queryset, data = request.data)
            if serializer.is_valid(raise_exception =  True):
                serializer.save()
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                })
        except queryset.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND
            })

    def patch(self,request):
        try:
            queryset = Profile.objects.get(user = self.request.user)
            serializer = ProfileSerializer(queryset, data = request.data,partial = True)
            if serializer.is_valid(raise_exception =  True):
                serializer.save()
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                })
        except queryset.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND
        })

class UpdateUser(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserSerializer

    def patch(self,request,id):
        try:
            queryset = User.objects.get(id = id)
            serializer = UserSerializer(queryset, data = request.data, partial = True)
            if serializer.is_valid(raise_exception = True):
                serializer.save()
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                })
        except queryset.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })

# checked
class ParkingView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
    serializer_class = ParkingSerializer

    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':status.HTTP_200_OK,
                'data':serializer.data,
                'message':"Success"
            })
        return Response({
            'message':"Invalid data"
        })

    def get(self,request):
        queryset = Parking.objects.filter(occupied = False).order_by('slot_number')
        total_space = Parking.objects.all().count()
        parked_space = Parking.objects.filter(occupied = True).order_by('slot_number')
        if queryset.exists():
            serializer = self.serializer_class(queryset, many = True)
            return Response({
                'status':status.HTTP_200_OK,
                'total_space': total_space,
                'empty-space': queryset.count(),
                'parked-space': parked_space,
                'data': serializer.data,
                'message':'Success'
            })
        else:
            return Response({
                'message':'No parking available'
            })

# checked
class ProvideTicket(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TicketSerializer

    def post(self,request):
        queryset = Parking.objects.filter(occupied = False).order_by('slot_number')
        if queryset.exists():
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': status.HTTP_200_OK,
                    'data':serializer.data,
                    'message':"Success"
                }) 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)     
        else:
            return Response({
                'message':"Parking is full."
            })

# checked
class CarEntry(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CarSerializer

    def post(self,request,pk):
        try:
            ticket= Ticket.objects.get(pk = pk)
        except Ticket.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Ticket of this id does not exist",
            })

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save(ticket = ticket)
            return Response({
                'status': status.HTTP_200_OK,
                'data':serializer.data,
                'message':"Success"
            }) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)        

# checked
class UpdateParkingSlotStatus(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permissions_classes = (permissions.IsAuthenticated, )
    serializer_class = ParkingSerializer

    def patch(self,request,pk,format = None):
        try:
            ticket = Ticket.objects.get(pk =pk)
        except Ticket.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Ticket of this id does not exist",
            })

        if ticket.active == True:
            slot_allotted = ticket.slot_allotted
            parking = Parking.objects.get(slot_number = slot_allotted)
            serializer = self.serializer_class(parking,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'data':serializer.data,
                    'message':f"{ticket} updated"
                })
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'message':'Ticket is inactive.'
            })

# checked
class ExitParking(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CarSerializer

    def patch(self,request,pk,format = None):
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Car of this id does not exist",
            })

        if car.status == "Parked":
            serializer = CarSerializer(car,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'data':serializer.data,
                    'message':"Car Departed"
                })
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'Car you are trying to search has already departed.'})

# checked
class UpdateTicket(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TicketSerializer

    def patch(self,request,pk,format = None):
        try:
            ticket = Ticket.objects.get(pk = pk)
        except Ticket.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Ticket of this id does not exist",
            })
            
        if ticket.active == True:
            serializer = self.serializer_class(ticket, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'data':serializer.data,
                    'message':"Ticekt is inactive now"
                })
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'message':'Ticket is already inactive.'
            })

# checked
class UpdateCarStatus(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CarSerializer

    def patch(self,request,pk,format= None):
        try:
            car = Car.objects.get(pk = pk)
        except Car.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Car of this id does not exist",
            })

        if car.status == 'Parked':
            serializer = self.serializer_class(car,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'data':serializer.data,
                })
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'message':'Car has already departed.'
            })

# checked
class BillGenerator(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self,request,pk,format = None):
        try:
            ticket= Ticket.objects.get(pk = pk)
        except Ticket.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Ticket of this id does not exist",
            })

        if ticket.active == True:
            serializer = BillSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(ticket = ticket)
                return Response({
                    'status':status.HTTP_200_OK,
                    'data':serializer.data,
                    'message':'Success'
                })
            return Response({
                ' message':"Errror generating bill"
            })
        else:
            return Response({
                'message':'Ticket must be active for generating bill.'
            })

# checked
class Pay(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self,request,pk,format=None):
        try:
            bill= Bill.objects.get(pk = pk)
        except Bill.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Ticket of this id does not exist",
            })

        serializer = PaymentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(bill = bill)
            return Response({
                'status':status.HTTP_200_OK,
                'data':serializer.data,
                'message':'Success'
            })
        return Response({
            ' message':"Invalid Payment."
        })


# checked
class TicketHistory(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['slot_allotted', 'ticket_issued','active']

# checked
class PaymentHistory(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PaymentSerializer
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['bill__total_bill','total_payment','status','payment_date']








  



    





        


    
            



        





# error in change user password
# reset user password



