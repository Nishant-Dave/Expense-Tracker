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
        return Expense.objects.filter(user=self.request.user)

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

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import pandas as pd

@login_required
def export_expenses(request):
    expenses = Expense.objects.filter(user=request.user).values(
        'date', 'category', 'amount', 'description'
    )
    
    # Create DataFrame
    df = pd.DataFrame(list(expenses))
    
    if not df.empty:
        # Map category codes to display values
        category_dict = dict(Expense.CATEGORY_CHOICES)
        df['category'] = df['category'].map(category_dict)
        
        # Rename columns for the actual CSV header
        df = df.rename(columns={
            'date': 'Date',
            'category': 'Category',
            'amount': 'Amount',
            'description': 'Description'
        })
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses_report.csv"'
    
    # Export explicitly without Pandas arbitrary numerical indices
    df.to_csv(response, index=False)
    
    return response