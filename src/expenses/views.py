from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense
from .forms import ExpenseForm

class ExpenseListView(LoginRequiredMixin, generic.ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context

class ExpenseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def export_expenses(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses_report.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Date', 'Category', 'Amount', 'Description'])

    # Get data
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses_qs = Expense.objects.filter(user=request.user)
    
    if start_date:
        expenses_qs = expenses_qs.filter(date__gte=start_date)
    if end_date:
        expenses_qs = expenses_qs.filter(date__lte=end_date)
        
    expenses = expenses_qs.values(
        'date', 'category', 'amount', 'description'
    )
    
    # Map category codes to display values
    category_dict = dict(Expense.CATEGORY_CHOICES)

    # Write data rows
    for expense in expenses:
        category_display = category_dict.get(expense['category'], expense['category'])
        writer.writerow([
            expense['date'],
            category_display,
            expense['amount'],
            expense['description']  # May be empty string but handled gracefully by csv module
        ])

    return response