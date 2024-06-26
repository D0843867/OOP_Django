# Generated by Django 4.2.3 on 2024-06-02 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Food",
            fields=[
                ("foodid", models.AutoField(primary_key=True, serialize=False)),
                ("foodname", models.TextField()),
                ("price", models.IntegerField()),
                ("visible", models.IntegerField()),
                ("soldout", models.IntegerField()),
                ("amount", models.IntegerField()),
                ("picture_url", models.TextField(blank=True, null=True)),
            ],
            options={"db_table": "Food", "managed": False,},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("orderid", models.AutoField(primary_key=True, serialize=False)),
                ("completed", models.IntegerField()),
                ("takeout", models.IntegerField()),
                ("time", models.TextField()),
            ],
            options={"db_table": "Order", "managed": False,},
        ),
        migrations.CreateModel(
            name="Orderdetail",
            fields=[
                ("orderdetailid", models.AutoField(primary_key=True, serialize=False)),
                ("amount", models.IntegerField()),
            ],
            options={"db_table": "OrderDetail", "managed": False,},
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                ("account", models.TextField(primary_key=True, serialize=False)),
                ("username", models.TextField(blank=True, null=True)),
                ("phone", models.IntegerField(blank=True, null=True)),
                ("password", models.TextField()),
            ],
            options={"db_table": "User_info", "managed": False,},
        ),
    ]
