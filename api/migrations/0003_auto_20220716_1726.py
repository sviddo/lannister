# Generated by Django 3.2.14 on 2022-07-16 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220715_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('c', 'Created'), ('a', 'Approved'), ('r', 'Rejected'), ('p', 'Paid')], default='c', max_length=1),
        ),
        migrations.AlterField(
            model_name='requesthistory',
            name='type_of_change',
            field=models.CharField(choices=[('c', 'Created'), ('a', 'Approved'), ('r', 'Rejected'), ('p', 'Paid'), ('e', 'Edited')], default='c', max_length=1),
        ),
    ]