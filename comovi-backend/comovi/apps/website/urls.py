from django.urls import path

from comovi.apps.website.views import HomeView, LoginView, MyProfileView, InboxView, LogoutView, PropertyView, \
    NewspaperView, PropertyInteriorView, PaymentInteriorView, PaymentView, PayView, SentInboxView, SendEmailView, \
    InboxDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('inbox/<uuid:pk>/', InboxDetailView.as_view(), name='inbox_detail'),
    path('inbox/create/', SendEmailView.as_view(), name='send_email'),
    path('inbox/sent/', SentInboxView.as_view(), name='inbox_sent'),
    path('newspaper/', NewspaperView.as_view(), name='newspaper'),
    path('property/<uuid:pk>/', PropertyView.as_view(), name='property'),
    path('property-interior/<uuid:pk>/', PropertyInteriorView.as_view(), name='property_interior'),
    path('payments/', PaymentInteriorView.as_view(), name='payments'),
    path('pay/<uuid:pk>/', PayView.as_view(), name='pay'),
    path('payments/history/', PaymentView.as_view(), name='payment_history')
]

app_name = 'website'
