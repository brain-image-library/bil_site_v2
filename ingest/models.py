from django.db import models
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor


class MinimalImgMetadata(models.Model):
    def __str__(self):
        return self.project_name
    AI = 'AI'
    CSHL = 'CSHL'
    USC = 'USC'
    ORGANIZATION_CHOICES = (
        (CSHL, 'Cold Spring Harbor Laboratory'),
        (USC, 'University of Southern California'),
        (AI, 'Allen Institute'),
    )
    organization_name = models.CharField(
        max_length=200,
        choices=ORGANIZATION_CHOICES,
        default=AI,
    )
    project_name = models.CharField(max_length=200)
    project_description = models.CharField(max_length=200)
    project_funder_id = models.CharField(max_length=200)
    background_strain = models.CharField(max_length=200)
    image_filename_pattern = models.CharField(max_length=200)
    linked_to_data = models.BooleanField(default=False)


class MinimalImgTable(tables.Table):
    id = tables.LinkColumn('ingest:detail', args=[A('pk')])
    project_description = tables.Column()

    def render_project_description(self, value):
        limit_len = 32
        value = value if len(value) < limit_len else value[:limit_len]+"…"
        return value

    class Meta:
        model = MinimalImgMetadata
        template_name = 'ingest/bootstrap_ingest.html'

