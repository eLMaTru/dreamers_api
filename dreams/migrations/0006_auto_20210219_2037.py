# Generated by Django 3.1.2 on 2021-02-19 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreams', '0005_auto_20210127_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='dream',
            name='title',
            field=models.CharField(blank=True, default='', max_length=101, null=True),
        ),
    ]
