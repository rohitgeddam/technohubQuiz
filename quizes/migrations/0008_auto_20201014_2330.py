# Generated by Django 3.1.1 on 2020-10-14 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0007_quiztaker_completion_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztaker',
            name='completion_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
