from rest_framework.decorators import action
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from base.views import BaseViewSet
from ..models.payment_method_option import PaymentMethodOption
from ..models.order import Order
from ..serializers.payment_method_option import PaymentMethodOptionSerializer


class PaymentMethodOptionViewSet(BaseViewSet):
    permission_classes = [AllowAny]
    queryset = PaymentMethodOption.objects.all()
    search_map = {
        "name": "icontains",
        "description": "icontains",
    }
    serializer_class = PaymentMethodOptionSerializer
    required_alternate_scopes = {}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.legacy_value is not None:
            if Order.objects.filter(payment_method=instance.legacy_value).exists():
                return Response({
                    "detail": "This payment method is used by existing orders. Deletion is not allowed. Please set status to Inactive."
                }, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        previous_active_count = PaymentMethodOption.objects.filter(is_active=True).count()
        instance = self.get_object()
        new_is_active = serializer.initial_data.get("is_active", None)
        if new_is_active is not None:
            if isinstance(new_is_active, str):
                new_is_active = new_is_active.lower() in ("true", "1", "yes")
            else:
                new_is_active = bool(new_is_active)
        # If turning off and it is the last active
        if new_is_active is False and instance.is_active and previous_active_count <= 1:
            raise serializers.ValidationError({
                "is_active": "At least one payment method must remain active."
            })
        serializer.save()

    @action(detail=False, methods=["post"], url_path="bulk-toggle")
    def bulk_toggle(self, request, *args, **kwargs):
        ids = request.data.get("ids", [])
        is_active = request.data.get("is_active", None)
        if not isinstance(ids, list) or is_active is None:
            return Response({"detail": "ids (list) and is_active (bool) are required"}, status=status.HTTP_400_BAD_REQUEST)
        is_active_bool = False
        if isinstance(is_active, str):
            is_active_bool = is_active.lower() in ("true", "1", "yes")
        else:
            is_active_bool = bool(is_active)
        if not is_active_bool:
            total_active = PaymentMethodOption.objects.filter(is_active=True).count()
            turning_off_count = PaymentMethodOption.objects.filter(id__in=ids, is_active=True).count()
            if total_active - turning_off_count <= 0:
                return Response({
                    "detail": "At least one payment method must remain active."
                }, status=status.HTTP_400_BAD_REQUEST)
        PaymentMethodOption.objects.filter(id__in=ids).update(is_active=is_active_bool)
        self.clear_querysets_cache()
        return Response(status=status.HTTP_204_NO_CONTENT)


