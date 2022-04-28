# Generated by Django 4.0.2 on 2022-04-19 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('exit_time', models.DateTimeField(auto_now_add=True)),
                ('total_bill', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('parking_id', models.AutoField(primary_key=True, serialize=False)),
                ('slot_number', models.IntegerField()),
                ('occupied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('slot_allotted', models.IntegerField()),
                ('ticket_issued', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.CharField(max_length=250)),
                ('citizenship_id', models.BigIntegerField(default=0)),
                ('pan_no', models.IntegerField(default=0)),
                ('avatar', models.ImageField(default='default.png', upload_to='profile_picture/')),
                ('citizenship', models.FileField(default='citizen_default.jpg', upload_to='citizenship/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_payment', models.FloatField()),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpayed')], default='Unpaid', max_length=25)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Parking.bill')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('colour', models.CharField(max_length=25)),
                ('numberplate', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Parked', 'Parked'), ('Departed', 'Departed')], default='Departed', max_length=25)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ticket', to='Parking.ticket')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Parking.ticket'),
        ),
    ]