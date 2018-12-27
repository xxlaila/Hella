# Generated by Django 2.1.1 on 2018-12-19 09:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='department',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='mobile',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='手机'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sex',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32),
        ),
    ]
