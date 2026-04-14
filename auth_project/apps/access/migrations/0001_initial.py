from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="BusinessElement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="AccessRoleRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rules", to="access.role")),
                ("element", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rules", to="access.businesselement")),
                ("read_permission", models.BooleanField(default=False)),
                ("read_all_permission", models.BooleanField(default=False)),
                ("create_permission", models.BooleanField(default=False)),
                ("update_permission", models.BooleanField(default=False)),
                ("update_all_permission", models.BooleanField(default=False)),
                ("delete_permission", models.BooleanField(default=False)),
                ("delete_all_permission", models.BooleanField(default=False)),
            ],
            options={"unique_together": {("role", "element")}},
        ),
    ]
