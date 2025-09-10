from django.db import models
from base.models import TimeStampedModel


class PaymentMethodOption(TimeStampedModel):
    OFFLINE = "offline"
    ONLINE = "online"
    METHOD_TYPE_CHOICES = (
        (OFFLINE, "offline"),
        (ONLINE, "online"),
    )

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    method_type = models.CharField(max_length=10, choices=METHOD_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    # Optional mapping to legacy constant in `ecommerce.constants.PaymentMethod`
    legacy_value = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "ecommerce_payment_methods"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


