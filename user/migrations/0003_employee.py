# Generated by Django 3.2.7 on 2021-12-20 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_film'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=128)),
            ],
        ),
    ]
