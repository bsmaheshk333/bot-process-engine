from django.db import models

# Create your models here.


class WorkItemModel(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    state: str = models.CharField(verbose_name="work-item state")
    status: str = models.CharField(verbose_name="work-item status")
    detail = models.JSONField()
    exception_type: str = models.CharField(verbose_name="exception type")
