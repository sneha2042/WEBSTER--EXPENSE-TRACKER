# Generated by Django 3.2.8 on 2021-12-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_profile_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]