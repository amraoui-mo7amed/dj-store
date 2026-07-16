from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_alter_stock_uuid'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                'DROP TABLE IF EXISTS dashboard_event CASCADE;',
                'DROP TABLE IF EXISTS dashboard_subscriber CASCADE;',
            ],
            reverse_sql=[
                'CREATE TABLE dashboard_event (id serial primary key);',
                'CREATE TABLE dashboard_subscriber (id serial primary key);',
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='ref_code',
            field=models.CharField(default='', editable=False, max_length=8),
        ),
        migrations.AlterField(
            model_name='stock',
            name='uuid',
            field=models.CharField(default='89537b', editable=False, max_length=6, unique=True),
        ),
    ]
