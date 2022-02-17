from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from .models import Product
from cms.utils.urlutils import admin_reverse


class SharedFarmToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'sharedfarm_cms_integration-products',  # a unique key for this menu
            'SharedFarm',  # the text that should appear in the menu
        )
        menu.add_sideframe_item(
            name='Farm list',  # name of the new menu item
            url=admin_reverse('sharedfarm_product_changelist'),  # the URL it should open with
        )
        menu.add_modal_item(
            name='Add a new farm',                # name of the new menu item
            url=admin_reverse('sharedfarm_product_add'),  # the URL it should open with
        )
        # menu.add_modal_item(
        #     name='Add a new farm',                # name of the new menu item
        #     url=admin_reverse('sharedfarm_product_add'),  # the URL it should open with
        # )


# register the toolbar
toolbar_pool.register(SharedFarmToolbar)
