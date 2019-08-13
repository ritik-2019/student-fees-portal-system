# Generated by Django 2.2.2 on 2019-07-05 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='photo',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logindata',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, verbose_name='Email Address '),
        ),
        migrations.AlterField(
            model_name='photodata',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, verbose_name='Email Address '),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.CharField(max_length=100),
        ),
    ]
