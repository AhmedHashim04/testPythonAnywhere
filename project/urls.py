"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from home.views import HomeView, TermsOfServiceView, PrivacyPolicy
from project.admin import custom_admin_site
from django.http import HttpResponseForbidden

def disabled_view(request):
    return HttpResponseForbidden("This page is disabled.")

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(

    path("accounts/email/", disabled_view),path("accounts/password/change/", disabled_view),path("accounts/signup/", disabled_view),path("accounts/login/", disabled_view),path("accounts/password/reset/", disabled_view),path("accounts/password/set/", disabled_view),
    path('', HomeView.as_view(), name='home'), 
    path('my-account/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include("allauth.urls")),
    path('products/', include("product.urls", namespace="product")),
    path('order/', include("order.urls", namespace="order")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('contact/', include("contact.urls", namespace="contact")),
    path('admin/', admin.site.urls),
    path('mohamed/', custom_admin_site.urls),
    path('terms/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path("privacy/", PrivacyPolicy.as_view(), name="privacy_policy"),

    prefix_default_language=True,
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# handler404 = 'home.views.handler404'
# handler500 = 'home.views.handler500'

    

