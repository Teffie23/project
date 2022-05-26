from django.db import models
from django.urls import reverse
from robokassa.signals import result_received
from django.dispatch import receiver
class user(models.Model):
    name = models.CharField(max_length=255, verbose_name='Фио')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания абонеменнта')
    slug = models.SlugField(max_length=255, unique=False, db_index=True, verbose_name='URL')
    time_update = models.DateTimeField(auto_now=True, verbose_name='время последнего посещения')
    num_scaf = models.ForeignKey('scaf', on_delete=models.PROTECT, null=True, verbose_name='Номер занимаемого шкафа')
    trainer = models.ForeignKey('trainer', on_delete=models.PROTECT, null=True, verbose_name='тренажёр')
    tarif=models.ForeignKey('tarif',on_delete=models.PROTECT,null=True,verbose_name='тариф')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Посетители'
        verbose_name_plural = verbose_name
        ordering = ['name', 'time_create']


class trainer(models.Model):
    name_train = models.CharField(max_length=255, db_index=True, verbose_name='Название тренажора')
    statuss= models.BooleanField(default=True, verbose_name='Состояние тренажёра')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name_train

    def get_absolute_url(self):
        return reverse('train', kwargs={'train_slug': self.slug})

    class Meta:
        verbose_name = 'Тренажёры'
        verbose_name_plural = verbose_name
        ordering = ['id']


class scaf(models.Model):
    is_blocks = models.BooleanField(default=True, verbose_name='Состояие шкафа')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('scafs', kwargs={'scafs_slug': self.slug})

    class Meta:
        verbose_name = 'Шкафы'
        verbose_name_plural = verbose_name
        ordering = ['id']
class tarif(models.Model):
    name_tarif=models.CharField(max_length=255, verbose_name='Имя Тарифа')
    time_active=models.IntegerField(verbose_name='Срок активности')
    bye=models.FloatField(verbose_name='Цена')
    total=models.FloatField( blank=True, null=True,verbose_name='Количество денег')
    status = models.CharField(max_length=255, blank=True, null=True)
    extra_param = models.CharField(max_length=255, blank=True, null=True)
    slug= models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return str(self.name_tarif)

    def get_absolute_url(self):
        return reverse('tarif', kwargs={'tarif_slug': self.slug})

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = verbose_name
        ordering = ['id','bye']
@receiver(result_received)
def payment_recived(sender,**kwargs):
    order=tarif.objects.get(pk=kwargs['InvId'])
    order.status='paid'
    order.bye=kwargs['OutSum']
    order.extra_param=kwargs['extra']['my_param']
    order.save()
# Create your models here.
