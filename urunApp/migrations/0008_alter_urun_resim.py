# Generated by Django 4.1.1 on 2023-04-03 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunApp', '0007_alter_urun_resim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urun',
            name='resim',
            field=models.FileField(blank=True, default='../static/public/no-image.jpg', null=True, upload_to='uploads', verbose_name='Resim'),
        ),
    ]
