from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    # path('', views.home), THIS WILL BE USED FOR FUNCTION BASED VIEWS
    path('', views.ProductView.as_view(), name='home'),
    
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('add-address/', views.add_address, name='add_address'),
    path('update-address/<int:id>/', views.update_address, name='update_address'),
    path('delete-address/<int:id>/', views.delete_address, name='delete_address'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search_products, name='search'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>/', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.bottomwear, name='bottomweardata'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    # AUTHENTICATION PHASE STARTED
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form = LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    # PASSWORD RESET PHASE
    path('passwod-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('passwod-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('passwod-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    # AUTHENTICATION PHASE ENDED


    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)