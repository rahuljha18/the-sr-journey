from decimal import Decimal

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Booking, Partner, PartnerSettlement, SettlementAuditLog
from django import forms
from django.db.models import Sum
from django.core.exceptions import ValidationError

def confirm_bookings(modeladmin, request, queryset):
    updated = queryset.update(booking_status="CONFIRMED")

    modeladmin.message_user(
        request,
        f"{updated} booking(s) confirmed successfully."
    )


confirm_bookings.short_description = "Confirm selected bookings"


def cancel_bookings(modeladmin, request, queryset):
    updated = queryset.update(booking_status="CANCELLED")

    modeladmin.message_user(
        request,
        f"{updated} booking(s) cancelled successfully."
    )


cancel_bookings.short_description = "Cancel selected bookings"


def mark_completed(modeladmin, request, queryset):
    updated = queryset.update(booking_status="COMPLETED")

    modeladmin.message_user(
        request,
        f"{updated} booking(s) marked as completed."
    )


mark_completed.short_description = "Mark selected bookings as completed"


def mark_payment_paid(modeladmin, request, queryset):
    updated = queryset.update(payment_status="PAID")

    modeladmin.message_user(
        request,
        f"{updated} booking(s) marked as paid."
    )


mark_payment_paid.short_description = "Mark selected bookings as paid"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_id",
        "customer_name",
        "mobile",
        "service_type",
        "package_name",
        "travel_date",
        "passengers",
        "cab_category",
        "partner",
        "amount",
        "commission_amount",
        "partner_payable",
        "payment_status",
        "booking_status",
        "created_at",
        
    )

    list_filter = (
        "booking_status",
        "payment_status",
        "service_type",
        "cab_category",
        "travel_date",
        "partner",
    )

    search_fields = (
        "booking_id",
        "customer_name",
        "mobile",
        "package_name",
        "partner__partner_name",
        "partner__vehicle_number",
        "partner__driver_name",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    actions = [
        confirm_bookings,
        cancel_bookings,
        mark_completed,
        mark_payment_paid,
    ]

    readonly_fields = (
        "booking_id",
        "created_at",
    )

    fieldsets = (
        (
            "Booking Information",
            {
                "fields": (
                    "booking_id",
                    "service_type",
                    "package_name",
                    "travel_date",
                    "passengers",
                    "cab_category",
                )
            },
        ),

        (
            "Customer Information",
            {
                "fields": (
                    "customer_name",
                    "mobile",
                )
            },
        ),

        (
            "Travel Information",
            {
                "fields": (
                    "pickup_location",
                    "drop_location",
                    "partner",
                    "special_requirement",
                )
            },
        ),

        
(
    "Payment & Commission",
    {
        "fields": (
            "amount",
            "commission_rate",
            "commission_amount",
            "partner_payable",
            "payment_status",
            "booking_status",
        )
    },
),


        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        from decimal import Decimal, ROUND_HALF_UP

        amount = obj.amount or Decimal("0.00")
        rate = obj.commission_rate or Decimal("5.00")

        obj.commission_amount = (
            amount * rate / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        if obj.partner_id:
            obj.partner_payable = (
                amount - obj.commission_amount
            )
        else:
            obj.partner_payable = Decimal("0.00")

        super().save_model(request, obj, form, change)

    def view_details(self, obj):
        url = reverse(
            "booking_detail",
            args=[obj.booking_id]
        )

        return format_html(
            '<a href="{}" target="_blank">👁️ View Details</a>',
            url
        )

    view_details.short_description = "Details"

    




@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    list_display = (
        "partner_name",
        "company_name",
        "mobile",
        "cab_category",
        "vehicle_number",
        "driver_name",
        "driver_mobile",
        "status",
        "created_at",
        "view_booking_history",
    )

    list_filter = (
        "status",
        "cab_category",
    )

    search_fields = (
        "partner_name",
        "company_name",
        "mobile",
        "vehicle_number",
        "driver_name",
        "driver_mobile",
    )

    ordering = ("-created_at",)

    list_per_page = 25
    def view_booking_history(self, obj):
        url = reverse(
        "partner_booking_history",
        args=[obj.id]
    )
        return format_html(
        '<a href="{}" target="_blank">View Booking History</a>',
        url
    )

    view_booking_history.short_description = "Booking History"
    
    

class PartnerSettlementForm(forms.ModelForm):

    class Meta:
        model = PartnerSettlement
        fields = "__all__"

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if amount is None or amount <= Decimal("0.00"):
            raise ValidationError(
                "Settlement amount must be greater than zero."
            )

        return amount

    def clean(self):
        cleaned_data = super().clean()

        partner = cleaned_data.get("partner")
        amount = cleaned_data.get("amount")

        if not partner or amount is None or amount <= 0:
            return cleaned_data

        # Only confirmed/completed bookings are payable
        total_payable = Booking.objects.filter(
            partner=partner,
            booking_status__in=["CONFIRMED", "COMPLETED"],
        ).aggregate(
            total=Sum("partner_payable")
        )["total"] or Decimal("0.00")

        # Exclude the current record when editing a settlement
        existing_settlements = PartnerSettlement.objects.filter(
            partner=partner
        )

        if self.instance and self.instance.pk:
            existing_settlements = existing_settlements.exclude(
                pk=self.instance.pk
            )

        already_paid = existing_settlements.aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

        remaining_balance = total_payable - already_paid

        if amount > remaining_balance:
            raise ValidationError(
                f"Payment exceeds the remaining payable balance. "
                f"Available balance: ₹{remaining_balance:.2f}"
            )

        return cleaned_data



@admin.register(PartnerSettlement)
class PartnerSettlementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "partner",
        "amount",
        "payment_date",
        "payment_method",
        "transaction_reference",
    )

    list_filter = ("payment_method", "payment_date")

    search_fields = (
        "partner__partner_name",
        "partner__vehicle_number",
        "transaction_reference",
    )

    ordering = ("-payment_date",)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        action = "UPDATED" if change else "CREATED"

        super().save_model(request, obj, form, change)

        changed_fields = ", ".join(form.changed_data) if change else "New settlement created"

        SettlementAuditLog.objects.create(
            settlement_id=obj.id,
            partner_name=obj.partner.partner_name,
            action=action,
            performed_by=request.user.get_username(),
            amount=obj.amount,
            details=changed_fields,
        )

    def delete_model(self, request, obj):
        SettlementAuditLog.objects.create(
            settlement_id=obj.id,
            partner_name=obj.partner.partner_name,
            action="DELETED",
            performed_by=request.user.get_username(),
            amount=obj.amount,
            details="Settlement deleted from admin",
        )

        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset.select_related("partner"):
            SettlementAuditLog.objects.create(
                settlement_id=obj.id,
                partner_name=obj.partner.partner_name,
                action="DELETED",
                performed_by=request.user.get_username(),
                amount=obj.amount,
                details="Settlement deleted using bulk admin action",
            )

        super().delete_queryset(request, queryset)


@admin.register(SettlementAuditLog)
class SettlementAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "settlement_id",
        "partner_name",
        "action",
        "performed_by",
        "amount",
        "created_at",
    )

    list_filter = ("action", "created_at")
    search_fields = (
        "settlement_id",
        "partner_name",
        "performed_by",
        "details",
    )

    ordering = ("-created_at",)
    list_per_page = 25

    readonly_fields = (
        "settlement_id",
        "partner_name",
        "action",
        "performed_by",
        "amount",
        "details",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

