# Generated by Django 2.2 on 2019-05-09 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
