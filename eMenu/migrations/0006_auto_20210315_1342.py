# Generated by Django 3.1.7 on 2021-03-15 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eMenu', '0005_auto_20210312_1256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'ordering': ['-price', 'name']},
        ),
        migrations.AddField(
            model_name='note',
            name='add_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
