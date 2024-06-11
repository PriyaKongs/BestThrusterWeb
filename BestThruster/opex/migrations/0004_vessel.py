# Generated by Django 5.0.6 on 2024-06-11 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opex', '0003_alter_thruster_p_d_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vessel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('thrust_kn', models.JSONField(blank=True, null=True)),
                ('stw_knots', models.JSONField(blank=True, null=True)),
                ('hours', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
