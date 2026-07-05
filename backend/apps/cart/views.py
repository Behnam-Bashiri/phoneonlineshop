from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.cart.models import SavedForLater
from apps.cart.serializers import (
    AddToCartSerializer,
    ApplyCouponSerializer,
    CartSerializer,
    SavedForLaterSerializer,
    UpdateCartItemSerializer,
)
from apps.cart.services import CartService
from core.utils.pagination import StandardResultsSetPagination


class CartView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def _get_session_key(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

    def get_cart(self, request):
        user = request.user if request.user.is_authenticated else None
        session_key = self._get_session_key(request) if not user else ""
        return CartService.get_or_create_cart(user=user, session_key=session_key)

    def get(self, request):
        cart = self.get_cart(request)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.get_cart(request)
        try:
            CartService.add_item(
                cart,
                serializer.validated_data["variant_id"],
                serializer.validated_data.get("quantity", 1),
            )
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        cart = self.get_cart(request)
        CartService.clear_cart(cart)
        return Response({"detail": "Cart cleared."})


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = CartService.get_or_create_cart(user=request.user)
        try:
            CartService.update_item_quantity(cart, item_id, serializer.validated_data["quantity"])
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data)

    def delete(self, request, item_id):
        cart = CartService.get_or_create_cart(user=request.user)
        CartService.remove_item(cart, item_id)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data)


class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = CartService.get_or_create_cart(user=request.user)
        try:
            CartService.apply_coupon(cart, serializer.validated_data["code"])
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data)

    def delete(self, request):
        cart = CartService.get_or_create_cart(user=request.user)
        CartService.remove_coupon(cart)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data)


class SavedForLaterViewSet(ReadOnlyModelViewSet):
    serializer_class = SavedForLaterSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return SavedForLater.objects.filter(user=self.request.user).select_related(
            "product", "variant", "product__brand"
        )


class SaveForLaterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            CartService.save_for_later(request.user, item_id)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Item saved for later."})


class MoveToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, saved_id):
        try:
            CartService.move_to_cart(request.user, saved_id)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        cart = CartService.get_or_create_cart(user=request.user)
        totals = CartService.get_cart_totals(cart)
        data = CartSerializer(cart, context={"request": request}).data
        data.update(totals)
        return Response(data)
