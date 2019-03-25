from django import forms
from django.core.mail import send_mail as sm
from django.db import transaction

from comovi.apps.core.models import InboxMessage, Property, User


class InboxMessageForm(forms.Form):
    to = forms.CharField(required=True)
    body = forms.Field(required=True)
    subject = forms.CharField(required=True)

    _to = []
    _to_users = []
    _body = ''
    _subject = ''
    _property = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(InboxMessageForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        self._subject = cleaned_data.get("subject", '')
        self._body = cleaned_data.get("body", '')
        to = cleaned_data.get('to', '')

        if to.startswith('property-'):
            to = to.replace('property-', '')
            self._property = Property.objects.get(id=to)
            admins = self._property.admin_profiles.all()
            for admin in admins:
                self._to.append(admin.user.email)
                self._to_users.append(admin.user)
        elif to.startswith('user-'):
            to = to.replace('user-', '')
            user = User.objects.get(id=to)
            self._to.append(user.email)
            self._to_users.append(user)

        with transaction.atomic():
            message = InboxMessage.objects.create(
                user=self.request.user,
                subject=self._subject,
                property=self._property,
                message=self._body
            )
            for user in self._to_users:
                message.to.add(user)
            message.save()

        return cleaned_data