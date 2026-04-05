from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0002_remove_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.PROTECT,
                to='user.city',
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='celular',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
