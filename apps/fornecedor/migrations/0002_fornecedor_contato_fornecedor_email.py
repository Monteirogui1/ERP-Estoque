# Generated by Django 5.1.7 on 2025-03-31 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='contato',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
