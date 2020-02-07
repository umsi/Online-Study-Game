# Generated by Django 2.2.9 on 2020-02-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest_game', '0003_auto_20200206_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='donereturn',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='returned0',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='returned1',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='returned2',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='returned3',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='returned4',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='returned5',
        ),
        migrations.AddField(
            model_name='investment',
            name='respondent_investment',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_bonus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_received',
            field=models.IntegerField(null=True),
        ),
    ]