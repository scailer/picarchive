# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from utils.rest.auth.serializers import SetPasswordSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    verbose_name = serializers.CharField(
        source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'verbose_name')


class RestorePassword(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))

    default_error_messages = {
        'nouser': _(u'This email does not conected with any user'),
    }

    def get_user(self):
        return self.user_cache

    def validate_email(self, attrs, source):
        try:
            user = User.objects.get(email=attrs[source])
            self.user_cache = user

        except User.DoesNotExist:
            raise serializers.ValidationError(self.error_messages['nouser'])

        return attrs

    def save(self, **kwargs):
        user = self.get_user()
        user.make_password()
        return user

    class Meta:
        model = User


class RegistrationSerializer(SetPasswordSerializer,
                             serializers.ModelSerializer):

    email = serializers.EmailField(source='email', required=True)

    default_error_messages = {
        'email_not_unique': _("Email does not unique."),
    }

    def validate_email(self, attrs, source):
        email = attrs.get(source)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                self.error_messages['email_not_unique'])

        return attrs

    def restore_object(self, attrs, instance=None):
        data = {
            'email': attrs.get('email'),
            'username': User.objects.make_username(attrs.get('email')),
        }

        instance = super(SetPasswordSerializer,
                         self).restore_object(data, instance)

        instance.set_password(attrs.get('new_password1'))
        instance.new_password1 = ''
        instance.new_password2 = ''

        return instance

    class Meta:
        model = User
        fields = ['id', 'email', 'new_password1', 'new_password2']
