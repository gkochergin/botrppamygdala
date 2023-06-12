# Generated by Django 4.2.2 on 2023-06-10 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_message_ordinal_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата первой активации бота', verbose_name='Registration date'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='message_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.message'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='sent_at',
            field=models.DateTimeField(help_text='Дата, когда было отправлено сообщение', verbose_name='Sending date & time'),
        ),
    ]