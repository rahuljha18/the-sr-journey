
from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand
from travelbookings.models import Booking


class Command(BaseCommand):
    help = "Recalculate commission and partner payable for all bookings"

    def handle(self, *args, **options):
        bookings = Booking.objects.all().order_by("id")
        updated = 0

        for booking in bookings.iterator():
            amount = booking.amount or Decimal("0.00")
            rate = booking.commission_rate

            if rate is None or rate <= 0:
                rate = Decimal("5.00")

            commission = (
                amount * rate / Decimal("100")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            if booking.partner_id:
                payable = amount - commission
            else:
                payable = Decimal("0.00")

            booking.commission_rate = rate
            booking.commission_amount = commission
            booking.partner_payable = payable

            booking.save(update_fields=[
                "commission_rate",
                "commission_amount",
                "partner_payable",
            ])

            updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully recalculated {updated} booking(s)."
            )
        )
