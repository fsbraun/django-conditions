from django.db import models
from django.test import TestCase

from django_conditions.fsm import FSMField, transition


class ProtectedAccessModel(models.Model):
    status = FSMField(default="new", protected=True)

    @transition(field=status, source="new", target="published")
    def publish(self):
        pass

    class Meta:
        app_label = "django_conditions"


class MultiProtectedAccessModel(models.Model):
    status1 = FSMField(default="new", protected=True)
    status2 = FSMField(default="new", protected=True)

    class Meta:
        app_label = "django_conditions"


class TestDirectAccessModels(TestCase):
    def test_multi_protected_field_create(self):
        obj = MultiProtectedAccessModel.objects.create()
        self.assertEqual(obj.status1, "new")
        self.assertEqual(obj.status2, "new")

    def test_no_direct_access(self):
        instance = ProtectedAccessModel()
        self.assertEqual(instance.status, "new")

        def try_change():
            instance.status = "change"

        self.assertRaises(AttributeError, try_change)

        instance.publish()
        instance.save()
        self.assertEqual(instance.status, "published")