# Generated by Django 4.2.2 on 2023-06-08 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0014_alter_message_ordinal_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='ordinal_number',
            field=models.IntegerField(help_text='Порядковый номер отправки (уникальный)'),
        ),
    ]
