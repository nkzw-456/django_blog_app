# Generated by Django 3.2.7 on 2021-09-14 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='images',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
