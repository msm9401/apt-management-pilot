# Generated by Django 4.1 on 2023-07-01 11:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="choice",
            table="choice",
        ),
        migrations.AlterModelTable(
            name="question",
            table="question",
        ),
    ]
