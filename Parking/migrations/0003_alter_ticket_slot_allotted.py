# Generated by Django 4.0.2 on 2022-04-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parking', '0002_alter_ticket_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='slot_allotted',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]