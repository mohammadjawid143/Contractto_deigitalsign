# Generated by Django 5.1.3 on 2024-12-06 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_remove_contract_signature1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contract_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
