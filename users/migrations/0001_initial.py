# Generated by Django 5.0 on 2024-03-20 21:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kullanici',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=50)),
                ('soyisim', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100, null=True)),
                ('resim', models.FileField(upload_to='kullanicilar/', verbose_name='Profil Resmi')),
                ('tel', models.IntegerField(default=0)),
                ('dogum', models.DateField()),
                ('olusturulma_tarih', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
