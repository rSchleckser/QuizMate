# Generated by Django 5.0.7 on 2024-08-07 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_question_correct_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_option',
            field=models.CharField(default='correct Choice', max_length=100),
        ),
        migrations.AddField(
            model_name='question',
            name='option1',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='option2',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='option3',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='option4',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='courses.course'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
    ]
