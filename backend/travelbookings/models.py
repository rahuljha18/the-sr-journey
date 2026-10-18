from django.db import models
from decimal import Decimal

class Booking(models.Model):

    BOOKING_STATUS = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT_STATUS = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    booking_id = models.CharField(max_length=30, unique=True)
    customer_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    service_type = models.CharField(max_length=50)
    package_name = models.CharField(max_length=150, blank=True)

    travel_date = models.DateField(null=True, blank=True)

    passengers = models.PositiveIntegerField(default=1)

    cab_category = models.CharField(max_length=50, blank=True)

    pickup_location = models.CharField(
        max_length=200,
        blank=True
    )

    drop_location = models.CharField(
        max_length=200,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    
    # Partner commission settings
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("5.00"),
    )

    # The SR Journey's 5% commission
    commission_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Amount payable to the assigned partner
    partner_payable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )


    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="PENDING"
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="PENDING"
    )

    special_requirement = models.TextField(
        blank=True
    )
    partner = models.ForeignKey(
    "Partner",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="bookings"
)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking_id} - {self.customer_name}"


class Partner(models.Model):

    PARTNER_STATUS = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    partner_name = models.CharField(
        max_length=100
    )

    company_name = models.CharField(
        max_length=150,
        blank=True
    )

    mobile = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    cab_category = models.CharField(
        max_length=50
    )

    vehicle_number = models.CharField(
        max_length=30
    )

    driver_name = models.CharField(
        max_length=100
    )

    driver_mobile = models.CharField(
        max_length=15
    )

    status = models.CharField(
        max_length=20,
        choices=PARTNER_STATUS,
        default="ACTIVE"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.partner_name} - {self.vehicle_number}"
    
    
class PartnerSettlement(models.Model):

    PAYMENT_METHODS = [
        ("UPI", "UPI"),
        ("BANK_TRANSFER", "Bank Transfer"),
        ("CASH", "Cash"),
        ("CHEQUE", "Cheque"),
        ("OTHER", "Other"),
    ]

    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        related_name="settlements"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="UPI"
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.partner.partner_name} - "
            f"₹{self.amount} - {self.payment_date}"
        )

# =========================================================
# PARTNER SETTLEMENT AUDIT LOG
# =========================================================

class SettlementAuditLog(models.Model):

    ACTION_CHOICES = [
        ("CREATED", "Created"),
        ("UPDATED", "Updated"),
        ("DELETED", "Deleted"),
    ]

    settlement_id = models.PositiveIntegerField(
        db_index=True
    )

    partner_name = models.CharField(
        max_length=100
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    performed_by = models.CharField(
        max_length=150,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    details = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.action} - "
            f"{self.partner_name} - "
            f"Settlement #{self.settlement_id}"
        )
