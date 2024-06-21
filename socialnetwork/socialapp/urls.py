from django.urls import path
from .views import UserSignupAPIView, UserSearchAPIView,CustomTokenObtainPairView, LogoutAPIView ,SendFriendRequestAPIView,AcceptFriendRequestAPIView,RejectFriendRequestAPIView,FriendListAPIView,PendingFriendRequestListAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name='user-signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('send-friend-request/', SendFriendRequestAPIView.as_view(), name='send-friend-request'),
    path('accept-friend-request/<int:pk>/', AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),
    path('reject-friend-request/<int:pk>/', RejectFriendRequestAPIView.as_view(), name='reject-friend-request'),
    path('friends/', FriendListAPIView.as_view(), name='friends-list'),
    path('pending-friend-requests/', PendingFriendRequestListAPIView.as_view(), name='pending-friend-requests-list'),

]
