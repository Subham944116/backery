from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import Product, Cart, CartItem
from .serializers import *
from rest_framework import status

# PRODUCT LIST + FILTERS
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Product.objects.all()

        treat = self.request.query_params.get('treat')
        flavor = self.request.query_params.get('flavor')
        weight = self.request.query_params.get('weight')
        option = self.request.query_params.get('option')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        sort = self.request.query_params.get('sort')

        # ✅ Case-insensitive filters
        if treat:
            qs = qs.filter(treat_type__iexact=treat)

        if flavor:
            qs = qs.filter(flavor__iexact=flavor)

        if weight:
            qs = qs.filter(weight__iexact=weight)

        # ✅ JSONField safe filter
        if option:
            qs = qs.filter(options__icontains=option)

        # ✅ Convert price to numbers safely
        try:
            if min_price:
                qs = qs.filter(price__gte=float(min_price))
            if max_price:
                qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass  # ignore invalid price input

        # ✅ Sorting
        if sort == 'price_low_to_high':
            qs = qs.order_by('price')
        elif sort == 'price_high_to_low':            qs = qs.order_by('-price')
        elif sort == 'popularity':
            
            qs = qs.order_by('-popularity')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')

        return qs


 

class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductDetailSerializer(
            product,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


# ADD TO CART
class AddToCartView(APIView):
    authentication_classes = [TokenAuthentication]  # <-- token auth
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(
    cart=cart,
    product=product,
    custom_cake=None
)


        if not created:
            item.quantity += 1
            item.save()

        return Response({"message": "Added to cart"})


# VIEW CART
class CartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(
    cart,
    context={'request': request}
)
        return Response(serializer.data)



class OrderNowView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_item_id = request.data.get("cart_item_id")

        if not cart_item_id:
            return Response(
                {"error": "cart_item_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = CartItem.objects.get(
                id=cart_item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartItemSerializer(
            item,
            context={'request': request}
        )

        return Response(
            {
                "message": "Proceed to checkout",
                "item": serializer.data
            },
            status=status.HTTP_200_OK
        )
