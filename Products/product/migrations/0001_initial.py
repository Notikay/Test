# Generated by Django 3.0.4 on 2020-03-10 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название товара')),
                ('price', models.PositiveIntegerField(default=0, help_text='Указывать сумму в рублях', verbose_name='Цена')),
                ('type_product', models.CharField(choices=[('TOP', 'Верх'), ('BOTTOM', 'Низ'), ('UNDEFINED', 'Не выбран')], max_length=50, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]