from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import index, shopPage, genderFilterPage
class TestUrls(SimpleTestCase):
    

    def test_index_url_is_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func,index)