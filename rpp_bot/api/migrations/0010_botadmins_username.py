# Generated by Django 4.2.2 on 2023-06-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_botadmins_user_id_alter_user_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='botadmins',
            name='username',
            field=models.CharField(default='', max_length=255, verbose_name='Telegram username'),
        ),
    ]
