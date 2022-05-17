from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, BookSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import Book
from rest_framework.parsers import JSONParser
import io




# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration Successfull'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class BookDetail(APIView):
    def get(self,request,*args,**kwargs):
        jdata = request.body
        bobj = io.BytesIO(jdata)
        data = JSONParser().parse(bobj)
        id = data.get('id')
        if id is not None:
            try:
                bk = Book.objects.get(id=id)
            except Book.DoesNotExist:
                return Response({'msg':'record not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookSerializer(bk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        bk_qs = Book.objects.all()
        serializer = BookSerializer(bk_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        jdata = request.body
        bobj = io.BytesIO(jdata)
        data = JSONParser().parse(bobj)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response({'msg':'plz send the valid data'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,*args,**kwargs):
        jdata = request.body
        bobj = io.BytesIO(jdata)
        data = JSONParser().parse(bobj)
        id = data.get("id")
        try:
            bk = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({'msg':'record not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(bk, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'resource updated successfully'}, status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'plz send the valid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        jdata = request.body
        bobj = io.BytesIO(jdata)
        data = JSONParser().parse(bobj)
        id = data.get("id")
        try:
            bk = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({'msg':'record not found'}, status=status.HTTP_404_NOT_FOUND)
        bk.delete()
        return Response({'msg':'record deleted'}, status=status.HTTP_204_NO_CONTENT)

