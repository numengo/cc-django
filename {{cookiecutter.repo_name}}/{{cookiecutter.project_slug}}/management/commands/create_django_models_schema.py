# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json
from pprint import pprint

from ngoschemapremium.transforms.django2jsonschema import Django2JsonSchemaTransform
from ngoschema import utils, settings
from ngoschema.resolver import domain_uri

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

DJANGO_APPS = list(apps.app_configs.keys())


class Command(BaseCommand):
    """Create the schema of the application Django models"""

    def handle(self, *args, **options):

        def django_ns_uri(app_name):
            return "#/definitions/" + app_name

        ns = {app: django_ns_uri(app) for app in DJANGO_APPS}

        schema = {
            '$id': domain_uri('django'),
            '$schema': settings.MS_URI,
            'description': 'Django definitions',
            'title': 'object',
            'definitions': OrderedDict()
        }

        for app in DJANGO_APPS:
            schema['definitions'][app] = Django2JsonSchemaTransform.transform(app, ns)

        pprint(schema)

        fp = settings.APPS_DIR('schemas/django.json')
        with open(fp, 'w') as f:
            json.dump(schema, f, indent=2)
