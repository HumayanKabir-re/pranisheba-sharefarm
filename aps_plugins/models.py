from django.db import models
from cms.models.pluginmodel import CMSPlugin
from cms.models import PlaceholderField, CMSPlugin as CMSPlugin_custom
# from sharedfarm.models import Product
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator, MinLengthValidator, MaxLengthValidator
from djangocms_text_ckeditor.fields import HTMLField
from djangocms_text_ckeditor.models import AbstractText, CMSPlugin as ck_CMSPlugin


# Create your models here.

class Section_With_Image_background(CMSPlugin):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="section_with_image_background")

    class Meta:
        verbose_name = "Section with Image Background"
        pass

    def __unicode__(self):
        return f'{self.name}'

    pass


class WhoWeAreLandingText(CMSPlugin):
    text1 = models.CharField(max_length=200, null=True, blank=True)
    text2 = models.CharField(max_length=200, null=True, blank=True)
    text3 = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Who we are landing text"

    def __unicode__(self):
        return f'{self.text1}'


class StakeHolderDetails(CMSPlugin):
    icons = (
        ('bi bi-people', 'Farmers'),
        ('bi bi-cash-coin', 'Investors'),
        ('bi bi-bank2', 'Agri Companies'),
        ('bi bi-cart-check', 'Buyers'),

    )
    title = models.CharField(max_length=200, null=False, blank=False)
    icon = models.CharField(max_length=100, choices=icons, null=True, blank=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Stakeholder details"

    def __unicode__(self):
        return f'{self.title}'


class WhatWeDo(CMSPlugin):
    image = models.ImageField(upload_to="what_we_do")
    head = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "What We Do"

    def __unicode__(self):
        return f'{self.head}'




class GenericTitleDescription(CMSPlugin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_first = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Generic Title & Description"

    def __unicode__(self):
        return f'{self.title}'


class TeamMember(CMSPlugin):
    name = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="team_memeber", null=True, blank=True)

    class Meta:
        verbose_name = "Team Member details"

    def __unicode__(self):
        return f'{self.name}'


class OurCompany(ck_CMSPlugin):
    thumb1 = models.ImageField(upload_to="our_company")
    thumb2 = models.ImageField(upload_to="our_company")
    thumb3 = models.ImageField(upload_to="our_company")
    thumb4 = models.ImageField(upload_to="our_company")
    Video_thumb = models.ImageField(upload_to="our_company")
    video_url = models.URLField(help_text='Please enter your video url', validators=[URLValidator])
    description = HTMLField(null=True, blank=True, configuration="BLOG_POST_TEXT_CKEDITOR")

    class Meta:
        verbose_name = "Our Company"

    def __unicode__(self):
        return f'{self.Video_thumb}'


class Brochure(CMSPlugin):
    image = models.ImageField(upload_to="our_company")
    brochure = models.FileField(upload_to='our_company')

    class Meta:
        verbose_name = "Our Brochure"

    def __unicode__(self):
        return f'{self.brochure}'


# class ContactInfoPluginModel(CMSPlugin):
#     phone = models.CharField(max_length=13, null=False, help_text='Contact phone number')
#     email = models.EmailField(null=False, help_text='Email address', )
#
#     class Meta:
#         verbose_name = "Top bar Scroll contact info"
#
#     def __unicode__(self):
#         return f'{self.phone}'
#

class ContactInfoPluginModel(CMSPlugin):
    first_text = models.CharField(max_length=50, null=False, help_text='Enter text')
    second_text = models.CharField(max_length=50, null=False, help_text='Enter text', )

    class Meta:
        verbose_name = "Top bar Scroll contact info"

    def __unicode__(self):
        return f'{self.first_text}'


class FeatureAndPartnerPluginModel(CMSPlugin):
    logo = models.ImageField(upload_to="FeatureAndPartner")
    hover_logo = models.ImageField(upload_to="FeatureAndPartner")
    url = models.URLField(help_text='Please enter your brand url', validators=[URLValidator], null=True)

    class Meta:
        verbose_name = "Feature nad Partner Logo"

    def __unicode__(self):
        return f'{self.logo}'


class StandardHTMLPlugin(CMSPlugin):
    image = models.ImageField(upload_to="StandardHTMLPlugin")
    head = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "Standard HTML content"

    def __unicode__(self):
        return f'{self.head}'


class TestimonialPluginModel(CMSPlugin):
    rating = models.PositiveIntegerField()
    image = models.ImageField(upload_to="Testimonial")
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "Testimonial content"

    def __unicode__(self):
        return f'{self.name}'


def my_placeholder_slotname(instance):
    return 'banner_text_editor'


class SharedFarmBannerDetailsPluginModel(CMSPlugin_custom):
    app_url = models.URLField(help_text='Please enter your app url', validators=[URLValidator], null=True)
    rotate_img = models.ImageField(upload_to="Sharedfarm_banner", null=True, blank=True)
    front_img = models.ImageField(upload_to="Sharedfarm_banner", null=True, blank=True)

    class Meta:
        verbose_name = "Shared Farm Banner content"

    def __unicode__(self):
        return f'{self.app_url}'


class TeamDepartment(CMSPlugin):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return f'{self.name}'


class ContactUs(ck_CMSPlugin):
    text_field = HTMLField(null=True, blank=True, configuration="BLOG_POST_TEXT_CKEDITOR")
    contact_no = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return f'{self.contact_no}'



class Policy(CMSPlugin):
    head = models.CharField(max_length=200)
    description = HTMLField(null=True, blank=True, configuration="POLICY_POST_TEXT_CKEDITOR")
    

    class Meta:
        verbose_name = "Policy"

    def __unicode__(self):
        return f'{self.head}'

