# Generated by Django 2.0.4 on 2018-06-21 19:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0007_remove_usertestjunction_marks_obtained'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextensiontable',
            name='Student',
            field=models.ForeignKey(on_delete='CASCADE', to=settings.AUTH_USER_MODEL),
        ),
    ]