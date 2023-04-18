# Generated by Django 4.1.1 on 2023-04-14 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urunApp', '0011_alter_yorumlar_urun_alter_yorumlar_yazar'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='olusturan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ürünü Oluşturan'),
        ),
    ]
