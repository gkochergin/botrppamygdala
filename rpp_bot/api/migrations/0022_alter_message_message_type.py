# Generated by Django 4.2.2 on 2023-06-18 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_message_message_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('ARTICLE', '📖 Статья'), ('LECTURE', '📺 Лекция'), ('MEDITATION', '🧘\u200d♀️ Медитация'), ('WORKOUT', '🏋️\u200d♀️ Упражнение')], default='ARTICLE', max_length=10),
        ),
    ]