from django.test import TestCase
from .models import Owner, Firearm
from django.utils import timezone

class FirearmRegistryTests(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            name="John Doe",
            contact="+1234567890",
            license_status="active",
            registered_date="2023-01-01",
            age=30,
            address="123 Main St"
        )
        
        self.firearm = Firearm.objects.create(
            owner=self.owner,
            serial_number="ABC123",
            gun_name="Glock 19",
            gun_type="handgun",
            ammo_type="9mm",
            status="deposit",
            date="2023-01-15",
            location="Police Station 1"
        )
    
    def test_owner_creation(self):
        self.assertEqual(self.owner.name, "John Doe")
        self.assertEqual(self.owner.contact, "+1234567890")
        self.assertEqual(self.owner.license_status, "active")
    
    def test_firearm_creation(self):
        self.assertEqual(self.firearm.serial_number, "ABC123")
        self.assertEqual(self.firearm.gun_name, "Glock 19")
        self.assertEqual(self.firearm.gun_type, "handgun")
        self.assertEqual(self.firearm.owner.name, "John Doe")
    
    def test_unique_serial_number(self):
        with self.assertRaises(Exception):
            Firearm.objects.create(
                owner=self.owner,
                serial_number="ABC123",  # Duplicate
                gun_name="Another Gun",
                gun_type="rifle",
                ammo_type=".308",
                status="confiscated",
                date="2023-02-01",
                location="Police Station 2"
            )
    
    def test_minimum_age(self):
        with self.assertRaises(Exception):
            Owner.objects.create(
                name="Young Owner",
                contact="+0987654321",
                license_status="pending",
                registered_date="2023-01-01",
                age=17,  # Below minimum
                address="456 Oak St"
            )