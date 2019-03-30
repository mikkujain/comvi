from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.db.models import Q
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView

from comovi.apps.core.models import User, Property, PropertyInterior, InboxMessage, PropertyInteriorHasService, Payment, \
    Post, BaseModel
from comovi.apps.website.dashboard import Dashboard
from comovi.apps.website.forms import InboxMessageForm
from .translations import translations
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import UpdateView
from .forms import ProfileModelForm
import uuid
import datetime

# noinspection PyMethodMayBeStatic
class LoginView(TemplateView):
    template_name = 'website/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('website:index'))
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('website:index'))
            else:
                error = translations['inactive_user']
        else:
            user_exist = User.objects.filter(username=username).count() > 0
            error = translations['incorrect_password'] if user_exist else translations['user_does_not_exist']
        return TemplateResponse(template=self.template_name, request=request, context={'error': error})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'website/dashboard_2.html' # changes index to dashboard.html


class PageView(LoginRequiredMixin, TemplateView):
    template_name = 'website/real-cerezos.html'
    
class DetailMsgView(LoginRequiredMixin, TemplateView):
    template_name = 'website/inbox_detail.html'


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'website/inbox.html'
    model = InboxMessage
    context_object_name = 'messages'
    paginate_by = 15
    queryset = InboxMessage.objects.all().order_by('-date_creation')

    def get_queryset(self):
        queryset = super(InboxView, self).get_queryset()
        if hasattr(self.request.user, 'admin_profile') and self.request.user.admin_profile:
            return queryset.filter(Q(to__id__in=[self.request.user.id]) |
                                   Q(property__id__in=self.request.user.admin_profile.my_properties().values_list('id',
                                                                                                                  flat=True))).order_by(
                '-date_creation')
        elif hasattr(self.request.user, 'owner_profile') and self.request.user.owner_profile:
            return queryset.filter(Q(to__id__in=[self.request.user.id]) |
                                   Q(property__id__in=self.request.user.owner_profile.my_properties().values_list('id',
                                                                                                                  flat=True))).order_by(
                '-date_creation')
        else:
            return queryset.filter(to__id__in=[self.request.user.id]).order_by('-date_creation')


class InboxDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/inbox_detail.html'
    model = InboxMessage
    queryset = InboxMessage.objects.all()


class SendEmailView(LoginRequiredMixin, FormView):
    template_name = 'website/send_email.html'
    model = InboxMessage
    form_class = InboxMessageForm
    success_url = '/inbox/sent/'

    def get_form_kwargs(self):
        kwargs = super(SendEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SentInboxView(InboxView):

    def get_queryset(self):
        return self.request.user.sent_messages.all().order_by('-date_creation')


class PaymentInteriorView(LoginRequiredMixin, ListView):
    template_name = 'website/payments.html'
    model = PropertyInteriorHasService
    context_object_name = "payments"
    paginate_by = 15
    queryset = PropertyInteriorHasService.objects.all() \
        .select_related('property_interior') \
        .select_related('service')

    def get_queryset(self):
        user = self.request.user
        is_root = user.is_superuser
        is_admin = False if not hasattr(user, 'admin_profile') or not user.admin_profile else True
        is_owner = False if not hasattr(user, 'owner_profile') or not user.owner_profile else True
        queryset = super(PaymentInteriorView, self).get_queryset()
        if is_root:
            return queryset
        if is_admin:
            properties = user.admin_profile.properties_managed.through.objects.all().values('property_id')
            return queryset.filter(property_interior__property__id__in=properties)
        if is_owner:
            property_interiors = user.owner_profile.property_interiors_owned.through.objects.all().values(
                'propertyinterior_id')
            return queryset.filter(property_interior__id__in=property_interiors)
        return PropertyInteriorHasService.objects.none()


class PaymentView(LoginRequiredMixin, ListView):
    template_name = 'website/history.html'
    model = Payment
    context_object_name = 'payments'
    paginate_by = 30
    queryset = Payment.objects.all().order_by('-payment_datetime')

    def get_queryset(self):
        user = self.request.user
        is_root = user.is_superuser
        is_admin = False if not hasattr(user, 'admin_profile') or not user.admin_profile else True
        is_owner = False if not hasattr(user, 'owner_profile') or not user.owner_profile else True
        queryset = super(PaymentView, self).get_queryset()
        if is_root:
            return queryset
        if is_admin:
            properties = user.admin_profile.properties_managed.through.objects.all().values('property_id')
            return queryset.filter(property_interior_has_service__property_interior__property_id__in=properties)
        if is_owner:
            property_interiors = user.owner_profile.property_interiors_owned.through.objects.all().values(
                'propertyinterior_id')
            return queryset.filter(property_interior_has_service__property_interior__id__in=property_interiors)
        return PropertyInteriorHasService.objects.none()


class NewspaperView(LoginRequiredMixin, ListView):
    template_name = 'website/newspaper.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 30
    queryset = Post.objects.all().select_related('category').order_by('-date_creation')

    def get_queryset(self):
        user = self.request.user
        is_owner = False if not hasattr(user, 'owner_profile') or not user.owner_profile else True
        queryset = super(NewspaperView, self).get_queryset()
        queryset = self.filter_params(queryset)
        if is_owner:
            return queryset.filter(is_active=True)
        return queryset

    def filter_params(self, queryset):
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        _property = self.request.GET.get('property', None)
        if _property and _property != '':
            queryset = queryset.filter(property_id=_property)
        elif hasattr(self.request.user, 'owner_profile') and self.request.user.owner_profile:
            properties = self.request.user.owner_profile.my_properties().values_list('id', flat=True)
            queryset = queryset.filter(property__id__in=properties)
        elif hasattr(self.request.user, 'admin_profile') and self.request.user.admin_profile:
            properties = self.request.user.admin_profile.my_properties().values_list('id', flat=True)
            queryset = queryset.filter(property__id__in=properties)
        return queryset


# noinspection PyMethodMayBeStatic
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('website:login'))


class PropertyView(LoginRequiredMixin, DetailView):
    template_name = 'website/property.html'
    queryset = Property.objects.all()
    model = Property

    def get_context_data(self, **kwargs):
        obj = kwargs['object']

        preferences = obj.make_preferences()
        kwargs.update({
            'preferences': preferences,
            'property_interiors_stat': Dashboard.make_property_interiors_stat(obj),
            'service_stats': Dashboard.make_services_to_show(preferences.services_to_show.all())
        })

        return super(PropertyView, self).get_context_data(**kwargs)


class PropertyInteriorView(LoginRequiredMixin, DetailView):
    template_name = 'website/property_interior.html'
    queryset = PropertyInterior.objects.all()
    model = PropertyInterior

    def get_context_data(self, **kwargs):
        return super(PropertyInteriorView, self).get_context_data(**kwargs)


class PayView(LoginRequiredMixin, DetailView):
    template_name = 'website/pay.html'
    model = PropertyInteriorHasService
    queryset = PropertyInteriorHasService.objects.all()



class EditUserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView): 
    template_name = "website/my_profile.html"
    form_class = ProfileModelForm
    success_message = "Profile Successfully Updated"
    
    def get_object(self, queryset=None):
        return self.request.user





