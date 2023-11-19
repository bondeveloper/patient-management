# Generated by Django 4.2.7 on 2023-11-18 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinic', '0003_medicalstaff_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalstaff',
            name='province',
        ),
        migrations.AddField(
            model_name='medicalstaff',
            name='department',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]