from django.shortcuts import render

# Create your views here.
# accounts/views.py
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # call standard create
        response = super().create(request, *args, **kwargs)
        user = self.object if hasattr(self, 'object') else CustomUser.objects.get(pk=response.data['id'])
        # ensure token exists
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={'request': request}).data
        })

class LoginAPIView(ObtainAuthToken):
    """Returns a token and user data."""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={'request': request}).data
        })

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import SimpleUserSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Authenticated user follows target user.
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    request.user.following.add(target)
    return Response({'detail': f'Now following {target.username}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Authenticated user unfollows target user.
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    request.user.following.remove(target)
    return Response({'detail': f'Unfollowed {target.username}'}, status=status.HTTP_200_OK)

class FollowingListView(generics.ListAPIView):
    """
    List users that the authenticated user is following.
    """
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.following.all()

class FollowersListView(generics.ListAPIView):
    """
    List users that follow the specified user (or the authenticated user if no id).
    """
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # optional: allow viewing followers of a specific user via ?user_id=
        user_id = self.request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user
        return user.followers.all()