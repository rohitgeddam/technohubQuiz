# Generated by Django 3.1.1 on 2020-10-14 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0008_auto_20201014_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztaker',
            name='completion_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]