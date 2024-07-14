from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trends', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
