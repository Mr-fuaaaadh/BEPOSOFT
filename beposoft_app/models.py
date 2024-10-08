from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from .validators import validate_gst
import re
from django.core.exceptions import ValidationError
from decimal import Decimal
import random
# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta :
        db_table = "State"

class Departments(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        db_table = "Departments"

    def __str__(self):
        return self.name

class Supervisor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    class Meta:
        db_table = "Supervisor"

    def __str__(self):
        return self.name


class Family(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta :
        db_table = "Family"



class User(models.Model):

    eid = models.CharField(max_length=6, unique=True, editable=False)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True,null=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=100)
    alternate_number = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=100)
    image = models.ImageField(max_length=100, upload_to="staff_images/", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    allocated_states = models.ManyToManyField(State)
    gender = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=100, null=True, blank=True)
    driving_license = models.CharField(max_length=100, null=True, blank=True)
    driving_license_exp_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=100, null=True, blank=True) #(Full-time  Part-time Contract)
    designation = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=100, null=-True,blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    confirmation_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    supervisor_id = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True)
    signatur_up = models.ImageField(upload_to="signature/",max_length=100,null=True)
    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    approval_status = models.CharField(max_length=100, choices=APPROVAL_CHOICES, default='disapproved', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Handle password hashing
        if self.pk is None or 'password' in kwargs:  
            self.password = make_password(self.password)
        # Handle unique EID
        if not self.eid:
            self.eid = self.generate_unique_eid()
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generate_unique_eid(self):
        while True:
            eid = str(random.randint(100000, 999999))
            if not User.objects.filter(eid=eid).exists():
                return eid

    class Meta:
        db_table = "User"


class Attributes(models.Model):
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # ex COLOR SIZE 

    def __str__(self):
        return self.name

    class Meta:
        db_table = "attributes"


class ProductAttribute(models.Model):
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=255) #ex RED BLACK L M 

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

    class Meta:
        db_table = "product_attributes" 


class Customers(models.Model):
    gst = models.CharField(
        unique=True,
        max_length=15,
        null=True,
        blank=True,
        validators=[validate_gst],  
    )
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,unique=True)
    alt_phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100,unique=True)
    address = models.CharField(max_length=500,null=True)
    zip_code =models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    comment = models.CharField(max_length=500,null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    
    class Meta :
        db_table = "Customers"



class Shipping(models.Model):
    created_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    zipcode = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    class Meta :
        db_table = "Shipping_Address"

    def __str__(self):
        return self.name




class Products(models.Model):
    PRODUCT_TYPES = [
        ('single', 'Single'),
        ('variant', 'Variant'),
    ]
    
    UNIT_TYPES = [
        ('BOX', 'BOX'),
        ('NOS', 'NOS'),
        ('PRS', 'PRS'),
        ('SET', 'SET'),
        ('SET OF 12', 'SET OF 12'),
        ('SET OF 16', 'SET OF 16'),
        ('SET OF 6', 'SET OF 6'),
        ('SET OF 8', 'SET OF 8'),
    ]
    created_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=500)
    hsn_code = models.CharField(max_length=100)
    family = models.ManyToManyField(Family, related_name='products')
    type = models.CharField(max_length=100, choices=PRODUCT_TYPES, default='single')
    unit = models.CharField(max_length=100, choices=UNIT_TYPES, default="BOX")
    purchase_rate = models.FloatField()
    tax = models.FloatField() 
    exclude_price = models.FloatField(editable=False)  
    selling_price = models.FloatField(null=True)  

    def calculate_exclude_price(self):
        if self.selling_price is not None:
            self.exclude_price = self.selling_price / (1 + self.tax / 100)
        else:
            self.exclude_price = 0

    def save(self, *args, **kwargs):
        self.calculate_exclude_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SingleProducts(models.Model) :
    created_user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='single_products')
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')

    class Meta:
        db_table = "single_product"

    def __str__(self):
        return f"{self.product.name} - {self.price}"


class VariantProducts(models.Model):
    created_user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variant_products')
    name = models.CharField(max_length=100)
    stock = models.PositiveBigIntegerField(null=True)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='images/',null=True)

    class Meta :
        db_table = "variant_product"
    
    def __str__(self):
        return self.name





class Order(models.Model):
    COMPANY_CHOICES = [
        ('MICHEAL IMPORT EXPORT PVT LTD', 'MICHEAL IMPORT EXPORT PVT LTD'),
        ('BEPOSOFT PVT LTD', 'BEPOSOFT PVT  LTD'),
    ]

    manage_staff = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, choices=COMPANY_CHOICES, default='MICHEAL IMPORT EXPORT PVT LTD')
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=20, unique=True, blank=True)
    billing_address = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
        ('Return', 'Return'),
    ], default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Razorpay', 'Razorpay'),
        ('Net Banking', 'Net Banking'),
        ('Bank Transfer', 'Bank Transfer')
    ], default='Net Banking')

    def save(self, *args, **kwargs):
        if not self.invoice:
            self.invoice = self.generate_invoice_number()
            print(f"Generated invoice number: {self.invoice}")
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        prefix = ""
        if self.company == 'MICHEAL IMPORT EXPORT PVT LTD':
            prefix = "MI-"
        elif self.company == 'BEPOSOFT PVT LTD':
            prefix = "BR-"
        
        number = self.get_next_invoice_number(prefix)
        invoice_number = f"{prefix}{number}"
        print(f"Invoice number generated: {invoice_number}")
        return invoice_number

    def get_next_invoice_number(self, prefix):
        # Get the highest existing invoice number for the given prefix
        highest_invoice = Order.objects.filter(invoice__startswith=prefix).order_by('invoice').last()
        if highest_invoice:
            number = int(highest_invoice.invoice.split('-')[-1]) + 1
        else:
            number = 1
        return str(number).zfill(6)  # Zero-pad to 6 digits

    def __str__(self):
        return f"Order {self.invoice} by {self.customer}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # without GST
    tax = models.PositiveIntegerField()  # tax percentage
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False)  # taxable amount
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price per unit
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False)  # total cost

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.price

    def calculate_net_price(self):
        net_price = self.rate / (1 + Decimal(self.tax) / 100)
        return net_price

    def calculate_total(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        self.net_price = self.calculate_net_price()
        self.total = self.calculate_total()
        super().save(*args, **kwargs)



