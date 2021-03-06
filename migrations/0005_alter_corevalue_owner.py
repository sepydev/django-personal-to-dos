# Generated by Django 4.0.1 on 2022-02-17 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personal_to_dos', '0004_rename_user_corevalue_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corevalue',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_owner', related_query_name='%(app_label)s_%(class)s_owners', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
