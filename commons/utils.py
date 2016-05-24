# coding: utf-8
from __future__ import unicode_literals
import uuid


def get_uuid():
  """
  Generate a 32 character unique id.
  """
  return ''.join(str(uuid.uuid4()).split('-'))
