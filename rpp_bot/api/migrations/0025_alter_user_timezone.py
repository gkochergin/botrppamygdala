# Generated by Django 4.2.2 on 2023-06-20 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_user_marathon_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='timezone',
            field=models.CharField(default='UTC', help_text='Часовой пояс пользователя', max_length=10),
        ),
    ]
