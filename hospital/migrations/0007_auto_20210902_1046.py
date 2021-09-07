# Generated by Django 3.0.5 on 2021-09-02 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0006_auto_20210902_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpatient',
            name='history_change_reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]