from datetime import datetime
from django.db import models
from django.urls import reverse
from accounts.models import User


class ReportManager(models.Manager):
    """ Report manager """

    def get_all_reports(self, user):
        reports = Report.objects.filter(user=user, is_active=True, is_deleted=False)
        return reports

    def get_running_reports(self, user):
        running_reports = Report.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_reports


class Report(models.Model):
    """ Report model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = ReportManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:report-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:report-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
