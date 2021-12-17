# Generated by Django 3.2.7 on 2021-12-17 12:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('users', models.ManyToManyField(related_name='films', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
