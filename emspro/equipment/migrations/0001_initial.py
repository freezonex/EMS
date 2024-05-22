# Generated by Django 4.2.13 on 2024-05-21 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EnergySource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(default="default_type", max_length=100)),
                (
                    "supplier",
                    models.CharField(default="default_supplier", max_length=100),
                ),
                ("price", models.FloatField()),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Equipment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("type", models.CharField(default="default_type", max_length=100)),
                ("status", models.BooleanField(default=True)),
                (
                    "energy_type",
                    models.CharField(default="default_energy", max_length=100),
                ),
                ("rating", models.FloatField(default=0.0)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Workshop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "operator",
                    models.CharField(default="Unknown Operator", max_length=100),
                ),
                ("details", models.TextField(default="No details provided.")),
                ("status", models.CharField(default="Pending", max_length=100)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
                (
                    "equipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintenance_records",
                        to="equipment.equipment",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="equipment",
            name="workshop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="equipment",
                to="equipment.workshop",
            ),
        ),
        migrations.CreateModel(
            name="EnergyConsumption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("volume", models.FloatField(blank=True, null=True)),
                ("electric", models.FloatField(blank=True, null=True)),
                ("pressure", models.FloatField(blank=True, null=True)),
                ("temperature", models.FloatField(blank=True, null=True)),
                ("actual_rate", models.FloatField(blank=True, null=True)),
                ("standard_rate", models.FloatField(blank=True, null=True)),
                (
                    "energy_type",
                    models.CharField(default="Electricity", max_length=100),
                ),
                (
                    "energy_used",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
                (
                    "energysource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="equipment.energysource",
                    ),
                ),
                (
                    "equipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="consumptions",
                        to="equipment.equipment",
                    ),
                ),
            ],
        ),
    ]