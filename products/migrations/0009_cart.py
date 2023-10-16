# Generated by Django 4.0.4 on 2023-10-16 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_formmodel_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('user_product_quantity', models.IntegerField()),
                ('user_add_date', models.DateTimeField(auto_now_add=True)),
                ('user_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productmodel')),
            ],
        ),
    ]