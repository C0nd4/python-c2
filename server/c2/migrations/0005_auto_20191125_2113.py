# Generated by Django 2.2.7 on 2019-11-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c2', '0004_auto_20191125_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='arguments',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]