# Generated by Django 5.0.7 on 2024-08-08 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_question_correct_option_question_option1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.CharField(default='Answer', max_length=100),
        ),
    ]
