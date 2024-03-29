from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinLengthValidator

STATE_CHOICES = (('Andaman & Nicobar Islands','Andaman & Nicobar Island'),
                 ('Andhra Pradesh', 'Andhra Pradesh'),
                 ('Arunachal Pradesh', 'Arunachal Pradesh'),
                 ('Assam', 'Assam'),
                 ('Bihar', 'Bihar'),
                 ('Chandigarh', 'Chandigarh'),
                 ('Chhattisgarh', 'Chhattisgarh'),
                 ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
                 ('Delhi', 'Delhi'),
                 ('Goa','Goa'),
                 ('Gujarat', 'Gujarat'),
                 ('Haryana', 'Haryana'),
                 ('Himachal Pradesh', 'Himachal Pradesh'),
                 ('Jammu and Kashmir', 'Jammu and Kashmir'),
                 ('Jharkhand', 'Jharkhand'),
                 ('Karnataka', 'Karnataka'),
                 ('Kerala', 'Kerala'),
                 ('Lakshadweep', 'Lakshadweep'),
                 ('Madhya Pradesh', 'Madhya Pradesh'),
                 ('Maharashtra', 'Maharashtra'),
                 ('Manipur', 'Manipur'),
                 ('Meghalaya', 'Meghalaya'),
                 ('Mizoram', 'Mizoram'),
                 ('Nagaland', 'Nagaland'),
                 ('Orissa', 'Orissa'),
                 ('Pondicherry', 'Pondicherry'),
                 ('Punjab', 'Punjab'),
                 ('Rajasthan', 'Rajasthan'),
                 ('Sikkim', 'Sikkim'),
                 ('Tamil Nadu', 'Tamil Nadu'),
                 ('Telangana', 'Telangana'),
                 ('Tripura', 'Tripura'),
                 ('Uttaranchal', 'Uttaranchal'),
                 ('Uttar Pradesh', 'Uttar Pradesh'),
                 ('West Bengal', 'West Bengal'))


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self) -> str:
        return str(self.id)
    

CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(blank=True,null=True)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self) -> str:
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

