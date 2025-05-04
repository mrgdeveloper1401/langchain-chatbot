from django.db import models

from chat_app.ai import langchain_pdf_file
from core_app.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Message(CreateMixin, UpdateMixin, SoftDeleteMixin):
    file = models.ForeignKey("catalog_app.MediaFile", on_delete=models.DO_NOTHING, related_name="messages")
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    response = models.JSONField(blank=True)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "message"
    
    def save(self, *args, **kwargs):
        documents = langchain_pdf_file(self.file)
        self.response = [doc.page_content for doc in documents]
        self.metadata = documents[0].metadata if documents else {}
        super().save(*args, **kwargs)