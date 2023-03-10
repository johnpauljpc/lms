# Generated by Django 4.0.6 on 2023-03-08 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_author_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_profile',
            field=models.ImageField(upload_to='Images/authors'),
        ),
        migrations.AlterField(
            model_name='course',
            name='featured_image',
            field=models.ImageField(null=True, upload_to='Images/featured_img'),
        ),
    ]
