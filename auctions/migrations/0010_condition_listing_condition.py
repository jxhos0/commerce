# Generated by Django 4.1.6 on 2023-02-27 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_end_datetime_alter_listing_starting_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_quality', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='condition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auctions.condition'),
        ),
    ]