from django.contrib import admin
from .models import PaymentMethodOption


@admin.register(PaymentMethodOption)
class PaymentMethodOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "method_type", "is_active", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("method_type", "is_active")

# Register your models here.
