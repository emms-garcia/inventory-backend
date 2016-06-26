# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.core.validators import validate_email
from django.forms import ValidationError
from django.utils.translation import ugettext as _

# TASTYPIE
from tastypie.validation import Validation


class ClientValidation(Validation):

    def is_valid(self, bundle, request=None):
        errors = {}

        if not bundle.data:
            return {'__all__': _(u'No se recibieron datos.')}

        # Name required, must be longer than 2 characters
        if bundle.data.get('name'):
            if len(bundle.data['name']) < 3:
                errors['name'] = [
                    _(u'Nombre: Este campo debe tener al menos 3 caracteres.')]
        else:
            errors['name'] = [_(u'Nombre: Este campo es requerido.')]

        # Email must be email
        if bundle.data.get('email'):
            try:
                validate_email(bundle.data['email'])
            except ValidationError:
                errors['email'] = [
                    _(u'Correo: Debe ser un correo electrónico.')]

        return errors
