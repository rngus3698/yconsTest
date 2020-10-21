from django.db import models

# Create your models here.


class Deal(models.Model):
    user_give = models.ForeignKey('account.Profile', default=1, on_delete=models.CASCADE)
    user_take = models.IntegerField(default=0)
    deal_money = models.IntegerField(default=0)

    class Meta:
        db_table = 'Deal'

    def __unicode__(self):
        return '%d: %s' % (self.user_take, self.deal_money)
