from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
def unique_slugify(instance, slug):
        model = instance.__class__
        unique_slug = slug
        record_count = 0
        while model.objects.filter(slug=unique_slug).exists():
            unique_slug = slug + "-1"
            while model.objects.filter(slug=unique_slug).exists():
                record_count = record_count + 1
                unique_slug = slug + "-" + str(record_count)
        return unique_slug

class Category(models.Model):
    slug = models.SlugField(max_length=100, 
                            null=False, blank=False, 
                            editable=False, 
                            allow_unicode=True)  
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add =True)

    class Meta:
        db_table ='inventory_category'
        verbose_name_plural ='categories'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = slugify(f'category-{self.name}')
            self.slug = unique_slugify(self, slug_text)
        super().save(*args, **kwargs)

class Product(models.Model):
    slug = models.SlugField(max_length=100, 
                            null=False, blank=False, 
                            editable=False, 
                            allow_unicode=True)  
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add =True)

    class Meta:
        db_table ='inventory_product'
        verbose_name_plural ='products'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = slugify(f'product-{self.name}')
            self.slug = unique_slugify(self, slug_text)
        super().save(*args, **kwargs)

class Order(models.Model):
    slug = models.SlugField(max_length=100, 
                            null=False, blank=False, 
                            editable=False, 
                            allow_unicode=True)  
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_created = models.DateTimeField(auto_now_add =True)

    class Meta:
        db_table ='inventory_order'
        verbose_name_plural ='orders'
    def __str__(self):
        return f'order-for{self.products.name}'
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = slugify(f'Order-from-{self.order.user.name}')
            self.slug = unique_slugify(self, slug_text)
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    slug = models.SlugField(max_length=100, 
                            null=False, blank=False, 
                            editable=False, 
                            allow_unicode=True)  
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add =True)

    class Meta:
        db_table ='inventory_order_item'
        verbose_name_plural ='order_items'
    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = slugify(f'Order-item-for{self.order.user.name}')
            self.slug = unique_slugify(self, slug_text)
        super().save(*args, **kwargs)