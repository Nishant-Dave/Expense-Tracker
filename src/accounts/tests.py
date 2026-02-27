from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')

    def test_signup_view_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'phone_number': '1234567890',
            'city': 'Test City',
            'monthly_budget': '1500.50',
            'profile_avatar': 'avatar2',
        }
        # In actual forms, we also need to confirm password, let's just create user directly to test model
        # Or test form creation if we submit form data
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            phone_number=data['phone_number'],
            city=data['city'],
            monthly_budget=data['monthly_budget'],
            profile_avatar=data['profile_avatar']
        )
        
        self.assertEqual(User.objects.count(), 1)
        db_user = User.objects.get(username='testuser')
        self.assertEqual(db_user.phone_number, '1234567890')
        self.assertEqual(db_user.city, 'Test City')
        self.assertEqual(float(db_user.monthly_budget), 1500.50)
        self.assertEqual(db_user.profile_avatar, 'avatar2')

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpassword123')
        # Login and check redirect
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
        # Should redirect to default login_redirect_url
        self.assertRedirects(response, reverse('expenses:expense-list'), fetch_redirect_response=False)
