from rest_framework import serializers
from base.serializers import BaseSerializer
from ..models.payment_method_option import PaymentMethodOption


class PaymentMethodOptionSerializer(BaseSerializer):
    # Serializer chuyển đổi giữa model và JSON cho API
    class Meta:
        model = PaymentMethodOption
        fields = [
            "id",
            "name",
            "description",
            "method_type",
            "is_active",
            "legacy_value",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


