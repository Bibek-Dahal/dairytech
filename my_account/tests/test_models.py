from django.test import TestCase
from my_account.models import User
# from my_account.models import User
from my_account.models import User

class TestUserModel(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='johndoe@gmail.com',
            first_name='john',
            last_name='doe',
            phone_number='9864778987',
            password='johndoe'
        )

    def test_user_create(self):
        self.assertEqual(self.user.email, 'johndoe@gmail.com')
        self.assertEqual(self.user.first_name, 'john')
        self.assertEqual(self.user.last_name, 'doe')
        self.assertEqual(self.user.phone_number, '9864778987')
        self.assertTrue(self.user.check_password('johndoe'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_get_name(self):
        self.assertEqual(self.user.get_name(), 'john doe')

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@gmail.com',
            first_name='admin',
            last_name='doe',
            phone_number='9864778998',
            password='admindoe',
            middle_name='prasad'
        )

        self.assertEqual(user.email, 'admin@gmail.com')
        self.assertEqual(user.first_name, 'admin')
        self.assertEqual(user.middle_name, 'prasad')
        self.assertEqual(user.last_name, 'doe')
        self.assertEqual(user.phone_number, '9864778998')
        self.assertTrue(user.check_password('admindoe'))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        self.assertEqual(user.get_name(),'admin prasad doe')

    def test_check_duplicate_user(self):
        
        with self.assertRaisesMessage(ValueError,'User with email or phone number already exists.'):
            User.objects.create_user(
                email='johndoe@gmail.com',
                first_name='john',
                last_name='doe',
                phone_number='9864778987',
                password='johndoe'
        )
    
    def test_check_craete_user_withot_email(self):
        
        with self.assertRaisesMessage(ValueError,'User must have email set.'):
            User.objects.create_user(
                first_name='john',
                email='',
                last_name='doe',
                phone_number='9864778987',
                password='johndoe'
        )

        # self.assertRaises(ValueError,'User with email or phone number already exists.')
    def test_check_craete_user_without_phone_number(self):
        
        with self.assertRaisesMessage(ValueError,'User must have phone number set.'):
            User.objects.create_user(
                first_name='john',
                email='johndoe@gmail.com',
                last_name='doe',
                phone_number='',
                password='johndoe'
        )
    
    def test_check_craete_user_without_first_name(self):
        
        with self.assertRaisesMessage(ValueError,'User must have first name set.'):
            User.objects.create_user(
                first_name='',
                email='johndoe@gmail.com',
                last_name='doe',
                phone_number='9864778987',
                password='johndoe'
        )
    
    def test_check_craete_user_without_last_name(self):
        
        with self.assertRaisesMessage(ValueError,'User must have last name set.'):
            User.objects.create_user(
                first_name='john',
                email='johndoe@gmail.com',
                last_name='',
                phone_number='9864778987',
                password='johndoe'
        )
            