# Generated by Django 3.0.5 on 2021-08-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0012_priscriptrion'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
