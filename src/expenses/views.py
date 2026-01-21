from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Expense


class expenseListView(LoginRequiredMixin, ListView):
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