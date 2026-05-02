from django.contrib import admin
from django.contrib.admin.utils import unquote, quote
from django.utils.encoding import force_str
from reversion.admin import VersionAdmin
from test_app.models import TestModel, TestModelRelated, TestModelCustomObjectId


class TestModelAdmin(VersionAdmin):

    filter_horizontal = ("related",)


class TestModelCustomObjectIdAdmin(VersionAdmin):

    def reversion_register(self, model, **kwargs):
        kwargs["object_id_field"] = "slug"
        super().reversion_register(model, **kwargs)

    def get_reversion_object_id(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))
        return force_str(obj.slug) if obj else unquote(object_id)

    def get_reversion_changeform_object_id(self, version):
        obj = self.model._default_manager.using(version.db).get(slug=version.object_id)
        return quote(str(obj.pk))


admin.site.register(TestModel, TestModelAdmin)
admin.site.register(TestModelRelated, admin.ModelAdmin)
admin.site.register(TestModelCustomObjectId, TestModelCustomObjectIdAdmin)
