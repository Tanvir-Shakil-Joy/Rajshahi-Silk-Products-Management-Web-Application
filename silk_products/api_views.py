from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from .models import SilkProduct, UserProfile
from .serializers import UserRegistrationSerializer, UserSerializer, SilkProductSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        UserProfile.objects.create(
            user=user,
            role=request.data.get('role', 'buyer'),
            phone=request.data.get('phone', '')
        )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class SilkProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = SilkProduct.objects.all()
    serializer_class = SilkProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SilkProduct.objects.all()
        search = self.request.query_params.get('search', None)
        product_type = self.request.query_params.get('type', None)
        available_only = self.request.query_params.get('available', None)

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(type__icontains=search))
        if product_type:
            queryset = queryset.filter(type=product_type)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(availability=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SilkProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SilkProduct.objects.all()
    serializer_class = SilkProductSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'error': 'You can only update your own products'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'error': 'You can only delete your own products'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_stats(request):
    total_products = SilkProduct.objects.count()
    available_products = SilkProduct.objects.filter(availability=True).count()
    product_types = SilkProduct.objects.values('type').distinct().count()
    
    return Response({
        'total_products': total_products,
        'available_products': available_products,
        'unavailable_products': total_products - available_products,
        'product_types': product_types,
    })