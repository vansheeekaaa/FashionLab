from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trends", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="designsubmission",
            name="votes",
            field=models.IntegerField(default=0),
        ),
    ]
