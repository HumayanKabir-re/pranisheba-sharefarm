from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import *
from django.utils.translation import gettext as _
from django.template.loader import select_template
from .forms import *


class Section_With_Image_Background_Plugin(CMSPluginBase):
    model = Section_With_Image_background
    name = "Section With Image Background"
    render_template = "section_with_image_background.html"

    def render(self, context, instance, placeholder):
        context.update({
            'name': instance.name,
            'image': instance.image
        })
        return context


class WhoWeAreLandingTextPlugin(CMSPluginBase):
    model = WhoWeAreLandingText
    name = "Who we are landing text"
    render_template = "who_we_are_landing_text.html"

    def render(self, context, instance, placeholder):
        context.update({
            'text1': instance.text1,
            'text2': instance.text2,
            'text3': instance.text3
        })
        return context

    pass


class BannerOverlayTextPlugin(CMSPluginBase):
    model = WhoWeAreLandingText
    name = "Banner video landing text"
    render_template = "banner_overlay_text.html"

    def render(self, context, instance, placeholder):
        context.update({
            'text1': instance.text1,
            'text2': instance.text2,
            'text3': instance.text3
        })
        return context

    pass


class StakeHolderDetailsPlugin(CMSPluginBase):
    model = StakeHolderDetails
    name = "Stakeholder details"
    render_template = "stakeholder_details.html"
    form = StakeholderDescriptionForm
    fields = ('title', 'icon', 'description')

    def render(self, context, instance, placeholder):
        context.update({
            'title': instance.title,
            'icon': instance.icon,
            'description': instance.description,
        })
        return context

    pass

    class Media:
        css = {
            "all": ("css/textareacounter.css",)
        }
        js = ("js/textareacounter.js",)


class WhatWeDoPlugin(CMSPluginBase):
    model = WhatWeDo
    name = 'Left Side Image Section'
    render_template = 'left_side_image_section.html'

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'head': instance.head,
            'description': instance.description

        })
        return context


class GenericTitleDescriptionPlugin(CMSPluginBase):
    model = GenericTitleDescription
    name = 'Generic Title Description'
    render_template = 'technology.html'

    def render(self, context, instance, placeholder):
        context.update({
            'title': instance.title,
            'description': instance.description

        })
        return context


class GenericTitleDescriptionBlogHeadPlugin(CMSPluginBase):
    model = GenericTitleDescription
    name = 'Latest Blog Title Description'
    render_template = 'latest_blog_post_head.html'

    def render(self, context, instance, placeholder):
        context.update({
            'title': instance.title,
            'description': instance.description

        })
        return context


class BuyAgriProductsPlugin(CMSPluginBase):
    model = WhatWeDo
    name = 'Right Side Image Section'
    render_template = 'Right_side_image_section.html'

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'head': instance.head,
            'description': instance.description

        })
        return context


class AboutUsHeadPlugin(CMSPluginBase):
    model = GenericTitleDescription
    name = 'About Us Header Section'
    render_template = "about_us_header.html"

    def render(self, context, instance, placeholder):
        context.update({
            'title': instance.title,
            'description': instance.description
        })
        return context


class AboutUsSectionOnePlugin(CMSPluginBase):
    model = WhatWeDo
    name = 'About Section One'
    render_template = 'about_section_one.html'

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'head': instance.head,
            'description': instance.description
        })
        return context


class AboutUsSectionTwoPlugin(CMSPluginBase):
    model = WhatWeDo
    name = 'About Section Two'
    render_template = 'about_section_two.html'

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'head': instance.head,
            'description': instance.description
        })
        return context


class TeamMemberPlugin(CMSPluginBase):
    model = TeamMember
    name = 'Team Member'
    render_template = 'team_member.html'

    def render(self, context, instance, placeholder):
        context.update({
            'name': instance.name,
            'designation': instance.designation,
            'image': instance.image
        })
        return context


class OurCompanyPlugin(CMSPluginBase):
    model = OurCompany
    name = 'Our Company'
    render_template = 'our_company.html'

    def render(self, context, instance, placeholder):
        context.update({
            'thumb1': instance.thumb1,
            'thumb2': instance.thumb2,
            'thumb3': instance.thumb3,
            'thumb4': instance.thumb4,
            'Video_thumb': instance.Video_thumb,
            'video_url': instance.video_url,
            'description': instance.description
        })
        context = super(OurCompanyPlugin, self).render(context, instance, placeholder)
        return context


class AboutShareFarmingPlugin(CMSPluginBase):
    model = Section_With_Image_background
    name = 'About SharedFarming'
    render_template = 'about_sharefarming.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context


class AboutShareFarmingCardPlugin(CMSPluginBase):
    model = GenericTitleDescription
    name = 'sharedFarming Card'
    render_template = 'sharefarming_card.html'
    require_parent = True

    def render(self, context, instance, placeholder):
        context = super(AboutShareFarmingCardPlugin, self).render(context, instance, placeholder)
        # context.update({
        #     'title': instance.title,
        #     'description': instance.description
        # })
        return context


class BrochurePlugin(CMSPluginBase):
    model = Brochure
    name = 'Upload Brochure'
    render_template = 'upload_brochure.html'

    def render(self, context, instance, placeholder):
        context = super(BrochurePlugin, self).render(context, instance, placeholder)
        # context.update({
        #     'title': instance.title,
        #     'description': instance.description
        # })
        return context


class ContactInfoPlugin(CMSPluginBase):
    model = ContactInfoPluginModel
    name = 'Contact info'
    render_template = 'contact_info.html'

    def render(self, context, instance, placeholder):
        context.update({
            'first_text': instance.first_text,
            'second_text': instance.second_text,
        })
        return context


class FeatureAndPartnerPlugin(CMSPluginBase):
    model = FeatureAndPartnerPluginModel
    name = 'Feature and partner logo'
    render_template = 'feature_partner.html'

    def render(self, context, instance, placeholder):
        context.update({
            'logo': instance.logo,
            'hover_logo': instance.hover_logo,
            'url': instance.url,
        })
        return context


class OurAwardsPlugin(CMSPluginBase):
    model = StandardHTMLPlugin
    name = "Our Awards text"
    render_template = "our_awards.html"

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'head': instance.head,
            'description': instance.description
        })
        return context

    pass


class TestimonialPlugin(CMSPluginBase):
    model = TestimonialPluginModel
    name = "Testimonial content"
    render_template = "testimonial.html"

    def render(self, context, instance, placeholder):
        context.update({
            'rating': instance.rating,
            'image': instance.image,
            'name': instance.name,
            'designation': instance.designation,
            'description': instance.description
        })
        return context

    pass


from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from cms.admin.placeholderadmin import PlaceholderAdminMixin


class SharedFarmBannerAppURLPlugin(CMSPluginBase):
    model = SharedFarmBannerDetailsPluginModel
    name = "SharedFarm Banner url"
    render_template = "sharedfarm_app_url.html"
    # form = SharedFarmBannerTextForm
    fields = ('app_url',)

    # frontend_editable_fields = ("banner_text",)

    def render(self, context, instance, placeholder):
        context.update({
            'app_url': instance.app_url,
        })
        # context = super(SharedFarmBannerPlugin, self).render(context, instance, placeholder)
        return context

    pass


class SharedFarmBannerImagePlugin(CMSPluginBase):
    model = SharedFarmBannerDetailsPluginModel
    name = "SharedFarm Banner images"
    render_template = "sharedfarm_banner_img.html"
    # form = SharedFarmBannerTextForm
    fields = ('rotate_img', 'front_img')

    # frontend_editable_fields = ("banner_text",)

    def render(self, context, instance, placeholder):
        context.update({
            'rotate_img': instance.rotate_img,
            'front_img': instance.front_img,
        })
        # context = super(SharedFarmBannerPlugin, self).render(context, instance, placeholder)
        return context

    pass


class TeamMemberTopRowPlugin(CMSPluginBase):
    model = TeamMember
    name = 'Team Member Top Management'
    render_template = 'team_member_top_row.html'

    def render(self, context, instance, placeholder):
        context.update({
            'name': instance.name,
            'designation': instance.designation,
            'image': instance.image
        })
        return context


class TeamMemberBottomRowPlugin(CMSPluginBase):
    model = TeamMember
    name = 'Team Member Business Team'
    render_template = 'team_member_bottom_row.html'

    def render(self, context, instance, placeholder):
        context.update({
            'name': instance.name,
            'designation': instance.designation,
            'image': instance.image
        })
        return context


class TeamMemberListPlugin(CMSPluginBase):
    model = TeamDepartment
    name = "Team List"
    render_template = "TeamList.html"
    allow_children = True

    # frontend_editable_fields = ("banner_text",)

    def render(self, context, instance, placeholder):
        context.update({
            'name': instance.name,
        })
        context = super(TeamMemberListPlugin, self).render(context, instance, placeholder)
        return context


class TeamListItemPlugin(CMSPluginBase):
    model = TeamMember
    name = 'Team Member List Item'
    render_template = 'TeamListItem.html'
    require_parent = True

    def render(self, context, instance, placeholder):
        context = super(TeamListItemPlugin, self).render(context, instance, placeholder)
        # context.update({
        #     'title': instance.title,
        #     'description': instance.description
        # })
        return context


class ContactUsPlugin(CMSPluginBase):
    model = ContactUs
    name = "Contact US plugin"
    render_template = "contact_us.html"

    # allow_children = True

    # frontend_editable_fields = ("banner_text",)

    def render(self, context, instance, placeholder):
        context.update({
            'text_field': instance.text_field,
            'contact_no': instance.contact_no,
        })
        context = super(ContactUsPlugin, self).render(context, instance, placeholder)
        return context


class PolicyPlugin(CMSPluginBase):
    model = Policy
    name = 'Policy Plugin'
    render_template = 'policy_section.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'head': instance.head,
            'description': instance.description
        })
        return context


class TermsOfServicePlugin(CMSPluginBase):      # NEW, added for Terms of Service 23/03/2022
    model = Terms
    name = 'Terms of Service Plugin'
    render_template = 'policy_section.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'head': instance.head,
            'description': instance.description
        })
        return context


class FooterPlugin(CMSPluginBase):
    model = FooterLinks
    name = "Links and Socials"
    render_template = 'footer_plugin.html'
    # forms = FooterDropDownForm
    # fields = ('linkType',)
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'linkName': instance.linkName,
            'icon': instance.icon,
            'location': instance.location,
            'linkType': instance.linkType,
            'link': instance.link,
        })
        return context


plugin_pool.register_plugin(TermsOfServicePlugin)   # NEW, Changed the urls for redirecting Terms of Service - 23/03/2022
plugin_pool.register_plugin(FooterPlugin)
plugin_pool.register_plugin(PolicyPlugin)
plugin_pool.register_plugin(WhoWeAreLandingTextPlugin)
plugin_pool.register_plugin(BannerOverlayTextPlugin)
plugin_pool.register_plugin(Section_With_Image_Background_Plugin)
plugin_pool.register_plugin(StakeHolderDetailsPlugin)
plugin_pool.register_plugin(WhatWeDoPlugin)
plugin_pool.register_plugin(GenericTitleDescriptionPlugin)
plugin_pool.register_plugin(GenericTitleDescriptionBlogHeadPlugin)
plugin_pool.register_plugin(BuyAgriProductsPlugin)
# plugin_pool.register_plugin(AboutUsHeadPlugin)
# plugin_pool.register_plugin(AboutUsSectionOnePlugin)
# plugin_pool.register_plugin(AboutUsSectionTwoPlugin)
# plugin_pool.register_plugin(TeamMemberPlugin)
plugin_pool.register_plugin(OurCompanyPlugin)
plugin_pool.register_plugin(AboutShareFarmingPlugin)
plugin_pool.register_plugin(AboutShareFarmingCardPlugin)
plugin_pool.register_plugin(BrochurePlugin)
plugin_pool.register_plugin(ContactInfoPlugin)
plugin_pool.register_plugin(FeatureAndPartnerPlugin)
plugin_pool.register_plugin(OurAwardsPlugin)
plugin_pool.register_plugin(TestimonialPlugin)
plugin_pool.register_plugin(SharedFarmBannerAppURLPlugin)
plugin_pool.register_plugin(SharedFarmBannerImagePlugin)
plugin_pool.register_plugin(TeamMemberTopRowPlugin)
plugin_pool.register_plugin(TeamMemberBottomRowPlugin)
plugin_pool.register_plugin(TeamMemberListPlugin)
plugin_pool.register_plugin(TeamListItemPlugin)
plugin_pool.register_plugin(ContactUsPlugin)
