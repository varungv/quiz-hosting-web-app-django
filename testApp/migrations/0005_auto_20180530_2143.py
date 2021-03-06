# Generated by Django 2.0.4 on 2018-05-30 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0004_auto_20180530_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtable',
            name='Positive_mark',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='testtable',
            name='negative_mark',
            field=models.FloatField(default=0.25),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Correct_option',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=4),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_1',
            field=models.CharField(default='Option 1', max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_2',
            field=models.CharField(default='Option 2', max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_3',
            field=models.CharField(default='Option 3', max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_4',
            field=models.CharField(default='Option 4 Correct', max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Question',
            field=models.CharField(default='Test 1, Subject 4, Question 16', max_length=500),
        ),
    ]
