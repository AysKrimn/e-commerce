# Generated by Django 4.1.1 on 2023-04-12 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urunApp', '0010_yorumlar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yorumlar',
            name='urun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yorumlar', to='urunApp.urun', verbose_name='Ürün'),
        ),
        migrations.AlterField(
            model_name='yorumlar',
            name='yazar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yazar'),
        ),
    ]
