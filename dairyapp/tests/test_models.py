from django.test import TestCase
from dairyapp.models import *
from my_account.models import User

class DairyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            first_name='john',
            last_name='doe',
            phone_number='9864778987',
            password='johndoe'
        )
        self.user1 = User.objects.create_user(
            email='johndoe1@gmail.com',
            first_name='john1',
            last_name='doe',
            phone_number='9864778999',
            password='johndoe'
        )
        self.user2 = User.objects.create_user(
            email='johndoe2@gmail.com',
            first_name='john2',
            last_name='doe',
            phone_number='9864778944',
            password='johndoe'
        )

    def test_dairy_create(self):
        dairy = Dairy.objects.create(
            name='john dairy',
            user=self.user,
            location='shera',

        )
        self.assertEqual(dairy.name,'john dairy')
        self.assertEqual(dairy.user,self.user)
        self.assertEqual(dairy.location,'shera')

    def test_dairy_create_with_members(self):
        dairy = Dairy.objects.create(
            name='john dairy',
            user=self.user,
            location='shera',

        )
        #set dairy members
        dairy.members.set([self.user,self.user1,self.user2])
        
        self.assertEqual(dairy.name,'john dairy')
        self.assertEqual(dairy.user,self.user)
        self.assertEqual(dairy.location,'shera')
        self.assertEqual(dairy.members.all().count(),3)

        #remove dairy member
        dairy.members.remove(self.user2)
        self.assertEqual(dairy.members.all().count(),2)

        #remove all members
        dairy.members.clear()
        self.assertEqual(dairy.members.all().count(),0)

    def test_dairy_model_manager(self):
        dairy = Dairy.objects.create(
            name='john dairy',
            user=self.user,
            location='shera',
            is_verified=True

        )

        dairy1 = Dairy.objects.create(
            name='john dairy 1',
            user=self.user,
            location='nala',
            is_verified=True

        )

        dairy2 = Dairy.objects.create(
            name='john dairy 2',
            user=self.user,
            location='banepa',

        )

        #check if verified dairy count is exactly 2
        self.assertEqual(Dairy.verObs.all().count(),2)

        #check if number of inserted dairy is equal to 3
        self.assertEqual(Dairy.objects.all().count(),3)


class CommonTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            first_name='john',
            last_name='doe',
            phone_number='9864778987',
            password='johndoe'
        )

        self.dairy = Dairy.objects.create(
            name='john dairy',
            user=self.user,
            location='shera',
            is_verified=True

        )


class FatRateTestCase(CommonTestCase):
    
    def test_fatrate_create(self):
        fatrate = FatRate.objects.create(
            fat_rate=18,
            dairy=self.dairy,

        )

        self.assertEqual(fatrate.fat_rate,18)
        self.assertEqual(fatrate.dairy,self.dairy)
        self.assertEqual(fatrate.get_fat_rate,18)

        fatrate.bonous_amount = 2
        fatrate.save()

        self.assertEqual(fatrate.get_fat_rate,20)

class MilkRecordTestCase(CommonTestCase):
    

    def test_create_milk_record(self):
        milkrecord = MilkRecord.objects.create(
            dairy=self.dairy,
            user=self.user,
            milk_weight=20,
            milk_fat=4,
            shift='night',
            date='2023-09-03'
        )

        self.assertEqual(milkrecord.dairy,self.dairy)
        self.assertEqual(milkrecord.user,self.user)
        self.assertEqual(milkrecord.milk_weight,20)
        self.assertEqual(milkrecord.milk_fat,4)
        self.assertEqual(milkrecord.shift,'night')
        self.assertEqual(milkrecord.date,'2023-09-03')





        




