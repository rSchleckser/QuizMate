from django.db import migrations, models


def normalize_correct_option(apps, schema_editor):
    Question = apps.get_model('courses', 'Question')
    for question in Question.objects.exclude(correct_option__in=['1', '2', '3', '4']):
        question.correct_option = '1'
        question.save(update_fields=['correct_option'])


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_enrollment_grade'),
    ]

    operations = [
        migrations.RunPython(normalize_correct_option, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')],
                default=1,
            ),
        ),
    ]
