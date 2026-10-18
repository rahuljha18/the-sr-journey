from django.urls import path
from . import views

urlpatterns = [
    path("bookings/", views.booking_list, name="booking_list"),
    path("bookings/create/", views.create_booking, name="create_booking"),
    path(
        "bookings/track/<str:booking_id>/",
        views.booking_tracking,
        name="booking_tracking",
    ),
    path(
    "reports/bookings/export/",
    views.export_booking_report,
    name="export_booking_report",
),

path(
    "reports/revenue/export/",
    views.export_revenue_report,
    name="export_revenue_report",
),

path(
    "reports/partners/export/",
    views.export_partner_report,
    name="export_partner_report",
),
path(
    "booking/<str:booking_id>/",
    views.booking_detail,
    name="booking_detail"
),
path(
    "booking/<str:booking_id>/action/<str:action>/",
    views.booking_action,
    name="booking_action"
),
path(
    "booking/<str:booking_id>/payment/<str:payment_status>/",
    views.payment_action,
    name="payment_action"
),
path(
    "booking/<str:booking_id>/assign-partner/",
    views.assign_partner,
    name="assign_partner"
),

path(
    "partners/<int:partner_id>/booking-history/",
    views.partner_booking_history,
    name="partner_booking_history",
),

path(
    "settlements/<int:settlement_id>/receipt/",
    views.settlement_receipt,
    name="settlement_receipt",
),

path(
    "reports/settlements/export/",
    views.export_settlement_report,
    name="export_settlement_report",
),

path(
    "reports/commissions/export/",
    views.export_commission_report,
    name="export_commission_report",
),

path(
    "settlements/history/",
    views.settlement_history,
    name="settlement_history",
),
path(
    "partners/payment-dashboard/",
    views.partner_payment_dashboard,
    name="partner_payment_dashboard",
),

]