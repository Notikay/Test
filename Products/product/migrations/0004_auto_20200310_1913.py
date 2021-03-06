# Generated by Django 3.0.4 on 2020-03-10 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_set_top'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='bottom',
            field=models.ForeignKey(default='', limit_choices_to={'type_product': 'BOTTOM'}, on_delete=django.db.models.deletion.CASCADE, related_name='bottom', to='product.Production'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='set',
            name='top',
            field=models.ForeignKey(limit_choices_to={'type_product': 'TOP'}, on_delete=django.db.models.deletion.CASCADE, related_name='set', to='product.Production'),
        ),
    ]
