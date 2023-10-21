from django.db import models
from my_account.models import User
from django.utils.translation import gettext_lazy as _
from . custom_model_managers import *
from django.urls import reverse
from datetime import date
from django.utils import timezone
from autoslug import AutoSlugField
from basemodels.models import BaseModel

class Dairy(BaseModel):
    name = models.CharField(_("name"),max_length=200,unique=True)
    slug = AutoSlugField("Slug",populate_from='name',unique=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name="dairies",verbose_name=_("user"))
    location = models.CharField(_("location"),max_length=200)
    is_verified = models.BooleanField(_("verified"),default=False)
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)
    members = models.ManyToManyField(User,verbose_name=_("members"),null=True,blank=True)

    objects = models.Manager()
    verObs = DairyModelManager()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("dairy")
        verbose_name_plural = _("dairies")

    def get_absolute_url(self):
        return reverse('dairyapp:homepage')
    

class FatRate(BaseModel):
    fat_rate = models.FloatField(_("fat rate"),max_length=5)
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE,verbose_name=_("dairy"))
    bonous_amount = models.PositiveSmallIntegerField("Bonous amount",default=0)
    created_at = models.DateTimeField(_("created at"),default=timezone.now())
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)
    

    def __str__(self) -> str:
        return f"{self.dairy.name}-{self.fat_rate}"
    
    @property
    def get_fat_rate(self):
        return self.fat_rate + self.bonous_amount
    
class MilkRecord(BaseModel):
    shift_choices = (
        ("morning","Morning"),
        ("night","Night")
    )
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE,verbose_name=_("dairy"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name=_("user"))
    shift = models.CharField(_("shift"),max_length=10,choices=shift_choices)
    milk_weight = models.FloatField(_("milk weight"))
    milk_fat = models.FloatField(_("milk fat"),max_length=5)
    date = models.DateField(_("date"))
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)

    class Meta:
        unique_together = ["dairy", "user","shift","date"]


class MilkReportEmailHistory(BaseModel):
    shift_choices = (
        ("morning","morning"),
        ("night","night")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE,verbose_name=_("dairy"))
    shift = models.CharField(_("shift"),max_length=10,choices=shift_choices)
    fat_rate = models.FloatField(_("fat rate"),max_length=5)
    bonous_amount = models.PositiveSmallIntegerField("Bonous amount",default=0)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    milk_weight = models.FloatField(_("milk weight"))
    avg_fat = models.FloatField(_("Avg fat"))
    total_amount = models.FloatField(_("Total amount"))
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)

    @property
    def get_fat_rate(self):
        return self.fat_rate + self.bonous_amount