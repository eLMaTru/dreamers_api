# Generated by Django 3.1.2 on 2021-04-16 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreams', '0006_auto_20210219_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
