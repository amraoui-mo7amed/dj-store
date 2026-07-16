from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_remove_event_subscriber_add_refcode'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AssociationRegistration',
        ),
        migrations.DeleteModel(
            name='NewsletterSubscription',
        ),
        migrations.AlterField(
            model_name='stock',
            name='uuid',
            field=models.CharField(default='7d016f', editable=False, max_length=6, unique=True),
        ),
    ]
