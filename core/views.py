

from django.shortcuts import render, redirect
from .models import Booking
from django.db.models import Sum
from datetime import date, timedelta
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Expense, MonthlyExpense, BusinessRule
from django.db.models import Sum
from django.shortcuts import render
from .models import Booking, Expense
from django.contrib.auth import authenticate, login
from datetime import date
from .models import Profile



# ADD BOOKING (keep this)

@login_required
def add_booking(request):

    if request.method == 'POST':

        Booking.objects.create(

            customer_name=request.POST['customer_name'],
            phone=request.POST['phone'],
            office_phone=request.POST['office_phone'],
            from_location=request.POST['from_location'],
            to_location=request.POST['to_location'],
            time=request.POST['time'],

            total_price=float(request.POST['total_price'] or 0),
            advance=float(request.POST['advance'] or 0),

            date=request.POST['date'],

            status='Pending'
        )

        return redirect('/employee-dashboard/')

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

    completed_moves = Booking.objects.filter(
        status__iexact='completed',
        date=today
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

        'search': search,
    }

    return render(request, 'index.html', context)



@login_required
def add_expense(request):

    bookings = Booking.objects.all()

    if request.method == 'POST':

        booking = Booking.objects.get(
            id=request.POST['booking']
        )

        labor = float(request.POST['labor'] or 0)

        packers = float(request.POST['packers'] or 0)

        supervisor = float(request.POST['supervisor'] or 0)

        driver = float(request.POST['driver'] or 0)

        stairs = float(request.POST['stairs'] or 0)


        derdare = int (request.POST['derdare'] or 0)

        night = int(request.POST['night'] or 0)

        long_way = int(request.POST['long_way'] or 0)

        carpenter = int( request.POST['carpenter'] or 0)



        additional = float(request.POST['additional'] or 0)

        total = (
            labor +
            packers +
            supervisor +
            driver +
            stairs +
            derdare +
           night +
           long_way +
           carpenter +
            additional 
            
        )

        Expense.objects.create(

            booking=booking,

            labor=labor,

            packers=packers,

            supervisor=supervisor,

            driver=driver,

            stairs=stairs,
    
        
             derdare=derdare,

             night=night,

             long_way=long_way,

            carpenter=carpenter,

            additional=additional,

            

            total=round(total, 2),

            date=request.POST['date']
        )

        return redirect('/employee-dashboard/')

    return render(
        request,
        'add_expense.html',
        {
            'bookings': bookings
        }
    )


@login_required
def edit_booking(request, id):

    booking = Booking.objects.get(id=id)

    if request.method == 'POST':

        booking.customer_name = request.POST['customer_name']
        booking.phone = request.POST['phone']
        booking.from_location = request.POST['from_location']
        booking.to_location = request.POST['to_location']

        booking.total_price = float(request.POST['total_price'] or 0)
        booking.advance = float(request.POST['advance'] or 0)
        booking.extra = float(request.POST['extra'] or 0)

        booking.balance = (
            booking.total_price
            + booking.extra
            - booking.advance
        )

        booking.date = request.POST['date']
        booking.status = request.POST['status']

        booking.save()

        return redirect('/employee-dashboard/')

    return render(
        request,
        'edit_booking.html',
        {
            'booking': booking
        }
    )

@login_required
def delete_booking(request, id):
    booking = Booking.objects.get(id=id)

    booking.delete()

    return redirect('/employee-dashboard/')


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
    daily_income = int (bookings.filter(
        date=today
    ).aggregate(
        Sum('total_price')
    )['total_price__sum']() ) or 0

    daily_expense = int ( expenses.filter(
        date=today
    ).aggregate(
        Sum('total')
    )['total__sum'] )or 0

    daily_profit = int (daily_income - daily_expense)

    # WEEKLY
    week_ago = today - timedelta(days=7)

    weekly_income = int (bookings.filter(
        date__gte=week_ago
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] ) or 0

    weekly_expense = int (expenses.filter(
        date__gte=week_ago
    ).aggregate(
        Sum('total')
    )['total__sum'] ) or 0

    weekly_profit = int (weekly_income - weekly_expense)

    # MONTHLY
    monthly_income = int (bookings.filter(
        date__month=today.month
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] ) or 0

    monthly_expense = int (expenses.filter(
        date__month=today.month
    ).aggregate(
        Sum('total')
    )['total__sum'] ) or 0

    monthly_profit = int (monthly_income - monthly_expense)

    # YEARLY
    yearly_income = int (bookings.filter(
        date__year=today.year
    ).aggregate(
        Sum('total_price')
    )['total_price__sum'] )or 0

    yearly_expense = int (  expenses.filter(
        date__year=today.year
    ).aggregate(
        Sum('total')
    )['total__sum']  ) or 0

    yearly_profit = int (yearly_income - yearly_expense)

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

def upcoming_bookings(request):

    bookings = Booking.objects.exclude(
        status='Completed'
    ).order_by('date')

    today = date.today()

    tomorrow = today + timedelta(days=1)

    context = {

        'bookings': bookings,

        'today': today,

        'tomorrow': tomorrow,


    }

    return render(
        request,
        'upcoming_bookings.html',
        context
    )


from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Booking

@login_required
def completed_moves(request):

    today = date.today()

    # BOTH ADMIN AND EMPLOYEE SEE ONLY TODAY
    bookings = Booking.objects.filter(
        status__iexact='completed',
        date=today
    )

    return render(request, 'completed_moves.html', {
        'bookings': bookings,
        'today': today,
    })

def business_rule(request):

    return render(
        request,
        'business_rule.html'
    )


@login_required
def add_monthly_expense(request):

    from .models import MonthlyExpense

    if request.method == 'POST':

        fuel = int(request.POST['fuel'] or 0)

        repair = int(request.POST['repair'] or 0)

        oil = int(request.POST['oil'] or 0)

        office_rent = int(request.POST['office_rent'] or 0)

        house_rent = int(request.POST['house_rent'] or 0)

        other = int(request.POST['other'] or 0)

        total = (

            fuel +

            repair +

            oil +

            office_rent +

            house_rent +

            other

        )

        MonthlyExpense.objects.create(

            month=int(request.POST['month']),

            fuel=fuel,

            repair=repair,

            oil=oil,

            office_rent=office_rent,

            house_rent=house_rent,

            other=other,

            total=total,

        )

        return redirect('/monthly-expense/')

    monthly_expenses = MonthlyExpense.objects.all()

    return render(

        request,

        'monthly_expense.html',

        {

            'monthly_expenses': monthly_expenses

        }
    )

from django.shortcuts import render
from django.db.models import Sum
from .models import Booking, Expense

def profit_loss(request):

    months = [
        (1, "January"), (2, "February"), (3, "March"),
        (4, "April"), (5, "May"), (6, "June"),
        (7, "July"), (8, "August"), (9, "September"),
        (10, "October"), (11, "November"), (12, "December"),
    ]

    month = request.GET.get("month")
    week = request.GET.get("week")

    context = {
        "months": months,
        "selected_month": None,
    }

    # no month selected → show grid
    if not month:
        return render(request, "profit_loss.html", context)

    month = int(month)

    # BASE QUERY (MONTH FILTER)
    bookings = Booking.objects.filter(date__month=month)
    expenses = Expense.objects.filter(booking__date__month=month)

    # WEEK FILTER (FIXED - NOT ISO WEEK)
    if week:
        week = int(week)

        if week == 1:
            bookings = bookings.filter(date__day__gte=1, date__day__lte=7)
            expenses = expenses.filter(booking__date__day__gte=1, booking__date__day__lte=7)

        elif week == 2:
            bookings = bookings.filter(date__day__gte=8, date__day__lte=14)
            expenses = expenses.filter(booking__date__day__gte=8, booking__date__day__lte=14)

        elif week == 3:
            bookings = bookings.filter(date__day__gte=15, date__day__lte=21)
            expenses = expenses.filter(booking__date__day__gte=15, booking__date__day__lte=21)

        elif week == 4:
            bookings = bookings.filter(date__day__gte=22)
            expenses = expenses.filter(booking__date__day__gte=22)

    # INCOME
    total_income = sum(b.total_price or 0 for b in bookings)

    # EXPENSE (SAFE)
    total_expense = expenses.aggregate(
        total=Sum("total")
    )["total"] or 0

    # PROFIT
    total_profit = total_income - total_expense

    # CONTEXT
    context.update({
        "selected_month": month,
        "selected_month_name": dict(months).get(month),
        "bookings": bookings,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_profit": total_profit,
    })

    return render(request, "profit_loss.html", context)

@login_required
def profit_details(request, month):

    from django.db.models import Sum
    from .models import Booking, Expense, MonthlyExpense

    months = {

        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',

    }

    month_name = months.get(month)

    bookings = Booking.objects.filter(
        date__month=month
    )

    total_income = bookings.aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    daily_expense = Expense.objects.filter(
        date__month=month
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    monthly_expense = MonthlyExpense.objects.filter(
        month=month
    ).aggregate(
        Sum('total')
    )['total__sum'] or 0

    total_expense = (
        daily_expense +
        monthly_expense
    )

    total_profit = (
        total_income -
        total_expense
    )

    return render(

        request,

        'profit_details.html',

        {

            'month_name': month_name,

            'bookings': bookings,

            'total_income': total_income,

            'total_expense': total_expense,

            'total_profit': total_profit,

        }

    )


from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Booking

@login_required
def dashboard(request):

    if request.user.profile.role != 'employee':
        return redirect('/admin-dashboard/')

    today = date.today()

    total_bookings = Booking.objects.filter(
        status='Pending'
    ).count()

    completed_moves = Booking.objects.filter(
        status__iexact='completed',
        date=today
    ).count()

    return render(request, 'employee_dashboard.html', {
        'total_bookings': total_bookings,
        'completed_moves': completed_moves,
    })


@login_required
def daily_expense_report(request):

    expenses = Expense.objects.all().order_by('-date')

    return render(
        request,
        'daily_expense_report.html',
        {
            'expenses': expenses
        }
    )


@login_required
def monthly_expense_report(request):

    monthly_expenses = MonthlyExpense.objects.all()

    return render(
        request,
        'monthly_expense_report.html',
        {
            'monthly_expenses': monthly_expenses
        }
    )


@login_required
def admin_dashboard(request):

    if request.user.profile.role != 'admin':

        return redirect('/employee-dashboard/')

    total_bookings = Booking.objects.filter(
        status='Pending'
    ).count()

    today = date.today()

    completed_moves = Booking.objects.filter(
    status='Completed',
    date=today
).count()

    total_progress = Booking.objects.filter(
    status='Completed'
).count()

    daily_expense = Expense.objects.count()

    monthly_expense = MonthlyExpense.objects.count()

    profit = Booking.objects.count()

    return render(
        request,
        'admin_dashboard.html',
        {
            'total_bookings': total_bookings,
            'completed_moves': completed_moves,
            'daily_expense': daily_expense,
            'monthly_expense': monthly_expense,
            'profit': profit,
            'total_progress': total_progress,
        }
    )




@login_required
def employee_monthly_expense(request):

    if request.method == 'POST':

        fuel = int(request.POST['fuel'] or 0)

        repair = int(request.POST['repair'] or 0)

        oil = int(request.POST['oil'] or 0)

        house_rent = int(request.POST['house_rent'] or 0)

        office_rent = int(request.POST['office_rent'] or 0)

        payment = int(request.POST['payment'] or 0)

        other = int(request.POST['other'] or 0)

        total = (
            fuel +
            repair +
            oil +
            house_rent +
            office_rent +
            payment +
            other
        )

        MonthlyExpense.objects.create(

            month=int(request.POST['month']),

            fuel=fuel,

            repair=repair,

            oil=oil,

            house_rent=house_rent,

            office_rent=office_rent,

            payment=payment,

            other=other,

            total=total,
        )

        return redirect('/employee-dashboard/')

    return render(
        request,
        'employee_monthly_expense.html'
    )



@login_required
def employee_daily_expense(request):

    bookings = Booking.objects.all()

    if request.method == 'POST':

        booking = Booking.objects.get(
            id=request.POST['booking']
        )

        labor = float(request.POST['labor'] or 0)
        packers = float(request.POST['packers'] or 0)
        supervisor = float(request.POST['supervisor'] or 0)
        driver = float(request.POST['driver'] or 0)
        stairs = float(request.POST['stairs'] or 0)

        derdare = int(request.POST['derdare'] or 0)
        night = int(request.POST['night'] or 0)
        long_way = int(request.POST['long_way'] or 0)
        carpenter = int(request.POST['carpenter'] or 0)

        additional = float(request.POST['additional'] or 0)

        total = (
            labor +
            packers +
            supervisor +
            driver +
            stairs +
            derdare +
            night +
            long_way +
            carpenter +
            additional
        )

        Expense.objects.create(
            booking=booking,
            labor=labor,
            packers=packers,
            supervisor=supervisor,
            driver=driver,
            stairs=stairs,
            derdare=derdare,
            night=night,
            long_way=long_way,
            carpenter=carpenter,
            additional=additional,
            total=round(total, 2),
            date=request.POST['date']
        )

        return redirect('/employee-daily-expense/')

    # Show today's expenses + running total
    today = date.today()

    expenses_today = Expense.objects.filter(date=today).order_by('-id')

    grand_total = expenses_today.aggregate(
        Sum('total')
    )['total__sum'] or 0

    return render(
        request,
        'add_expense.html',
        {
            'bookings': bookings,
            'expenses_today': expenses_today,
            'grand_total': grand_total,
            'today': today,
        }
    )


def home(request):
    return render(request, "home.html")



def employee_business_rule(request):

    rule = BusinessRule.objects.last()

    return render(
        request,
        'employee_business_rule.html',
        {
            'rule': rule
        }
    )



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if hasattr(user, 'profile') and user.profile.role == 'admin':
                return redirect("/admin-dashboard/")
            else:
                return redirect("/employee-dashboard/")

        return render(request, "home.html", {
            "error": "Invalid username or password"
        })

    return render(request, "home.html")


@login_required
def total_progress(request):

    from datetime import date, timedelta

    today = date.today()

    bookings = Booking.objects.filter(
        status='Completed'
    ).order_by('-date')

    search_date = request.GET.get('search_date')

    filter_type = request.GET.get('filter')

    # SEARCH BY DATE
    if search_date:

        bookings = bookings.filter(
            date=search_date
        )

    # FILTERS
    elif filter_type == '1week':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=7)
        )

    elif filter_type == '2week':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=14)
        )

    elif filter_type == '3week':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=21)
        )

    elif filter_type == '1month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=30)
        )

    elif filter_type == '2month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=60)
        )

    elif filter_type == '3month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=90)
        )

    elif filter_type == '4month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=120)
        )

    elif filter_type == '5month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=150)
        )

    elif filter_type == '6month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=180)
        )

    elif filter_type == '7month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=210)
        )

    elif filter_type == '8month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=240)
        )

    elif filter_type == '9month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=270)
        )

    elif filter_type == '10month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=300)
        )

    elif filter_type == '11month':

        bookings = bookings.filter(
            date__gte=today - timedelta(days=330)
        )

    # TOTALS
    total_moves = bookings.count()

    total_income = 0

    total_balance = 0

    for booking in bookings:

        total_income += booking.total_price or 0

        total_balance += booking.balance or 0

    return render(

        request,

        'total_progress.html',

        {

            'bookings': bookings,

            'total_moves': total_moves,

            'total_income': total_income,

            'total_balance': total_balance,

        }

    )

from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from .models import Booking, Expense, MonthlyExpense

@login_required
def employee_dashboard(request):

    today = date.today()

    # =========================
    # 📦 TOTAL BOOKINGS (TODAY)
    # =========================
    total_bookings = Booking.objects.filter(
        date=today
    ).count()

    # =========================
    # ✅ COMPLETED MOVES (TODAY)
    # =========================
    completed_moves = Booking.objects.filter(
        status__iexact='completed',
        date=today
    ).count()

    # =========================
    # 💰 DAILY EXPENSE (TODAY)
    # =========================
    daily_expense = Expense.objects.filter(
        date=today
    ).aggregate(total=Sum('total'))['total'] or 0

    # =========================
    # 📊 MONTHLY EXPENSE
    # =========================
    monthly_expense = MonthlyExpense.objects.aggregate(
        total=Sum('total')
    )['total'] or 0

    return render(request, 'employee_dashboard.html', {
        'total_bookings': total_bookings,
        'completed_moves': completed_moves,
        'daily_expense': daily_expense,
        'monthly_expense': monthly_expense,
        'today': today,
    })

from datetime import date

def get_completed_bookings(user):
    today = date.today()

    qs = Booking.objects.filter(status__iexact='completed')

    if not user.is_superuser:
        qs = qs.filter(date=today)

    return qs

from django.contrib.auth.models import User
from django.http import HttpResponse

def fix_user(request):
    u = User.objects.get(username="helen")
    u.set_password("fghIOP45@@")
    u.save()

    return HttpResponse("Password fixed")