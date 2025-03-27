from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    contact=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200, null=True)
    userpic=models.ImageField(blank=True, null=True)
    regdate=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    
class Volunteer(models.Model):
    
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    contact=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200, null=True)
    userpic=models.ImageField(blank=True,null=True)
    idpic=models.ImageField(blank=True, null=True)
    aboutme=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=20,null=True)
    regdate=models.DateTimeField(auto_now_add=True)
    adminremark=models.CharField(max_length=200,null=True)
    updationdate=models.DateField(null=True)


    def __str__(self):
        return self.user.username
    
class DonationArea(models.Model):
    arename=models.CharField(max_length=200, null=True)
    description=models.TextField()
    creationdate=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.arename
    
    
class Donation(models.Model):
    DONATION_CHOICES = (
        ('FOOD DONATION', 'FOOD DONATION'),
        ('CLOTHES DONATION', 'CLOTHES DONATION'),
        ('FOOTWEAR DONATION', 'FOOTWEAR DONATION'),
        ('BOOKS DONATION', 'BOOKS DONATION'),
        ('FOOD DONATION', 'FOOD DONATION'),
        ('FURNITURE DONATION', 'FURNITURE DONATION'),
        ('VESSEL DONATION', 'VESSEL DONATION'),
        ('OTHER DONATION', 'OTHER DONATION')
    )
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donationname = models.CharField(choices=DONATION_CHOICES, max_length=200, null=True)
    donationpic = models.ImageField(null=True, blank=True)
    collectionloc = models.CharField(max_length=200, null=True)
    description = models.TextField()
    status = models.CharField(max_length=200, default='pending')
    donationdate = models.DateField(null=True)
    adminremark = models.CharField(max_length=200, null=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True, blank=True)
    donationarea = models.ForeignKey(DonationArea, on_delete=models.CASCADE, blank=True, null=True)
    volunteerremark = models.CharField(max_length=200, null=True)
    updationdate = models.DateField(null=True)

    def __str__(self):
        # Return a more meaningful string representation
        return f"{self.donationname} by {self.donor} on {self.donationdate}"  # Example of more descriptive string


#### 2. **Gallarey Model**:


class Gallarey(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    deliverypic = models.FileField(null=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return a more meaningful string representation
        return f"Gallery for {self.donation.donationname} created on {self.creationdate}"


    




