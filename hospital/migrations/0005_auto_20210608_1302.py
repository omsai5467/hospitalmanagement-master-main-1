# Generated by Django 3.0.5 on 2021-06-08 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_auto_20210527_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='Patient_type_1',
            field=models.CharField(choices=[('pretreatment', 'pretreatment'), ('Registrationcount', 'Registrationcount'), ('Preauthorisation', 'Preauthorisation'), ('Dischargestate', 'Dischargestate'), ('Claimphase', 'Claimphase'), ('surgery_update', 'surgery_update')], max_length=50),
        ),
    ]
