# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, label=_(u"Логин"))
    password = serializers.CharField(label=_(u"Пароль"))

    default_error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(LoginSerializer, self).__init__(request, *args, **kwargs)
        User = get_user_model()
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None:
                raise serializers.ValidationError(
                    self.error_messages['invalid_login'] % {
                        'username': self.username_field.verbose_name
                    })

            elif not self.user_cache.is_active:
                raise serializers.ValidationError(
                    self.error_messages['inactive'])

        if request and not request.session.test_cookie_worked():
            raise serializers.ValidationError(
                self.error_messages['no_cookies'])

        return attrs

    def get_user(self):
        return self.user_cache

    class Meta:
        model = get_user_model()


class SetPasswordSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(label=_("New password"))
    new_password2 = serializers.CharField(label=_("New password confirmation"))

    default_error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def validate_new_password1(self, attrs, source):
        if not attrs.get(source):
            raise serializers.ValidationError(
                self.error_messages['required'])

        return attrs

    def validate_new_password2(self, attrs, source):
        password1 = attrs.get('new_password1')
        password2 = attrs.get('new_password2')

        if not password2:
            raise serializers.ValidationError(
                self.error_messages['required'])

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'])

        return attrs

    def restore_object(self, attrs, instance=None):
        instance = super(SetPasswordSerializer,
                         self).restore_object(attrs, instance)

        instance.set_password(attrs.get('new_password1'))
        instance.new_password1 = ''
        instance.new_password2 = ''

        return instance

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordChangeSerializer(SetPasswordSerializer):
    default_error_messages = dict(
        SetPasswordSerializer.default_error_messages,
        **{'password_incorrect': _(
            "Your old password was entered incorrectly. "
            "Please enter it again.")}
    )

    old_password = serializers.CharField(label=_("Old password"))

    def validate_old_password(self, attrs, source):
        old_password = attrs.get("old_password")
        user = getattr(self, 'object', None)

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                self.error_messages['password_incorrect'])

        return attrs

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']
