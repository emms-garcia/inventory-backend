# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from accounts.models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

    def clean_username(self):
        username = self.cleaned_data["username"]
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return username

            if self.instance.id and user.id == self.instance.id:
                raise forms.ValidationError(_(u"El nombre de usuario ya existe."))
            return username
        raise forms.ValidationError(_(u"Éste campo es requerido."))

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if len(first_name) < 3:
            raise forms.ValidationError(_(u"Debe tener al menos 3 caracteres."))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if len(last_name) < 3:
            raise forms.ValidationError(_(u"Debe tener al menos 3 caracteres."))
        return last_name

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise forms.ValidationError(_(u"Debe tener al menos 6 caracteres."))
        return password
