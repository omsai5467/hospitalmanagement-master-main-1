# Generated by Django 3.0.5 on 2021-07-27 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_test4_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test4',
            name='name',
        ),
        migrations.CreateModel(
            name='names',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('testname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.test4')),
            ],
        ),
    ]
