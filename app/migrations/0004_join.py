# Generated by Django 5.1.4 on 2025-06-07 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_course_cimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simage', models.ImageField(upload_to='media/')),
            ],
        ),
    ]
