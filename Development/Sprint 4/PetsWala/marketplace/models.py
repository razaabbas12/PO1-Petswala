from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from accounts.models import Vendor, User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null = True, blank = True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=False)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product=models.ForeignKey(Product,models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Started", "Started"),
    ("Abanodned", "Abandoned"),
    ("Finished", "Finished"),
)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', models.CASCADE, null = True, blank = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=1)
    vendor = models.CharField(max_length=255, default='ABC')
    quantity = models.IntegerField(default = 1)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    line_total = models.DecimalField(default = 0.0, max_digits = 1000, decimal_places = 2, null = True, blank = True)
    status = models.CharField(max_length = 120, choices = STATUS_CHOICES, default = "Pending")

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title

    @property
    def line_total(self):
        line_total = float(self.product.price) * float(self.quantity)
        return round(line_total, 2)

class Cart(models.Model):
    # user = models.ForeignKey(User, models.CASCADE)
    total = models.DecimalField(max_digits = 100, decimal_places = 2, default = 0.0)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    active = models.BooleanField(default = True)

    def __str__(self):
        return "Cart id: %s" %(self.id)


class Order(models.Model):
    user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
    address = models.CharField(max_length = 120, default = '{user.address}')
    city = models.CharField(max_length = 50, default = 'ABC')
    sub_total = models.DecimalField(default = 0.0, max_digits = 1000, decimal_places = 2, null = True, blank = True)
    final_total = models.DecimalField(default = 0.0, max_digits = 1000, decimal_places = 2, null = True, blank = True)
    tax_total = models.DecimalField(default = 0.0, max_digits = 1000, decimal_places = 2, null = True, blank = True)
    order_id = models.CharField(max_length = 120, default = 'ABC')
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = "Started")
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return self.order_id

    @property
    def final_total(self):
        return float(self.sub_total) + float(self.tax_total)
