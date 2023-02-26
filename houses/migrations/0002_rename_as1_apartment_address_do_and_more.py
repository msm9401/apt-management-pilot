# Generated by Django 4.1 on 2023-01-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartment',
            old_name='as1',
            new_name='address_do',
        ),
        migrations.RenameField(
            model_name='apartment',
            old_name='as3',
            new_name='address_dong',
        ),
        migrations.RenameField(
            model_name='apartment',
            old_name='as2',
            new_name='address_si',
        ),
        migrations.RenameField(
            model_name='apartment',
            old_name='bjdCode',
            new_name='bjd_code',
        ),
        migrations.RenameField(
            model_name='apartment',
            old_name='kaptCode',
            new_name='kapt_code',
        ),
        migrations.RenameField(
            model_name='apartment',
            old_name='kaptName',
            new_name='kapt_name',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='as4',
        ),
        migrations.AddField(
            model_name='apartment',
            name='address_li',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]