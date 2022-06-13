from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aps_plugins.models import Policy
from .models import *
from django.utils.translation import gettext as _
from django.template.loader import select_template
from .forms import *
from django.urls import reverse


class SubscriptionFormPlugin(CMSPluginBase):
    model = SubscriptionPluginModel
    name = 'Subscription Form Section'
    render_template = 'sharedfarm/plugins/subscription.html'

    """Enables latest event to be rendered in CMS"""

    def render(self, context, instance, placeholder):

        #
        # NOTE: We're actually interested in the request.path here, NOT the
        # referer, since this form will appear alongside real content, unlike
        # the contact form page, which is standalone.
        #
        try:
            path = context['request'].path
        except:
            path = ''

        form = SubscriptionForm(initial={'referer': path})

        context.update({
            "title": instance.title,
            "form": form,
            "form_action": reverse('sharedfarm:subscribe'),
        })
        return context


from djangocms_text_ckeditor.cms_plugins import TextPlugin


class MyTextPlugin(TextPlugin):
    name = _(u"My text plugin")
    model = MyModel


class HowWeWorkHeadPlugin(CMSPluginBase):
    model = HowWeWorkHead
    name = "How we works plugin"
    render_template = "sharedfarm/plugins/how_we_work.html"
    allow_children = True

    # frontend_editable_fields = ("banner_text",)

    def render(self, context, instance, placeholder):
        context.update({
            'myfield': instance.myfield,
            'number_of_steps': instance.number_of_steps,
        })
        context = super(HowWeWorkHeadPlugin, self).render(context, instance, placeholder)
        return context


class HowWeWorkStepItemPlugin(CMSPluginBase):
    model = HowWeWorkStepItem
    name = "How we works Steps Item"
    render_template = "sharedfarm/plugins/how_we_works_step_item.html"
    require_parent = True

    # frontend_editable_fields = ("banner_text",)

    def render(self, context, instance, placeholder):
        # context.update({
        #     'myfield': instance.myfield,
        #     'number_of_steps': instance.number_of_steps,
        # })
        context = super(HowWeWorkStepItemPlugin, self).render(context, instance, placeholder)
        return context


plugin_pool.register_plugin(MyTextPlugin)
plugin_pool.register_plugin(HowWeWorkHeadPlugin)
plugin_pool.register_plugin(HowWeWorkStepItemPlugin)

plugin_pool.register_plugin(SubscriptionFormPlugin)
