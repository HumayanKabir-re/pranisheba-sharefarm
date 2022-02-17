from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


# ৳
def currency(amount):
    # amount = round(float(amount))
    return "৳ %s" % (intcomma(amount))


register.filter('currency', currency)
