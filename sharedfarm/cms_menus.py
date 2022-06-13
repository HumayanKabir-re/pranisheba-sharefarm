from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import get_language_from_request, gettext_lazy as _
from cms.menu_bases import CMSAttachMenu
from menus.base import Modifier
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


class TestMenu(CMSAttachMenu):
    name = _("SharedFarm Menu")

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        current_site = get_current_site(request)

        page_site = self.instance.node.site
        if self.instance and page_site != current_site:
            return []
        if language == "en":
            if(request.user.is_authenticated):  #NEW added logic to check if Logged In and should go to Farms - 13/03/2022
                n = NavigationNode(_('For Investors'), "/sharedfarm/#farms", 2, attr={'visible_for_anonymous': True})
            if not (request.user.is_authenticated):
                n = NavigationNode(_('For Investors'), "/sharedfarm/", 2, attr={'visible_for_anonymous': True})
            n2 = NavigationNode(_('For Farmers'), "https://pranisheba.com.bd/eng", 3,
                                attr={'visible_for_anonymous': True})
            # n3 = NavigationNode(_('For Investors'), "/investors/", 3, 1)
            n4 = NavigationNode(_('For Customers'), "https://pranishebashop.com.bd/", 4,
                                attr={'visible_for_anonymous': True})
        else:
            n = NavigationNode(_('বিনিয়োগকারীদের জন্য'), "/sharedfarm/", 2, attr={'visible_for_anonymous': True})
            n2 = NavigationNode(_('কৃষকদের জন্য'), "https://pranisheba.com.bd/eng", 3,
                                attr={'visible_for_anonymous': True})
            # n3 = NavigationNode(_('For Investors'), "/investors/", 3, 1)
            n4 = NavigationNode(_('গ্রাহকদের জন্য'), "https://pranishebashop.com.bd/", 4,
                                attr={'visible_for_anonymous': True})
        nodes.append(n)
        nodes.append(n2)
        # nodes.append(n3)
        nodes.append(n4)
        return nodes


class AboutUsMenu(CMSAttachMenu):
    name = _("AboutUs Menu")

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        current_site = get_current_site(request)
        page_site = self.instance.node.site
        if self.instance and page_site != current_site:
            return []
        if language == "en":
            n = NavigationNode(_('Our Services'), "/#our-services", 15, attr={'visible_for_anonymous': True})

            n1 = NavigationNode(_('Our Company'), "/#our-company", 16, attr={'visible_for_anonymous': True})
            n2 = NavigationNode(_('Our Technology'), "/#technology", 17,
                                attr={'visible_for_anonymous': True})
            n3 = NavigationNode(_('Our Leadership'), "/about-us/", 18, attr={'visible_for_anonymous': True})
            n4 = NavigationNode(_('How Jouthokhamar Works'), "/#how-we-works", 19,
                                attr={'visible_for_anonymous': True})
            n5 = NavigationNode(_('Get a Brochure'), "/#brochure", 20,
                                attr={'visible_for_anonymous': True})
            n6 = NavigationNode(_('Discover Our Company'), "/#discover-our-company", 21,
                                attr={'visible_for_anonymous': True})
            n7 = NavigationNode(_('Testimonials'), "/#testimonials", 22,
                                attr={'visible_for_anonymous': True})
        else:
            n = NavigationNode(_('আমাদের সেবাসমূহ'), "/#our-services", 15, attr={'visible_for_anonymous': True})

            n1 = NavigationNode(_('আমাদের প্রতিষ্ঠান'), "/#our-company", 16, attr={'visible_for_anonymous': True})
            n2 = NavigationNode(_('আমাদের প্রযুক্তি'), "/#technology", 17,
                                attr={'visible_for_anonymous': True})
            n3 = NavigationNode(_('আমাদের নেতৃত্ব'), "/about-us/", 18, attr={'visible_for_anonymous': True})
            n4 = NavigationNode(_('কিভাবে যৌথখামার কাজ করে'), "/#how-we-works", 19,
                                attr={'visible_for_anonymous': True})
            n5 = NavigationNode(_('ইস্তাহার ডাউনলোড করুন'), "/#brochure", 20,
                                attr={'visible_for_anonymous': True})
            n6 = NavigationNode(_('কোম্পানি সম্পর্কে আরো জানুন'), "/#discover-our-company", 21,
                                attr={'visible_for_anonymous': True})
            n7 = NavigationNode(_('প্রশংসাপত্র'), "/#testimonials", 22,
                                attr={'visible_for_anonymous': True})
        nodes.append(n)
        nodes.append(n1)
        nodes.append(n2)
        nodes.append(n3)
        nodes.append(n4)
        nodes.append(n5)
        nodes.append(n6)
        nodes.append(n7)
        return nodes


from django.urls import reverse


class UserMenu(Menu):
    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)

        if language == "en":
            n = NavigationNode(_("profile"), reverse('core:profile'), 10, attr={'visible_for_anonymous': False})
            n1 = NavigationNode(_("My profile"), reverse('core:profile'), 11, 10,
                                attr={'visible_for_anonymous': False})
            n2 = NavigationNode(_("My Farms"), reverse('core:my_farms'), 12, 10, attr={'visible_for_anonymous': False})
            n3 = NavigationNode(_("Log out"), reverse('core:logout'), 13, 10, attr={'visible_for_anonymous': False})
        else:
            n = NavigationNode(_("প্রোফাইল"), reverse('core:profile'), 10, attr={'visible_for_anonymous': False})
            n1 = NavigationNode(_("আমার প্রোফাইল"), reverse('core:profile'), 11, 10,
                                attr={'visible_for_anonymous': False})
            n2 = NavigationNode(_("আমার খামার"), reverse('core:my_farms'), 12, 10,
                                attr={'visible_for_anonymous': False})
            n3 = NavigationNode(_("প্রস্থান"), reverse('core:logout'), 13, 10, attr={'visible_for_anonymous': False})
            pass
        nodes.append(n)
        nodes.append(n1)
        nodes.append(n2)
        nodes.append(n3)
        return nodes


class MyMode(Modifier):
    """
    This modifier makes the changed_by attribute of a page
    accessible for the menu system.
    """

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        # if the menu is not yet cut, don't do anything

        if post_cut:
            return nodes
        # otherwise loop over the nodes
        if request.current_page:
            if request.current_page.is_home:
                # print(request.current_page, "i am here")
                for node in nodes:
                    if node.id == 15:
                        node.url = "#our-services"
                    elif node.id == 16:
                        node.url = "#our-company"
                    elif node.id == 17:
                        node.url = "#technology"
                    elif node.id == 19:
                        node.url = "#how-we-works"
                    elif node.id == 20:
                        node.url = "#brochure"
                    elif node.id == 21:
                        node.url = "#discover-our-company"
                    elif node.id == 22:
                        node.url = "#testimonials"
                    else:
                        pass
        if not request.user.is_anonymous:
            for node in nodes:
                # does this node represent a Page?

                if node.id == 10:
                    node.title = f"{request.user.get_email_or_phone()}"
                # if node.attr["is_page"]:
                #     # if so, put its changed_by attribute on the node
                #     # node.attr["changed_by"] = Page.objects.get(id=node.id).changed_by
                #     print(node)
        return nodes


menu_pool.register_modifier(MyMode)

menu_pool.register_menu(TestMenu)
menu_pool.register_menu(AboutUsMenu)
menu_pool.register_menu(UserMenu)
