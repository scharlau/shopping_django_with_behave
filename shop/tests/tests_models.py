from django.test import Client, TestCase
from django.urls import reverse
from shop.models import Product

# Create your tests here.
# use the line below for debugging so that you can see what is on the page
#  print(response.content)

class ShopModelTests(TestCase):
        @classmethod
        def setUpTestData(cls):
            # set up test data in database
            Product.objects.create(name = "Acme Toaster", price= 23.99)
            Product.objects.create(name = "Acme Stool", price= 3.99)
        
        def test_product(self):
            products = Product.objects.all()
            self.assertEqual(products.count(), 2)
            product = Product.objects.get(id=1)
            self.assertEqual(product.name, "Acme Toaster")
    
