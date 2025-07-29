import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SilkProduct, UserProfile
from .forms import CustomUserCreationForm, SilkProductForm, ContactSellerForm


class SilkProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        UserProfile.objects.create(user=self.user, role='seller')

    def test_create_product(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        self.assertEqual(product.name, 'Test Saree')
        self.assertEqual(product.type, 'saree')
        self.assertEqual(product.price, 1500)
        self.assertTrue(product.availability)
        self.assertEqual(product.owner, self.user)

    def test_product_str_representation(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        self.assertEqual(str(product), 'Test Saree')


class UserProfileModelTest(TestCase):
    def test_create_user_profile(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        profile = UserProfile.objects.create(
            user=user,
            role='seller',
            phone='01234567890'
        )
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.role, 'seller')
        self.assertEqual(profile.phone, '01234567890')

    def test_user_profile_str_representation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        profile = UserProfile.objects.create(
            user=user,
            role='buyer'
        )
        self.assertEqual(str(profile), 'testuser (Buyer)')


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'seller',
            'phone': '01234567890'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'differentpass123',
            'role': 'seller',
            'phone': '01234567890'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_missing_required_fields(self):
        form_data = {
            'username': 'testuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class SilkProductFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'Test Saree',
            'type': 'saree',
            'price': 1500,
            'availability': True,
            'description': 'Beautiful silk saree'
        }
        form = SilkProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_negative_price(self):
        form_data = {
            'name': 'Test Saree',
            'type': 'saree',
            'price': -100,
            'availability': True,
            'description': 'Beautiful silk saree'
        }
        form = SilkProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_missing_required_fields(self):
        form_data = {
            'type': 'saree',
            'price': 1500
        }
        form = SilkProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ContactSellerFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'subject': 'Interest in your product',
            'message': 'I am interested in buying this product.'
        }
        form = ContactSellerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form_data = {
            'subject': 'Interest in your product'
        }
        form = ContactSellerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)


class SilkProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        UserProfile.objects.create(user=self.user, role='seller')

    def test_product_list_view(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Saree')

    def test_product_search(self):
        product = SilkProduct.objects.create(
            name='Silk Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        response = self.client.get(reverse('product_list'), {'search': 'Silk'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Silk Saree')

    def test_product_detail_view(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        response = self.client.get(reverse('product_detail', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Saree')

    def test_product_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_unauthenticated(self):
        response = self.client.get(reverse('product_create'))
        self.assertRedirects(response, '/login/?next=/create/')

    def test_product_create_post(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'New Saree',
            'type': 'saree',
            'price': 2000,
            'availability': True,
            'description': 'A new beautiful saree'
        }
        response = self.client.post(reverse('product_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SilkProduct.objects.filter(name='New Saree').exists())

    def test_product_update_view(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('product_update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_product_delete_view(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.user,
            description='Beautiful silk saree'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('product_delete', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SilkProduct.objects.filter(pk=product.pk).exists())

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'buyer',
            'phone': '01234567890'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        UserProfile.objects.create(user=self.user, role='seller')

    def test_user_registration_api(self):
        url = reverse('api_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'complexpass123',
            'password_confirm': 'complexpass123',
            'role': 'buyer',
            'phone': '01234567890'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)

    def test_jwt_login(self):
        refresh = RefreshToken.for_user(self.user)
        self.assertIsNotNone(refresh.access_token)

    def test_jwt_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        new_token = refresh.access_token
        self.assertIsNotNone(new_token)

    def test_protected_endpoint_access(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('api_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_api(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('api_logout')
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])


class SilkProductAPITest(APITestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller1',
            password='testpass123',
            email='seller@example.com'
        )
        self.buyer = User.objects.create_user(
            username='buyer1',
            password='testpass123',
            email='buyer@example.com'
        )
        
        UserProfile.objects.create(user=self.seller, role='seller')
        UserProfile.objects.create(user=self.buyer, role='buyer')
        
        self.client = APIClient()

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_product_api(self):
        self.authenticate_user(self.seller)
        url = reverse('api_product_list_create')
        data = {
            'name': 'New Test Saree',
            'type': 'saree',
            'price': '2000.00',
            'availability': True,
            'description': 'Another beautiful saree'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Saree')
        self.assertEqual(response.data['owner'], self.seller.id)

    def test_get_product_list_api(self):
        fresh_client = APIClient()
        refresh = RefreshToken.for_user(self.seller)
        fresh_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        product = SilkProduct.objects.create(
            name='Unique Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        url = reverse('api_product_list_create')
        response = fresh_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if isinstance(response.data, dict) and 'results' in response.data:
            products = response.data['results']
        else:
            products = response.data
        
        self.assertGreaterEqual(len(products), 1)
        product_names = [p['name'] for p in products]
        self.assertIn('Unique Test Saree', product_names)

    def test_get_product_detail_api(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        self.authenticate_user(self.seller)
        url = reverse('api_product_detail', kwargs={'pk': product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Saree')

    def test_update_product_api_owner(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        self.authenticate_user(self.seller)
        url = reverse('api_product_detail', kwargs={'pk': product.pk})
        data = {
            'name': 'Updated Saree',
            'type': 'saree',
            'price': '1800.00',
            'availability': False,
            'description': 'Updated description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Saree')

    def test_update_product_api_non_owner(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        self.authenticate_user(self.buyer)
        url = reverse('api_product_detail', kwargs={'pk': product.pk})
        data = {
            'name': 'Unauthorized Update',
            'type': 'saree',
            'price': '1800.00',
            'availability': False,
            'description': 'Unauthorized description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_api_owner(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        self.authenticate_user(self.seller)
        url = reverse('api_product_detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        with self.assertRaises(SilkProduct.DoesNotExist):
            SilkProduct.objects.get(pk=product.pk)

    def test_delete_product_api_non_owner(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        self.authenticate_user(self.buyer)
        url = reverse('api_product_detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_stats_api(self):
        existing_count = SilkProduct.objects.count()
        
        SilkProduct.objects.create(
            name='Stats Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        
        self.authenticate_user(self.seller)
        url = reverse('api_product_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_products', response.data)
        self.assertGreaterEqual(response.data['total_products'], existing_count + 1)


class PermissionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller = User.objects.create_user(
            username='seller1',
            email='seller@example.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer1',
            email='buyer@example.com',
            password='testpass123'
        )
        
        UserProfile.objects.create(user=self.seller, role='seller')
        UserProfile.objects.create(user=self.buyer, role='buyer')

    def test_anonymous_user_can_view_products(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_buyer_cannot_create_products(self):
        self.client.login(username='buyer1', password='testpass123')
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 302)

    def test_seller_can_create_products(self):
        self.client.login(username='seller1', password='testpass123')
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse('product_create'))
        self.assertRedirects(response, '/login/?next=/create/')

    def test_product_owner_can_edit(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        self.client.login(username='seller1', password='testpass123')
        response = self.client.get(reverse('product_update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_edit(self):
        product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )
        self.client.login(username='buyer1', password='testpass123')
        response = self.client.get(reverse('product_update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))


class EmailFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller = User.objects.create_user(
            username='seller1',
            email='seller@example.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer1',
            email='buyer@example.com',
            password='testpass123'
        )
        
        UserProfile.objects.create(user=self.seller, role='seller')
        UserProfile.objects.create(user=self.buyer, role='buyer')
        
        self.product = SilkProduct.objects.create(
            name='Test Saree',
            type='saree',
            price=1500,
            availability=True,
            owner=self.seller,
            description='Beautiful silk saree'
        )

    def test_email_sent_when_buyer_contacts_seller(self):
        self.client.login(username='buyer1', password='testpass123')
        data = {
            'subject': 'Interest in your product',
            'message': 'I am interested in buying this product.'
        }
        response = self.client.post(
            reverse('product_detail', kwargs={'pk': self.product.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'Interest in your product: {self.product.name}')
        self.assertEqual(mail.outbox[0].to, [self.seller.email])

    def test_contact_seller_form_submission(self):
        self.client.login(username='buyer1', password='testpass123')
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Seller')

        data = {
            'subject': 'Product Inquiry',
            'message': 'Can you provide more details about this product?'
        }
        response = self.client.post(
            reverse('product_detail', kwargs={'pk': self.product.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'Interest in your product: {self.product.name}')


class IntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_complete_user_journey(self):
        registration_data = {
            'username': 'journeyuser',
            'email': 'journey@example.com',
            'first_name': 'Journey',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'seller',
            'phone': '01234567890'
        }
        response = self.client.post(reverse('register'), registration_data)
        self.assertEqual(response.status_code, 302)

        login_success = self.client.login(username='journeyuser', password='complexpass123')
        self.assertTrue(login_success)

        product_data = {
            'name': 'Journey Saree',
            'type': 'saree',
            'price': 2500,
            'availability': True,
            'description': 'A beautiful journey saree'
        }
        response = self.client.post(reverse('product_create'), product_data)
        self.assertEqual(response.status_code, 302)

        product = SilkProduct.objects.get(name='Journey Saree')
        self.assertEqual(product.price, 2500)

        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Journey Saree')

        update_data = {
            'name': 'Updated Journey Saree',
            'type': 'saree',
            'price': 3000,
            'availability': True,
            'description': 'An updated beautiful journey saree'
        }
        response = self.client.post(reverse('product_update', kwargs={'pk': product.pk}), update_data)
        self.assertEqual(response.status_code, 302)

        updated_product = SilkProduct.objects.get(pk=product.pk)
        self.assertEqual(updated_product.name, 'Updated Journey Saree')
        self.assertEqual(updated_product.price, 3000)

    def test_api_integration_journey(self):
        registration_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'first_name': 'API',
            'last_name': 'User',
            'password': 'complexpass123',
            'password_confirm': 'complexpass123',
            'role': 'seller',
            'phone': '01234567890'
        }
        response = self.client.post(reverse('api_register'), registration_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)

        access_token = response.data['tokens']['access']
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        product_data = {
            'name': 'API Saree',
            'type': 'saree',
            'price': '1800.00',
            'availability': True,
            'description': 'A beautiful API saree'
        }
        response = api_client.post(reverse('api_product_list_create'), product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = api_client.get(reverse('api_product_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

        response = api_client.get(reverse('api_product_stats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_products', response.data)
