from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from expenses.models import Expense

@login_required
def dashboard_home(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    expenses = Expense.objects.filter(user=request.user)
    
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)
    
    # Calculate total safely mapping None back to Decimal 0
    total_agg = expenses.aggregate(total=Sum('amount'))['total']
    total_expense = total_agg if total_agg is not None else 0
    
    remaining_balance = request.user.monthly_budget - total_expense
    
    # Aggregation for Chart.js
    category_sums = expenses.values('category').annotate(amount_sum=Sum('amount'))
    
    # Format data for JSON serialization mapping codes to readable display names
    category_dict = dict(Expense.CATEGORY_CHOICES)
    chart_data = {
        category_dict.get(item['category'], item['category']): float(item['amount_sum'])
        for item in category_sums
    }
    
    context = {
        'total_expense': total_expense,
        'remaining_balance': remaining_balance,
        'chart_data': chart_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'dashboard/home.html', context)
