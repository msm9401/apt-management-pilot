# Generated by Django 4.1 on 2023-08-19 13:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medias", "0002_alter_photo_table_alter_video_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="file",
            field=models.FileField(upload_to=""),
        ),
    ]
