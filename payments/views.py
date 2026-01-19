import json
import requests # type: ignore
from django.conf import settings # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .models import Transaction
@login_required(login_url='login')
def stk_push(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        phone = data.get("phone")

        if not phone:
            return JsonResponse({"success": False, "message": "Phone required"}, status=400)

        if phone.startswith("0"):
            phone = "254" + phone[1:]

        transaction = Transaction.objects.create(
            user=request.user,
            amount=1,
            phone=phone,
            status="pending"
        )

        reference = f"APPFEE-{transaction.id}"

        payload = {
            "amount": 1,
            "phone_number": phone,
            "currency": "KES",
            "reference": reference,
            "description": "Loan Application Fee",
            "callback_url": "https://YOUR-NGROK-URL/payments/stk-push-webhook/",
        }

        headers = {
            "Authorization": f"Bearer {settings.INTASEND_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://sandbox.intasend.com/api/v1/payment/mpesa-stk-push/",
            json=payload,
            headers=headers,
            timeout=30
        )

        print("INTASEND STATUS:", response.status_code)
        print("INTASEND BODY:", response.text)

        return JsonResponse({
            "success": True,
            "invoice_id": transaction.id,
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

@csrf_exempt
def stk_push_webhook(request):
    """
    Webhook called by IntaSend when payment completes
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        reference = data.get("reference")  # e.g., APPFEE-12
        status = data.get("status")        # "completed" or "failed"

        if not reference:
            return JsonResponse({"error": "Reference missing"}, status=400)

        # Extract transaction ID from reference
        try:
            transaction_id = int(reference.split("-")[1])
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.status = status
            transaction.save()
        except Exception as e:
            return JsonResponse({"error": f"Transaction not found: {e}"}, status=400)

        return JsonResponse({"status": "received"})

    except Exception as e:
        return JsonResponse({"error": f"Invalid payload: {e}"}, status=400)

@login_required(login_url='login')
def check_payment_status(request, transaction_id):
    """
    Used by frontend JS polling to check if the Ksh 1 application fee is paid.
    """
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        return JsonResponse({"paid": transaction.status == "completed"})
    except Transaction.DoesNotExist:
        return JsonResponse({"paid": False})