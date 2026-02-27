from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from expenses.models import Expense
import datetime

User = get_user_model()

class DashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='password',
            monthly_budget=5000.00
        )
        self.client.login(username='testuser', password='password')
        self.dashboard_url = reverse('dashboard:home')

    def test_zero_expense_edge_case(self):
        # User has 0 expenses currently
        response = self.client.get(self.dashboard_url)
        
        self.assertEqual(response.status_code, 200)
        # Should handle None from aggregate(Sum) and return 0
        self.assertEqual(response.context['total_expense'], 0)
        # Remaining balance should be entire monthly budget (5000 - 0)
        self.assertEqual(response.context['remaining_balance'], 5000)

    def test_total_expense_and_remaining_calculation(self):
        # Create multiple expenses
        Expense.objects.create(user=self.user, amount=100.50, category='FOOD', date=datetime.date.today())
        Expense.objects.create(user=self.user, amount=250.00, category='TRANSPORT', date=datetime.date.today())
        
        response = self.client.get(self.dashboard_url)
        
        self.assertEqual(response.status_code, 200)
        
        # Total should be 350.50
        self.assertEqual(float(response.context['total_expense']), 350.50)
        
        # Remaining should be 5000 - 350.50 = 4649.50
        self.assertEqual(float(response.context['remaining_balance']), 4649.50)
