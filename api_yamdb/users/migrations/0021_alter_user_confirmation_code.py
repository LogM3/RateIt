# Generated by Django 3.2 on 2023-01-11 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='093135b5-bec2-4b8f-9129-d16eceafae44', editable=False, max_length=40),
        ),
    ]
