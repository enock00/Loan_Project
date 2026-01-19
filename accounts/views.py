import requests
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        id_no = request.POST.get("id_no", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not all([full_name, email, phone, id_no, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("register")

        if User.objects.filter(id_no=id_no).exists():
            messages.error(request, "ID number already exists.")
            return redirect("register")

        User.objects.create_user(
            email=email,
            phone=phone,
            id_no=id_no,
            full_name=full_name,
            password=password1
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "loans/register.html")

def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        id_no = request.POST.get("id_no", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not all([full_name, email, phone, id_no, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("register")

        if User.objects.filter(id_no=id_no).exists():
            messages.error(request, "ID number already exists.")
            return redirect("register")

        User.objects.create_user(
            email=email,
            phone=phone,
            id_no=id_no,
            full_name=full_name,
            password=password1
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "loans/register.html")


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        user = authenticate(request, identifier=identifier, password=password)

        if user:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "loans/login.html")

@login_required
def apply_loan(request):
    has_pending = Loan.objects.filter(user=request.user, status='pending').exists()

    if has_pending:
        messages.error(request, "You already have a pending loan.")
        return redirect('dashboard')

    if request.method == "POST":
        amount = request.POST.get("amount")
        purpose = request.POST.get("purpose")
        duration = request.POST.get("duration")
        pay_fee = request.POST.get("pay_fee")

        if pay_fee != "yes":
            messages.error(request, "You must pay the application fee to apply for a loan.")
            return redirect('apply_loan')

        Loan.objects.create(
            user=request.user,
            amount=amount,
            purpose=purpose,
            duration=duration,
            status="pending",
            fee_paid=True
        )

        messages.success(request, "Loan application submitted successfully.")
        return redirect('dashboard')

    return render(request, "loans/apply_loan.html")


@login_required
def dashboard(request):
    loans = Loan.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'loans': loans,
        'total_loans': loans.count(),
        'active_loans': loans.filter(status='approved').count(),
        'has_pending': loans.filter(status='pending').exists(),
    }
    return render(request, 'loans/dashboard.html', context)

@login_required
def update_loan_purpose(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)

    if request.method == "POST":
        loan.purpose = request.POST.get("purpose")
        loan.save()

    return redirect("dashboard")


@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "loans/profile.html")

def logout_view(request):
    logout(request)
    return redirect("login")