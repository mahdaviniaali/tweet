from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

#######
# <--------- Base Model QuerySet --------->
# <--------- کوئری ست مدل پایه برای استفاده در مدل های پایه --------->
########

class BaseModelQuerySet(models.QuerySet):

    # ----for soft delete------
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


########
# <--------- Base Model Manager --------->
# <--------- مدیر مدل پایه برای استفاده در مدل های پایه --------->
########


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db).alive()



#########
# <--------- Base Models --------->
# <--------- مدل پایه برای ایجاد ویژگی های مشترک  --------->
##########

class BaseModel(models.Model):
    
    deleted_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords(inherit=True)

    objects = BaseModelManager()
    all_objects = models.Manager()
    features = models.ManyToManyField('plans.Features', related_name='%(class)s_features', blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

