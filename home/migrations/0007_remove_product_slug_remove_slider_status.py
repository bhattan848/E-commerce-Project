# Generated by Django 4.0.4 on 2022-04-25 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_slider_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='slider',
            name='status',
        ),
    ]