# Generated by Django 3.1.2 on 2020-11-17 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('dreams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dream',
            name='is_voice',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dream',
            name='status',
            field=models.CharField(choices=[('enabled', 'enabled'), ('disable', 'disable'), ('delete', 'delete'), ('edited', 'edited')], default='ENABLED', max_length=25),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('enabled', 'enabled'), ('disable', 'disable'), ('delete', 'delete'), ('edited', 'edited')], default='ENABLED', max_length=25)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreams.dream')),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.useraccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
