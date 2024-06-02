# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Food(models.Model):
    foodid = models.AutoField(primary_key=True)
    foodname = models.TextField()
    price = models.IntegerField()
    visible = models.IntegerField()
    soldout = models.IntegerField()
    amount = models.IntegerField()
    picture_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Food'


class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    account = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='account')
    completed = models.IntegerField()
    takeout = models.IntegerField()
    time = models.TextField()

    class Meta:
        managed = False
        db_table = 'Order'


class Orderdetail(models.Model):
    orderdetailid = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='orderid')
    foodid = models.ForeignKey(Food, models.DO_NOTHING, db_column='foodid')
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'OrderDetail'


class UserInfo(models.Model):
    account = models.TextField(primary_key=True)
    username = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    password = models.TextField()

    class Meta:
        managed = False
        db_table = 'User_info'
