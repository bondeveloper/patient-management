# Generated by Django 4.2.7 on 2023-11-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_consultation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='patient_type',
            field=models.CharField(choices=[('in', 'In Patient'), ('out', 'Out Patient')], max_length=10),
        ),
    ]