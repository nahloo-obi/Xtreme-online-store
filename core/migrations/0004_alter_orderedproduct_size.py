# Generated by Django 4.1.1 on 2022-09-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_orderedproduct_colour_orderedproduct_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='size',
            field=models.CharField(max_length=4),
        ),
    ]
