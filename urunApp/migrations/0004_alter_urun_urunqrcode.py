# Generated by Django 4.1.1 on 2023-03-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunApp', '0003_urun_urunqrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urun',
            name='urunQRCode',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Ürünün QR Kod Numarası'),
        ),
    ]
