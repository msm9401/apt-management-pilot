# Generated by Django 4.1 on 2023-01-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('as1', models.CharField(max_length=200)),
                ('as2', models.CharField(max_length=200)),
                ('as3', models.CharField(max_length=200)),
                ('as4', models.CharField(blank=True, max_length=200, null=True)),
                ('bjdCode', models.CharField(max_length=200)),
                ('kaptCode', models.CharField(max_length=200)),
                ('kaptName', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
