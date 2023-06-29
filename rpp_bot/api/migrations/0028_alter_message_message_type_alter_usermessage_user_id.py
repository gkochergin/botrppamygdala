# Generated by Django 4.2.2 on 2023-06-23 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_alter_message_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('ARTICLE', '📖 Статья'), ('LECTURE', '📺 Лекция'), ('MEDITATION', '🧘\u200d♀️ Медитация'), ('WORKOUT', '🏋️\u200d♀️ Упражнение'), ('QUIZ', '✅ Тест')], default='ARTICLE', max_length=10),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='User'),
        ),
    ]