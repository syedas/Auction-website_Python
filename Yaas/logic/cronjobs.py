from django_cron import CronJobBase, Schedule
from django.shortcuts import get_object_or_404
from .models import Auction
from datetime import datetime

class YaasCron(CronJobBase):
    schedule = Schedule(run_every_mins=1,retry_after_failure_mins=1)
    code = 'yaas_cron_job'
    def do(self):
        blog = get_object_or_404(Auction.objects.all())
        if blog!=404:
            for a in blog:
              if a.deadline <= datetime.now():
                  a.is_locked=True
                  a.save()