from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    raw_id_fields = ("file",)
    list_select_related = ("file",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "file__title",
            "file__file",
            "message",
            "is_active",
            "response",
        )
