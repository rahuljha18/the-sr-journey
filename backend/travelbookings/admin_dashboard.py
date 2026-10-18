from django.db import models
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from .models import Booking, PartnerSettlement
from .models import Booking


@staff_member_required
def dashboard_view(request):

    # =========================
    # CURRENT DATE
    # =========================

    today = timezone.localdate()

    current_year = today.year
    current_month = today.month

    # =========================
    # DATE FILTER
    # =========================

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    filtered_bookings = Booking.objects.all()

    if start_date:
        try:
            start_date_obj = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            filtered_bookings = filtered_bookings.filter(
                created_at__date__gte=start_date_obj
            )

        except ValueError:
            start_date = ""

    if end_date:
        try:
            end_date_obj = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()

            filtered_bookings = filtered_bookings.filter(
                created_at__date__lte=end_date_obj
            )

        except ValueError:
            end_date = ""

    # =========================
    # BOOKING COUNTS
    # =========================

    total_bookings = Booking.objects.count()

    pending_bookings = Booking.objects.filter(
        booking_status="PENDING"
    ).count()

    confirmed_bookings = Booking.objects.filter(
        booking_status="CONFIRMED"
    ).count()

    completed_bookings = Booking.objects.filter(
        booking_status="COMPLETED"
    ).count()

    cancelled_bookings = Booking.objects.filter(
        booking_status="CANCELLED"
    ).count()


    # =========================
    # PARTNER ASSIGNMENT
    # =========================

    assigned_bookings = Booking.objects.filter(
        partner__isnull=False
    ).count()

    unassigned_bookings = Booking.objects.filter(
        partner__isnull=True
    ).count()


    # =========================
    # TOTAL REVENUE
    # =========================

    total_revenue = Booking.objects.filter(
        booking_status__in=[
            "CONFIRMED",
            "COMPLETED"
        ]
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # =========================
    # CURRENT MONTH BOOKINGS
    # =========================

    monthly_bookings = Booking.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    )

    current_month_bookings = monthly_bookings.count()


    # =========================
    # CURRENT MONTH REVENUE
    # =========================

    current_month_revenue = monthly_bookings.filter(
        booking_status__in=[
            "CONFIRMED",
            "COMPLETED"
        ]
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # =========================
    # CURRENT MONTH COMPLETED
    # =========================

    current_month_completed = monthly_bookings.filter(
        booking_status="COMPLETED"
    ).count()


    # =========================
    # CURRENT MONTH CONFIRMED
    # =========================

    current_month_confirmed = monthly_bookings.filter(
        booking_status="CONFIRMED"
    ).count()
        # =========================
    # FILTERED REPORT
    # =========================

    filtered_booking_count = filtered_bookings.count()

    filtered_revenue = filtered_bookings.filter(
        booking_status__in=[
            "CONFIRMED",
            "COMPLETED"
        ]
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    filtered_confirmed = filtered_bookings.filter(
        booking_status="CONFIRMED"
    ).count()

    filtered_completed = filtered_bookings.filter(
        booking_status="COMPLETED"
    ).count()

    filtered_cancelled = filtered_bookings.filter(
        booking_status="CANCELLED"
    ).count()

    # =========================
    # PAYMENT SUMMARY
    # =========================

    paid_revenue = filtered_bookings.filter(
        payment_status="PAID"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    pending_payment = filtered_bookings.filter(
        payment_status="PENDING"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    failed_payment = filtered_bookings.filter(
        payment_status="FAILED"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    refunded_payment = filtered_bookings.filter(
        payment_status="REFUNDED"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    paid_bookings = filtered_bookings.filter(
        payment_status="PAID"
    ).count()

    pending_payment_bookings = filtered_bookings.filter(
        payment_status="PENDING"
    ).count()
    
    
    # =========================
    # COMMISSION SUMMARY
    # =========================

    total_commission = filtered_bookings.filter(
        booking_status__in=["CONFIRMED", "COMPLETED"]
    ).aggregate(
        total=Sum("commission_amount")
    )["total"] or 0

    total_partner_payable = filtered_bookings.filter(
        partner__isnull=False,
        booking_status__in=["CONFIRMED", "COMPLETED"]
    ).aggregate(
        total=Sum("partner_payable")
    )["total"] or 0

    paid_commission = filtered_bookings.filter(
        payment_status="PAID",
        booking_status__in=["CONFIRMED", "COMPLETED"]
    ).aggregate(
        total=Sum("commission_amount")
    )["total"] or 0

    # =========================
    # PARTNER-WISE BOOKINGS
    # =========================

   

    # =========================
    # PARTNER-WISE PERFORMANCE
    # =========================

    partner_summary = list(
        Booking.objects.filter(
            partner__isnull=False
        ).values(
            "partner__id",
            "partner__partner_name",
        ).annotate(
            booking_count=Count("id"),
            completed_count=Count(
                "id",
                filter=models.Q(booking_status="COMPLETED"),
            ),
            cancelled_count=Count(
                "id",
                filter=models.Q(booking_status="CANCELLED"),
            ),
            pending_count=Count(
                "id",
                filter=models.Q(booking_status="PENDING"),
            ),
            total_amount=Sum("amount"),
            paid_amount=Sum(
                "amount",
                filter=models.Q(payment_status="PAID"),
            ),
            total_commission=Sum("commission_amount"),
            total_partner_payable=Sum(
                "partner_payable",
                filter=models.Q(
                    booking_status__in=["CONFIRMED", "COMPLETED"]
                ),
            ),
        ).order_by("-booking_count")
    )

    # =========================
    # PARTNER SETTLEMENT SUMMARY
    # =========================

    for partner in partner_summary:
        partner_id = partner["partner__id"]

        total_paid = (
            PartnerSettlement.objects.filter(
                partner_id=partner_id
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        total_payable = (
            Booking.objects.filter(
                partner_id=partner_id,
                booking_status__in=["CONFIRMED", "COMPLETED"],
            ).aggregate(
                total=Sum("partner_payable")
            )["total"] or 0
        )

        partner["settlement_paid"] = total_paid
        partner["settlement_pending"] = total_payable - total_paid

    partner_chart_labels = []
    partner_chart_bookings = []
    partner_chart_revenue = []


    for partner in partner_summary:
        partner_chart_labels.append(
        partner["partner__partner_name"]
        )
        partner_chart_bookings.append(
        partner["booking_count"]
        )
        partner_chart_revenue.append(
        float(partner["total_amount"] or 0)
        )

    # =========================
    # RECENT BOOKINGS
    # =========================

    recent_bookings = Booking.objects.select_related(
        "partner"
    ).order_by(
        "-created_at"
    )[:10]

    booking_status_chart = {
    "Pending": pending_bookings,
    "Confirmed": confirmed_bookings,
    "Completed": completed_bookings,
    "Cancelled": cancelled_bookings,
}
    # =========================
    # CONTEXT
    # =========================

    context = {

        # Overall
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "booking_status_chart": booking_status_chart,
        "partner_chart_labels": partner_chart_labels,
        "partner_chart_bookings": partner_chart_bookings,
        "partner_chart_revenue": partner_chart_revenue,
        # Partners
        "assigned_bookings": assigned_bookings,
        "unassigned_bookings": unassigned_bookings,

        # Revenue
        
        "total_revenue": total_revenue,

        # Commission Summary
        "total_commission": total_commission,
        "total_partner_payable": total_partner_payable,
        "paid_commission": paid_commission,

        # Current month
        "current_month_bookings": current_month_bookings,
        "current_month_revenue": current_month_revenue,
        "current_month_completed": current_month_completed,
        "current_month_confirmed": current_month_confirmed,
        # Date Filter
        "start_date": start_date or "",
        "end_date": end_date or "",
        "filtered_booking_count": filtered_booking_count,
        "filtered_revenue": filtered_revenue,
        "filtered_confirmed": filtered_confirmed,
        "filtered_completed": filtered_completed,
        "filtered_cancelled": filtered_cancelled,
        # Payment Summary
        "paid_revenue": paid_revenue,
        "pending_payment": pending_payment,
        "failed_payment": failed_payment,
        "refunded_payment": refunded_payment,
        "paid_bookings": paid_bookings,
        "pending_payment_bookings": pending_payment_bookings,
        # Partner report
        "partner_summary": partner_summary,

        # Recent bookings
        "recent_bookings": recent_bookings,
    }


    return render(
        request,
        "travelbookings/admin_dashboard.html",
        context
    )