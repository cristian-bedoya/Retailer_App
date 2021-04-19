from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UserProfile, Order, Payment, Shipping
from .serializer import UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer
from .serializer import OrderSerializer, ShippingSerializer, PaymentSerializer

class UserRegistrationView(CreateAPIView):
    """ Class for user registration """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):
    """ Class for  User login"""

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserProfileView(RetrieveAPIView):
    """ Class for User profile view"""

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'gov_id':user_profile.gov_id,
                }

        except Exception as err_e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(err_e)
                }
        return Response(response, status=status_code)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_list(request):
    """
 List  user, or create a new payment.
 """
    
    data = []
    next_page = 1
    previous_page = 1
    user = UserProfile.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(user, 5)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = UserProfileSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        next_page = data.next_page_number()
    if data.has_previous():
        previous_page = data.previous_page_number()

    return Response({'data': serializer.data, 'count': paginator.count,
                     'numpages' : paginator.num_pages,
                     'nextlink': '/api user/?page=' + str(next_page), 
                     'prevlink': '/api user/?page=' + str(previous_page)})

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def users_detail(request, pk):
    """
 Retrieve, update or delete a payment by id/pk.
 """
    try:
        payment = Shipping.objects.get(pk=pk)
    except payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(payment, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(payment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders_list(request):
    """
 List  orders, or create a new order.
 """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        orders = Order.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = OrderSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count,
                         'numpages' : paginator.num_pages,
                         'nextlink': '/api/orders/?page=' + str(next_page),
                         'prevlink': '/api/orders/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def orders_detail(request, pk):
    """
    Retrieve, update or delete a order by id/pk.
    """
    if pk == "serializers":
        return

    if pk[0] == "[" and pk[-1] == "]":
        pk = pk[1:-1].split(",")

    try:
        if type(pk) is str:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order,context={'request': request})

        elif isinstance(pk, list):
            orders = []
            for i in pk:
                orders.append(Order.objects.get(pk=i))
            serializer = OrderSerializer(orders, context={'request': request}, many=True)

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)



    if request.method == 'GET':
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shippings_list(request):
    """
 List  shippings, or create a new payment.
 """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        shippings = Shipping.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(shippings, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ShippingSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count,
                         'numpages' : paginator.num_pages,
                         'nextlink': '/api shippings/?page=' + str(next_page),
                         'prevlink': '/api shippings/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = ShippingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def shippings_detail(request, pk):
    """
 Retrieve, update or delete a payment by id/pk.
 """
    try:
        payment = Shipping.objects.get(pk=pk)
    except payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShippingSerializer(payment, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShippingSerializer(payment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payments_list(request):
    """
 List  payments, or create a new payment.
 """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        payments = Payment.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(payments, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = PaymentSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count,
                         'numpages' : paginator.num_pages,
                         'nextlink': '/api payments/?page=' + str(next_page),
                         'prevlink': '/api payments/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def payments_detail(request, pk):
    """
 Retrieve, update or delete a payment by id/pk.
 """
    try:
        payment = Payment.objects.get(pk=pk)
    except payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentSerializer(payment, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PaymentSerializer(payment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
