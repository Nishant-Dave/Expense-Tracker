from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Expense


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_spent = (
            Expense.objects.filter(user=self.request.user)
            .aggregate(total=Sum('amount'))
            .get('total') or 0
        )
        budget = self.request.user.monthly_budget or 0
        remaining_balance = budget - total_spent
        context['total_spent'] = total_spent
        context['monthly_budget'] = budget
        context['remaining_balance'] = remaining_balance

        return context
    
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    fields = ['amount', 'description', 'category', 'date']
    success_url = reverse_lazy('expenses:expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ExpenseUpdateView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    fields = ['amount', 'description', 'category', 'date']
    success_url = reverse_lazy('expenses:expense-list')

    def get_queryset(self):
        # Security: to prevent editing other's expense data'
        return Expense.objects.filter(user=self.request.user) 

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:expense-list')

    def get_queryset(self):
        # Security: to prevent deleting other's expense data'
        return Expense.objects.filter(user=self.request.user)    