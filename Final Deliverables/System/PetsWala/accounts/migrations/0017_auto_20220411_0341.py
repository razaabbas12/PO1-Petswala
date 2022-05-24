# Generated by Django 3.2.9 on 2022-04-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20220409_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='geolocation',
        ),
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='address',
            name='lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='request',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.TextField(),
        ),
    ]