# coding: utf-8

# DJANGO
from django.core.validators import validate_email
from django.forms import ValidationError
from django.utils.translation import ugettext as _

# TASTYPIE
from tastypie.validation import Validation

class AccountValidation(Validation):

    def is_valid(self, bundle, request=None):
        errors = {}
  
        if not bundle.data:
            return {'__all__': _(u'No se recibieron datos.')}

        # Username required, and must be email
        if bundle.data.get('username'):
            try:
                validate_email(bundle.data['username'])
            except ValidationError:
                errors['username'] = [_(u'Nombre de usuario: Debe ser un correo electrónico.')]
        else:
            errors['username'] = [_(u'Nombre de usuario: Este campo es requerido.')]

        # First name required and longer than 2 characters
        if bundle.data.get('first_name'):
            if len(bundle.data['first_name']) < 3:
                errors['first_name'] = [_(u'Nombre(s): Este campo debe tener al menos 3 caracteres.')]
        else:
            errors['first_name'] = [_(u'Nombre(s): Este campo es requerido.')]

        # Last name required and longer than 2 characters
        if bundle.data.get('last_name'):
            if len(bundle.data['last_name']) < 3:
                errors['last_name'] = [_(u'Apellido(s): Este campo debe tener al menos 3 caracteres.')]
        else:
            errors['last_name'] = [_(u'Apellido(s): Este campo es requerido.')]

        # Password required and longer than 4 characters
        if bundle.data.get('password'):
            if len(bundle.data['password']) < 5:
                errors['password'] = [_(u'Contraseña: Este campo debe tener al menos 5 caracteres.')]
        else:
            errors['password'] = [_(u'Contraseña: Este campo es requerido.')]


        return errors