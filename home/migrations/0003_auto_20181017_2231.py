# Generated by Django 2.1.2 on 2018-10-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20181017_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='self_care',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]