# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-29 17:06
from __future__ import unicode_literals

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_auto_20171030_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '640x480', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
