# Generated by Django 3.2.8 on 2021-12-04 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='expenses',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='expense',
            name='expense_type',
            field=models.CharField(choices=[('Positive', 'Positive'), ('Negative', 'Negative')], max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
