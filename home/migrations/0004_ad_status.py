# Generated by Django 4.0.4 on 2022-04-20 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_produc_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'active'), ('', 'default')], max_length=100),
        ),
    ]
