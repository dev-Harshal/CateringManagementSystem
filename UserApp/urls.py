from django.urls import path
from UserApp.views import * 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',indexPageView,name='index-page'),
    path('signup/',signupPageView,name='signup-page'),
    path('login/',loginPageView,name='login-page'),
    path('logout/',logoutPageView,name='logout-page'),
    path('home/',homePageView,name='home-page'),
    path('package/',packagePageView,name='package-page'),
    path('category/<int:category>/',displaySubCategoryView,name="display-category"),
    path('menu/<int:sub_category>/',displayMenuView,name="display-menu"),
    path('choose/menu/',chooseMenuView,name="choose-menu"),
    path('quotation/',displayQuotationView,name="display-quotation"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)