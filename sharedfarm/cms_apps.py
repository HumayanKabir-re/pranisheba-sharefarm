from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from aldryn_apphooks_config.app_base import CMSConfigApp
from django.utils.translation import gettext_lazy as _
from .cms_appconfig import SharedFarmConfig


@apphook_pool.register  # register the application
class SharedFarmApp(CMSConfigApp):
    app_name = "sharedfarm"
    name = "Shared Farm Application"
    app_config = SharedFarmConfig

    def get_urls(self, page=None, language=None, **kwargs):
        return ["sharedfarm.urls"]
