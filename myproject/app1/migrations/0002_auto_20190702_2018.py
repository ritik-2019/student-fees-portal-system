# Generated by Django 2.2.2 on 2019-07-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admindata',
            name='id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='employee_email',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
