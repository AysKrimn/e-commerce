# Generated by Django 4.1.1 on 2023-04-17 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunApp', '0014_alter_creditcardaccount_cardno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcardaccount',
            name='cardNo',
            field=models.CharField(max_length=19, verbose_name='Kart Numarası'),
        ),
    ]