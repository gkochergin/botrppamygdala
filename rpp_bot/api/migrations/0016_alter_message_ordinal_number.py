# Generated by Django 4.2.2 on 2023-06-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_message_ordinal_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='ordinal_number',
            field=models.IntegerField(default=1, help_text='Порядковый номер отправки (уникальный)'),
        ),
    ]
