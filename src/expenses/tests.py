from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Expense
import datetime

User = get_user_model()

class ExpenseTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username='usera', password='password')
        self.user_b = User.objects.create_user(username='userb', password='password')
        
        # User A logs in
        self.client.login(username='usera', password='password')
        
        # User A creates an expense directly in DB for testing edit/delete
        self.expense_a = Expense.objects.create(
            user=self.user_a,
            amount=100.00,
            description='Test Expense A',
            category='FOOD',
            date=datetime.date.today()
        )

    def test_expense_creation_view(self):
        # Test creating an expense via the view
        url = reverse('expenses:expense-add')
        data = {
            'amount': '50.00',
            'description': 'New Setup',
            'category': 'RENT',
            'date': datetime.date.today().isoformat()
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('expenses:expense-list'))
        
        # Check if saved to DB and user matches currently logged in user (User A)
        self.assertEqual(Expense.objects.filter(user=self.user_a).count(), 2)
        new_expense = Expense.objects.get(description='New Setup')
        self.assertEqual(new_expense.user, self.user_a)

    def test_data_isolation_list(self):
        # User B logs in
        self.client.logout()
        self.client.login(username='userb', password='password')
        
        url = reverse('expenses:expense-list')
        response = self.client.get(url)
        
        # User B should see 0 expenses
        self.assertQuerySetEqual(response.context['expenses'], [])

    def test_data_isolation_edit(self):
        # User B logs in and tries to edit User A's expense
        self.client.logout()
        self.client.login(username='userb', password='password')
        
        url = reverse('expenses:expense-edit', args=[self.expense_a.pk])
        response = self.client.get(url)
        
        # Should return 404 because get_queryset filters by self.request.user
        self.assertEqual(response.status_code, 404)

    def test_data_isolation_delete(self):
        # User B logs in and tries to delete User A's expense
        self.client.logout()
        self.client.login(username='userb', password='password')
        
        url = reverse('expenses:expense-delete', args=[self.expense_a.pk])
        response = self.client.post(url)
        
        # Should return 404
        self.assertEqual(response.status_code, 404)
        
        # Expense should still exist
        self.assertTrue(Expense.objects.filter(pk=self.expense_a.pk).exists())
