from django.test import TestCase

from .models import MenuItem, PageLink


class TestMenuItemAndPageLinkModels(TestCase):
    def setUp(self):
        self.menu_item_title = "Test title"
        self.menu_item_obj = MenuItem.objects.create(title=self.menu_item_title)

        self.page_link_title = "Test link"
        self.page_link_obj = PageLink.objects.create(
            title=self.page_link_title, menu_item=self.menu_item_obj, url="https://ramiboutas.com/"
        )

    def test_dunder_str_of_menu_item(self):
        self.assertEqual(str(self.menu_item_obj), self.menu_item_title)

    def test_dunder_str_of_page_link(self):
        self.assertEqual(str(self.page_link_obj), self.page_link_title)
