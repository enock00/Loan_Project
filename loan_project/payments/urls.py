from django.urls import path
from . import views

urlpatterns = [
    path("stk-push/", views.stk_push, name="stk_push"),
    path("stk-push-webhook/", views.stk_push_webhook, name="stk_push_webhook"),
    path("webhook-status/<int:transaction_id>/", views.check_payment_status, name="check_payment_status"),
]


