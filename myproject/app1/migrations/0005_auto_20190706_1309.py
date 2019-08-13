# Generated by Django 2.2.2 on 2019-07-06 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_auto_20190705_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='feesrecord',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, verbose_name='Email Address')),
                ('depositby', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='student',
            old_name='fees_left',
            new_name='fees_dep',
        ),
    ]
