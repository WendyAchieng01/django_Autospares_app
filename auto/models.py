from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField, ValidationError
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='category_images/', default='category_images/default_category_image.jpg')

    def __str__(self):
        return self.name

    def product_count(self):
        return self.product_set.count()

class Brand(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='brand_images/', default='brand_images/default_brand_image.jpg')

    def __str__(self):
        return self.name

    def product_count(self):
        return self.product_set.count()
    
class Accessories(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Untitled Accessories"
    
    def product_count(self):
        return self.product_set.count()

class Product(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='product_images/')
    desc = models.TextField()
    specification = models.TextField(blank=True, null=True, default='No specifications available')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE, blank=True, null=True)
    offer = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.offer and not self.sale_price:
            raise ValidationError('Sale price is required when offer is True')
        elif not self.offer and self.sale_price:
            self.sale_price = None  # Clear the sale price if offer is False

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Product)
def resize_product_image(sender, instance, **kwargs):
    if instance.img:
        image = ImageField.open(instance.img)
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        max_size = (300, 300)  # Adjust the size according to your requirements

        # Check if the image dimensions are larger than max_size
        if image.width > max_size[0] or image.height > max_size[1]:
            # Resize the image
            image.thumbnail(max_size, Image.ANTIALIAS)

        else:
            # Enlarge the image to max_size
            image = image.resize(max_size)

        # Save the resized/enlarged image back to the same field
        img_io = BytesIO()
        image.save(img_io, format='JPEG')  # You can change the format if needed
        instance.img = InMemoryUploadedFile(
            img_io,
            None,
            instance.img.name,
            'image/jpeg',  # Change the content type if needed
            img_io.tell,
            None
        )
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    county = models.CharField(max_length=200, null=True, default='')
    zipcode = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phonenumber = models.CharField(max_length=20)
    note = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist for {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    county = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

#Automat the profile thing
post_save.connect(create_profile, sender=User)    
