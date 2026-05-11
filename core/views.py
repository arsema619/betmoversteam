from django.shortcuts import render, redirect
from .models import Booking
from django.db.models import Sum
from datetime import date, timedelta
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ADD BOOKING (keep this)
@login_required
def add_booking(request):
    if request.method == 'POST':
        Booking.objects.create(
            messages.success(request, 'Booking Added Successfully'),
            customer_name=request.POST['customer_name'],
            phone=request.POST['phone'],
            from_location=request.POST['from_location'],
            to_location=request.POST['to_location'],
            total_price=request.POST['total_price'],
            advance=request.POST['advance'],
            balance=request.POST['balance'],
            date=request.POST['date'],
            status=request.POST['status'],
        )
        return redirect('/')

    return render(request, 'add_booking.html')


def dashboard(request):

    search = request.GET.get('search')

    bookings = Booking.objects.all().order_by('-date')

    if search:
        bookings = bookings.filter(
            customer_name__icontains=search
        )

    expenses = Expense.objects.all()

    today = date.today()

    tomorrow = today + timedelta(days=1)

    yesterday = today - timedelta(days=1)

    # BUSINESS RULES

    todays_bookings = bookings.filter(date=today)

    tomorrows_bookings = bookings.filter(date=tomorrow)

    yesterdays_bookings = bookings.filter(date=yesterday)

    # BOOKINGS

    total_bookings = bookings.count()

    todays_moves = todays_bookings.count()

    completed_moves = bookings.filter(
        status='Completed'
    ).count()

    # INCOME

    total_income = bookings.aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    # DAILY EXPENSE

    daily_expense = expenses.filter(
        date=today
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    # MONTHLY EXPENSE

    monthly_expense = expenses.filter(
        date__month=today.month
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    # TOTAL EXPENSE

    total_expense = expenses.aggregate(
        Sum('total')
    )['total__sum'] or 0

    # PROFIT

    profit = total_income - total_expense

    context = {

        'bookings': bookings,

        'todays_bookings': todays_bookings,

        'tomorrows_bookings': tomorrows_bookings,

        'yesterdays_bookings': yesterdays_bookings,

        'today': today,

        'tomorrow': tomorrow,

        'yesterday': yesterday,

        'total_bookings': total_bookings,

        'todays_moves': todays_moves,

        'completed_moves': completed_moves,

        'daily_expense': daily_expense,

        'monthly_expense': monthly_expense,

        'total_income': total_income,

        'total_expense': total_expense,

        'profit': profit,
    }

    return render(request, 'index.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        Expense.objects.create(
            labor=request.POST['labor'],
            packers=request.POST['packers'],
            driver=request.POST['driver'],
            supervisor=request.POST['supervisor'],
            additional=request.POST['additional'],
            miscellaneous=request.POST['miscellaneous'],
            total=request.POST['total'],
            date=request.POST['date'],
        )
        return redirect('/')

    return render(request, 'add_expense.html')

def edit_booking(request, id):
    booking = Booking.objects.get(id=id)

    if request.method == 'POST':
        booking.customer_name = request.POST['customer_name']
        booking.phone = request.POST['phone']
        booking.from_location = request.POST['from_location']
        booking.to_location = request.POST['to_location']
        booking.total_price = request.POST['total_price']
        booking.advance = request.POST['advance']
        booking.balance = request.POST['balance']
        booking.date = request.POST['date']
        booking.status = request.POST['status']

        booking.save()

        return redirect('/')

    return render(request, 'edit_booking.html', {
        'booking': booking
    })

def delete_booking(request, id):
    booking = Booking.objects.get(id=id)

    booking.delete()

    return redirect('/')


@login_required
def reports(request):
    bookings = Booking.objects.all()
    expenses = Expense.objects.all()

    total_income = bookings.aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    total_expense = expenses.aggregate(
        Sum('total')
    )['total__sum'] or 0

    completed_moves = bookings.filter(
        status='Completed'
    ).count()

    profit = total_income - total_expense

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'completed_moves': completed_moves,
        'profit': profit,
    }

    return render(request, 'reports.html', context)

def edit_expense(request, id):
    expense = Expense.objects.get(id=id)

    if request.method == 'POST':

        expense.labor = request.POST['labor']
        expense.packers = request.POST['packers']
        expense.driver = request.POST['driver']
        expense.supervisor = request.POST['supervisor']
        expense.additional = request.POST['additional']
        expense.miscellaneous = request.POST['miscellaneous']
        expense.total = request.POST['total']
        expense.date = request.POST['date']

        expense.save()

        return redirect('/')

    return render(request, 'edit_expense.html', {
        'expense': expense
    })


def delete_expense(request, id):
    expense = Expense.objects.get(id=id)

    expense.delete()

    return redirect('/')


@login_required
def reports(request):

    bookings = Booking.objects.all()
    expenses = Expense.objects.all()

    today = date.today()

    # DAILY
    daily_income = bookings.filter(
        date=today
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    daily_expense = expenses.filter(
        date=today
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    daily_profit = daily_income - daily_expense

    # WEEKLY
    week_ago = today - timedelta(days=7)

    weekly_income = bookings.filter(
        date__gte=week_ago
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    weekly_expense = expenses.filter(
        date__gte=week_ago
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    weekly_profit = weekly_income - weekly_expense

    # MONTHLY
    monthly_income = bookings.filter(
        date__month=today.month
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    monthly_expense = expenses.filter(
        date__month=today.month
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    monthly_profit = monthly_income - monthly_expense

    # YEARLY
    yearly_income = bookings.filter(
        date__year=today.year
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    yearly_expense = expenses.filter(
        date__year=today.year
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    yearly_profit = yearly_income - yearly_expense

    completed_moves = bookings.filter(
        status='Completed'
    ).count()

    context = {

        'daily_income': daily_income,
        'daily_expense': daily_expense,
        'daily_profit': daily_profit,

        'weekly_income': weekly_income,
        'weekly_expense': weekly_expense,
        'weekly_profit': weekly_profit,

        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_profit': monthly_profit,

        'yearly_income': yearly_income,
        'yearly_expense': yearly_expense,
        'yearly_profit': yearly_profit,

        'completed_moves': completed_moves,
    }

    return render(request, 'reports.html', context)



