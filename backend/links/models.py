from django.db import models
from django.utils.translation import gettext_lazy as _

class LinkPair(models.Model):
    users = models.ForeignKey(to= "users.User", verbose_name=_("user"), on_delete=models.CASCADE)
    link = models.CharField(verbose_name= _("link") ,max_length=2000)
    short_link = models.CharField(verbose_name= _("short link"), max_length=2000) # set by user or outo jenerate UUID
    usage = models.PositiveIntegerField(verbose_name=_("number of usage"), default=0)
    duration = models.BigIntegerField(verbose_name=_("duration"), default=86_400) # in second 
    is_expired = models.BooleanField(verbose_name=_("expired"), default=False) # celery update it based on duration

    
    def __str__(self):
        return self.users.phone_number