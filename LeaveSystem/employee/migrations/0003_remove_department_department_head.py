# Generated by Django 4.2.4 on 2023-08-16 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0002_department_department_head"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="department",
            name="department_head",
        ),
    ]
