# -*- coding: utf-8 -*-
from django.conf.urls import url, re_path, include
from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('division', views.DivisionViewSet)
router.register('district', views.DistrictViewSet)
router.register('breed', views.BreedViewSet)
router.register('faq-category', views.FaqCategoryViewSet)
router.register('faq-item', views.FaqItemViewSet)
router.register(r'fund_opportunities', views.FundOpportunityViewSet)
router.register(r'invoice', views.InvoiceViewSet, basename='invoice')
router.register(r'whats_new', views.WhatsNewBannerViewSet, basename='whats_new')

sharedfarm_api_urlpatterns = [

    path('', include(router.urls)),
    # this api is no longer required now
    # url(r'^checkout/(?P<farm>\d+)/(?P<unit>\w+)$', views.CheckoutRestApiView.as_view(), name='checkout'),
    url(r'^sdk_checkout/$', views.PaymentCheckOutAPI.as_view(), name='sdk_checkout'),
    url(r'^invest_summery/$', views.InvestmentSummeryView.as_view(), name='invest_summery')
]

sharedfarm_blog_api_urlpatterns = [
    path('posts/', views.get_posts)
]

app_name = "sharedfarm"
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    # url('create_book/', views.BookCreateView.as_view(), name='create_book'),
    url('^subscribe/$', views.SubscriptionView.as_view(), name='subscribe'),
    url(r'^(?P<product_id>\d+)/checkout/$', views.checkout, name='checkout'),
    path('return_url', views.ReturnUrlView.as_view(), name='return_url'),
    path('test_return_url', views.snippet_list),

]
