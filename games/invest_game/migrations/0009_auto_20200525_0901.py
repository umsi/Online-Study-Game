# Generated by Django 2.2.9 on 2020-05-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest_game', '0008_investment_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='started_question_5',
            field=models.DateTimeField(help_text='When the user landed on the question 5 stage', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_address_1',
            field=models.TextField(help_text='Street Address', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_address_2',
            field=models.TextField(help_text='Street Address 2', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_city',
            field=models.TextField(help_text='User City', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_name',
            field=models.TextField(help_text='Name', null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_state',
            field=models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Deleware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('AS', 'American Samoa'), ('GU', 'Guam'), ('MH', 'Marshall Islands'), ('FM', 'Micronesia'), ('MP', 'Northern Marianas'), ('PW', 'Palau'), ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands')], help_text='User State', max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='user_zip',
            field=models.TextField(help_text='User Zip Code', null=True),
        ),
    ]
