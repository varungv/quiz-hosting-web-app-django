# Generated by Django 2.0.4 on 2018-05-30 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0005_auto_20180530_2143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testtable',
            old_name='negative_mark',
            new_name='Negative_mark',
        ),
        migrations.AddField(
            model_name='usertestjunction',
            name='marks_obtained',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='usertestquestionjunction',
            name='result',
            field=models.IntegerField(),
        ),
    ]
