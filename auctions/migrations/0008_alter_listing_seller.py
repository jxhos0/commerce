# Generated by Django 4.1.6 on 2023-02-25 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_listing_end_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
