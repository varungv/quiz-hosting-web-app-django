# Generated by Django 2.0.4 on 2018-08-02 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0013_remove_questionstable_test_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionstable',
            name='Option_1',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_2',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_3',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Option_4',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Question',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='questionstable',
            name='Solution_Explanation',
            field=models.TextField(max_length=1000),
        ),
    ]
