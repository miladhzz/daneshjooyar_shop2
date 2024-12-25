# Generated by Django 4.2.11 on 2024-12-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PaymentLog",
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
                ("amount", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user_id", models.PositiveIntegerField()),
                ("order_id", models.PositiveIntegerField()),
                ("status", models.CharField(max_length=100)),
                ("error_code", models.CharField(max_length=200)),
            ],
        )
    ]
