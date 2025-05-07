from django.db import models



class Owner(models.Model):
    LICENSE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('revoked', 'Revoked'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending'),
    ]
    
    full_legal_name = models.CharField(max_length=255)  # Not making it unique at DB level
    contact_number = models.CharField(max_length=20)
    license_status = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES, default='pending')
    registration_date = models.DateField()
    age = models.PositiveIntegerField()
    residential_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['full_legal_name'],
                name='unique_owner_name',
                condition=models.Q(full_legal_name__isnull=False),
            ),
        ]

    def __str__(self):
        return self.full_legal_name
class Firearm(models.Model):
    GUN_TYPE_CHOICES = [
        ('handgun', 'Handgun'),
        ('rifle', 'Rifle'),
        ('shotgun', 'Shotgun'),
        ('submachine', 'Submachine Gun'),
        ('other', 'Other'),
    ]
    
    FIREARM_STATUS_CHOICES = [
        ('deposit', 'Deposit'),
        ('confiscated', 'Confiscated'),
        ('surrendered', 'Surrendered'),
        ('abandoned', 'Abandoned'),
    ]
    
    # Change this line to make serial_number the primary key
    serial_number = models.CharField(max_length=100, primary_key=True, unique=True)
    gun_model = models.CharField(max_length=255)
    gun_type = models.CharField(max_length=20, choices=GUN_TYPE_CHOICES)
    ammunition_type = models.CharField(max_length=100)
    firearm_status = models.CharField(max_length=20, choices=FIREARM_STATUS_CHOICES)
    date_of_collection = models.DateField()
    registration_location = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='firearms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gun_model} ({self.serial_number})"