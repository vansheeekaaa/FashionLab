from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trends', '0002_designsubmission_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_scores', models.JSONField(blank=True, null=True)),
                ('closet_items', models.ManyToManyField(related_name='users_with_in_closet', to='trends.designsubmission')),
            ],
        ),
    ]
