# Generated by Django 2.0.4 on 2018-07-10 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0012_remove_userextensiontable_last_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionstable',
            name='Test_Name',
        ),
    ]
