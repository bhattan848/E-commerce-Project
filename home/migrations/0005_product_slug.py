# Generated by Django 4.0.4 on 2022-04-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_ad_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]