from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("access", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("middle_name", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("role", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="users", to="access.role")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TokenBlacklist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.TextField(unique=True)),
                ("blacklisted_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
