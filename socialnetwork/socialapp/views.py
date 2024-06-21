
from .throttling import UserRateThrottle
from datetime import datetime, timedelta
from rest_framework import generics, permissions
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import User,FriendRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from socialapp.serializer import UserSerializer, UserSignupSerializer,FriendRequestSerializer,FriendSerializer,PendingFriendRequestSerializer
#from socialapp.serializer import UserSerializer,UserSignupSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


'''users = User.objects.all()
for user in users:
    print(f"Email: {user.email}, Name: {user.name}")'''

class UserSignupAPIView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print(f"Login attempt with email: {request.data.get('email', '')}")
        response = super().post(request, *args, **kwargs)
        response.data['email'] = request.data.get('email', '')
        return response

class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchAPIView(generics.ListAPIView):
    #queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can search

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__iexact=query) | Q(name__icontains=query))
    


# Friend request
class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user, status='pending')


#request accepted by the user who recived the  friend request
class AcceptFriendRequestAPIView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user == request.user:
            instance.status = 'accepted'
            instance.save()
            return Response({'detail': 'Friend request accepted.'})
        else:
            return Response({'detail': 'You cannot accept this friend request.'}, status=status.HTTP_403_FORBIDDEN)


class RejectFriendRequestAPIView(generics.DestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user == request.user:
            instance.status = 'rejected'
            instance.save()
            return Response({'detail': 'Friend request rejected.'})
        else:
            return Response({'detail': 'You cannot reject this friend request.'}, status=status.HTTP_403_FORBIDDEN)


#List accepted friend request (the user who send the request)
class FriendListAPIView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter users who have accepted friend requests with the current user
        friends = FriendRequest.objects.filter(from_user=self.request.user, status='accepted').values_list('to_user', flat=True)
        return User.objects.filter(id__in=friends)
    

#List pending request which is send by user (Recived user)

class PendingFriendRequestListAPIView(generics.ListAPIView):
    serializer_class = PendingFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter friend requests where the current user is the to_user and status is pending
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')