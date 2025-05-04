from django.db import models
from django.core.validators import FileExtensionValidator

from core_app.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class MediaFile(CreateMixin, UpdateMixin, SoftDeleteMixin):
    FILE_TYPE_IMAGE = 'image'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_DOCUMENT = 'document'
    FILE_TYPE_AUDIO = 'audio'
    FILE_TYPE_OTHER = 'other'

    FILE_TYPES = [
        (FILE_TYPE_IMAGE, 'Image'),
        (FILE_TYPE_VIDEO, 'Video'),
        (FILE_TYPE_DOCUMENT, 'Document'),
        (FILE_TYPE_AUDIO, 'Audio'),
        (FILE_TYPE_OTHER, 'Other'),
    ]

    file = models.FileField(
        upload_to='media_files/%Y/%m/%d/',
        validators=[
            FileExtensionValidator([
                'jpg', 'jpeg', 'png', 'gif',  # image
                'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',  # doc
                'mp4', 'mov', 'avi',  # video
                'mp3', 'wav',  # sound
            ])
        ]
    )
    title = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True,
                                help_text='متن توصیفی برای دسترسی پذیری و SEO')
    caption = models.TextField(blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        db_table = 'media_files'

    def __str__(self):
        return self.title or self.file.name

    def save(self, *args, **kwargs):
        ext = self.file.name.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            self.file_type = self.FILE_TYPE_IMAGE
        elif ext in ['mp4', 'mov', 'avi', 'mkv']:
            self.file_type = self.FILE_TYPE_VIDEO
        elif ext in ['pdf', 'doc', 'docx', 'xls', 'xlsx']:
            self.file_type = self.FILE_TYPE_DOCUMENT
        elif ext in ['mp3', 'wav', 'ogg']:
            self.file_type = self.FILE_TYPE_AUDIO
        else:
            self.file_type = self.FILE_TYPE_OTHER

        if self.file and not self.file_size:
            self.file_size = self.file.size

        super().save(*args, **kwargs)
