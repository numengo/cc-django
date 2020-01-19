import os
from .local import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(WORK_DIR, "db.sqlite3"),
    }
}
