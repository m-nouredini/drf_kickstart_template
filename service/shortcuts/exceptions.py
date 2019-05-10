from rest_framework import status
from rest_framework.exceptions import APIException

from django.utils.translation import ugettext_lazy as _


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Duplicate Entry')
    default_code = 'conflict'

    def __init__(self, detail=None, code=None, available_renderers=None):
        self.available_renderers = available_renderers
        super(Conflict, self).__init__(detail, code)
