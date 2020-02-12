# Generated by Django 2.2.9 on 2020-02-12 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest_game', '0006_auto_20200212_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='finished_respondent_investment',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='finished_user_investment',
        ),
        migrations.AddField(
            model_name='investment',
            name='started_compare',
            field=models.DateTimeField(help_text='When the user landed on the compare stage', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_experiment',
            field=models.DateTimeField(help_text='When the user landed on the welcome page', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_finish',
            field=models.DateTimeField(help_text='When the user landed on the finish stage, and completed the experiment', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_question_1',
            field=models.DateTimeField(help_text='When the user landed on the question 1 stage', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_question_1_5',
            field=models.DateTimeField(help_text='When the user landed on the question 1.5 stage (if relevant)', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_question_2',
            field=models.DateTimeField(help_text='When the user landed on the question 2 stage', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_question_3',
            field=models.DateTimeField(help_text='When the user landed on the question 3 stage', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='started_select_respondent',
            field=models.DateTimeField(help_text='When the user landed on the select respondent stage', null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='started_respondent_investment',
            field=models.DateTimeField(help_text='When the user landed on the respondent investment stage', null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='started_user_investment',
            field=models.DateTimeField(help_text='When the user landed on the user investment stage', null=True),
        ),
    ]