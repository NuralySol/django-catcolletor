# Create your views here. View is like controllers in Express JS.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions # modify these imports to match
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Cat, Feeding, Toy
from .serializers import CatSerializer, FeedingSerializer, ToySerializer, UserSerializer

# Define the home view
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the cat-collector api home route!'}
        return Response(content)

# Updated CatList and CatDetail views below
class CatList(generics.ListCreateAPIView):
    serializer_class = CatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This ensures we only return cats belonging to the logged-in user
        user = self.request.user
        return Cat.objects.filter(user=user)

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)

class CatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CatSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Cat.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        toys_not_associated = Toy.objects.exclude(id__in=instance.toys.all())
        toys_serializer = ToySerializer(toys_not_associated, many=True)

        return Response({
            'cat': serializer.data,
            'toys_not_associated': toys_serializer.data
        })

    def perform_update(self, serializer):
        cat = self.get_object()
        if cat.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this cat."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this cat."})
        instance.delete()

# User Registration
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })

# User Login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)  # Fetch user profile
        refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })