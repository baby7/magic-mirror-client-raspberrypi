import os
from conf import settings


def hass():
    os.system(settings.HASS_COMMEND)
