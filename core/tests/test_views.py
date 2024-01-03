from django.test import TestCase, Client
from django.urls import reverse
from core.models import Product, ProductImage, ProductReview

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.shop_page = reverse('shop-page')
        self.product = Product.objects.create(name="car",
                               price=3.4,
                                 description="very nice",
                                  gender="M",
                                   sale_type= "lX",
                                    accessory_type= "Bag",
                                     colour="Blue",
                                      size="S",
                                       tags="bnmn" )

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_shop_page_GET(self):
        response = self.client.get(self.index_url)
        print(self.product)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
