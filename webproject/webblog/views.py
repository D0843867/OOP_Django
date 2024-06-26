from django.shortcuts import render, HttpResponse, redirect
from django.db import connection, transaction
import datetime
from webblog import models
# Create your views here.

mycursor=connection.cursor()

#首頁
def myhome(request):
    # return render(request,"index.html",{"blog_name":"pzs123編成"})
    return redirect(login)
def login(request):
    now = datetime.datetime.now()  # 現在時間
    context = {'now': now}
    return render(request,"login.html",context)

def chackorder(orderid):
    # print(orderid)
    mycursor.execute('SELECT takeout FROM [Order] WHERE orderid = %s' % (orderid))
    takeout = mycursor.fetchall()[0][0]
    # print(takeout)
    # print(takeout == 0)
    foodid_list, amount_list = [], []
    mycursor.execute('SELECT foodid, amount FROM OrderDetail WHERE orderid = %s' % (orderid))
    for foodid, amount in mycursor.fetchall():
        foodid_list.append(foodid)
        amount_list.append(amount)

    foodname_list, picture_url_list, price_list = [], [], []
    total_price = 0
    for foodid, amount in zip(foodid_list, amount_list):
        mycursor.execute('SELECT foodname, picture_url, price FROM Food WHERE foodid = %s' % (foodid))
        foodname, picture_url, price = mycursor.fetchall()[0]
        foodname_list.append(foodname)
        picture_url_list.append(picture_url)
        price_list.append(price)
        total_price += price * amount

    context = {'takeout': takeout,
               'foodid_list': foodid_list,
               'amount_list': amount_list,
               'foodname_list': foodname_list,
               'picture_url_list': picture_url_list,
               'price_list': price_list,
               'total_price': total_price, }
    print(context)
    return context

def menu(request, orderid):
    #print(orderid)
    mycursor.execute('SELECT * FROM Food WHERE visible = 1')
    foodlist = mycursor.fetchall()
    mycursor.execute('SELECT f.foodname, od.amount, f.price,od.orderdetailid FROM OrderDetail od JOIN Food f ON od.foodid = f.foodid WHERE od.orderid = %s;',(orderid,))
    alreadylist = mycursor.fetchall()
    context = {'foodlist': foodlist,
               'orderid': orderid,
               'alreadylist':alreadylist}
    context.update(chackorder(orderid))
    return render(request, 'menu.html', context)

def ordercompleted(request):
    orderid = request.POST.get('orderid')
    times = datetime.datetime.now()
    mycursor.execute('UPDATE [Order] SET completed = 1, time = "%s" WHERE orderid = %s' % (times, orderid))

    mycursor.execute('SELECT account FROM [order] WHERE orderid = %s limit 1' % (orderid))
    account = mycursor.fetchall()[0][0]
    print(account)

    mycursor.execute('SELECT * FROM Food WHERE visible = 1')
    foodlist = mycursor.fetchall()
    mycursor.execute(
        'SELECT f.foodname, od.amount, f.price,od.orderdetailid FROM OrderDetail od JOIN Food f ON od.foodid = f.foodid WHERE od.orderid = %s;',
        (orderid,))
    alreadylist = mycursor.fetchall()
    context = {'foodlist': foodlist,
               'orderid': orderid,
               'alreadylist': alreadylist,
               'times':times,
               'account':account}
    context.update(chackorder(orderid))
    return render(request, 'ordercompleted.html', context)

def set_takeout(request):
    orderid = request.POST.get('orderid')
    takeout = request.POST.get('takeout')
    mycursor.execute('UPDATE [Order] SET takeout = %s WHERE orderid = %s' % (takeout, orderid))
    return redirect('/menu/%s' % orderid)

def drop_food(request):
    orderid = request.POST.get('orderid')
    orderdetailid = request.POST.get('orderdetailid')
    mycursor.execute('DELETE FROM OrderDetail WHERE orderid = %s AND orderdetailid = %s' % (orderid, orderdetailid))
    return redirect('/menu/%s' % orderid)

def change_amount(request):
    orderid = request.POST.get('orderid')
    foodid = request.POST.get('foodid')
    amount = request.POST.get('amount')
    mycursor.execute('UPDATE OrderDetail SET amount = %s WHERE orderid = %s AND foodid = %s' % (orderid, foodid))
    return redirect('/menu/%s' % orderid)

def add_order(request):
    orderid = request.POST.get('orderid')
    foodid = request.POST.get('foodid')
    amount = request.POST.get('amount')
    # print(orderid)
    # print(foodid)
    print(amount)
    if int(amount) > 0:
        mycursor.execute('INSERT INTO OrderDetail VALUES (null , %s, %s, %s)' % (orderid, foodid, amount))
    return redirect('/menu/%s' % orderid)

# ======================change menu============================

def change_menu(request):
    foodlist = models.Food.objects.filter(visible=1)
    return render(request, "change_menu.html", {'foodlist': foodlist})

def update_menu(request):
    if request.method == 'POST':
        with transaction.atomic():  # 確保所有更改都在單一事務中進行
            for key, value in request.POST.items():
                if key.startswith('delete_'):
                    food_id = key.split('_')[1]
                    if value == 'on':
                        models.Food.objects.filter(foodid=food_id).update(visible=0)
                        continue

                elif key.startswith('foodname_'):
                    food_id = key.split('_')[1]
                    picture_url = request.POST.get(f'picture_url_{food_id}')
                    foodname = value
                    price = request.POST.get(f'price_{food_id}')
                    soldout = request.POST.get(f'soldout_{food_id}', 'off') == 'on'

                    models.Food.objects.filter(foodid=food_id).update(
                        picture_url=picture_url,
                        foodname=foodname,
                        price=price,
                        amount=10,
                        soldout=soldout
                    )

    return redirect('/change_menu/')

def delete_menu(request):
    foodid = request.POST.get('foodid')
    # print('foodid:', foodid)
    models.Food.objects.filter(foodid=foodid).update(visible=0)
    return redirect('/change_menu/')

def add_menu(request):
    foodname = request.POST.get('foodname')
    price = request.POST.get('price')
    picture_url = request.POST.get('picture_url')
    # print('foodname:', foodname)
    # print('price:', price)
    # print('picture_url:', picture_url)
    models.Food(
        foodname=foodname,
        price=price,
        visible=1,
        soldout=0,
        amount=10,  # 待刪
        picture_url=picture_url
    ).save()
    return redirect('/change_menu/')

#==============================================================

def register(request):
    now = datetime.datetime.now()  # 現在時間
    context = {'now': now}
    return render(request,"register.html",context)

def order_list(request):
    now = datetime.datetime.now()  # 現在時間
    context = {'now': now}
    return render(request,"order_list.html",context)
def register_add(request):
    account = request.POST['account']
    username = request.POST['username']
    phone = request.POST['phone']
    password = request.POST['password']
    print('account:(', account, ')')
    print('username:(', username, ')')
    print('phone:(', phone, ')')
    print('password:(', password, ')')
    try:
        phone = int(phone)
    except ValueError:
        phone = None

    if account and password:
        # mycursor.execute('INSERT INTO User_info (account, password, username, phone) VALUES (%s, %s, %s, %s)',(account, password, username, phone))
        models.UserInfo(account, username, phone, password).save()
        # return HttpResponse("註冊成功")
        return redirect(login)
    elif account and not password:
        return HttpResponse("密碼未輸入")
    elif password and not account:
        return HttpResponse("帳號未輸入")
    else:
        return HttpResponse("帳號和密碼均未輸入")
def login_check(request):
    login_account = request.POST.get('account')
    login_password = request.POST.get('password')

    if not login_account or not login_password:
        if not login_account and not login_password:
            return HttpResponse("請輸入帳號密碼")
        elif not login_account:
            return HttpResponse("請輸入帳號")
        else:
            return HttpResponse("請輸入密碼")

    print(login_account, login_password)

    mycursor.execute('SELECT account, password FROM User_info')
    for acc, passw in mycursor.fetchall():
        print("acc", acc, "passw", passw)
        if login_account == acc and login_password == passw:

            cursor = connection.cursor()
            sql = 'INSERT INTO [Order] (account, completed, takeout, time) VALUES (%s, %s, %s, %s)'
            params = (login_account, 0, 0, datetime.datetime.now())
            cursor.execute(sql, params)

            #mycursor.execute('INSERT INTO [Order] VALUES (null , %s, %s, %s, "%s")' % (login_account, 0, 0, datetime.datetime.now()))

            cursor1 = connection.cursor()
            sql = 'SELECT orderid FROM "Order" WHERE account = %s ORDER BY orderid DESC LIMIT 1'
            params = (login_account,)
            cursor1.execute(sql, params)

            #mycursor.execute('SELECT orderid FROM [Order] WHERE account = %s ORDER BY orderid DESC limit 1' % (login_account))

            orderid = cursor1.fetchall()[0]
            # context = {'orderid': orderid}
            # print(context)
            # return HttpResponse("登錄成功")
            if acc == "admin":
                return redirect('/change_menu/')
            else:
                return redirect('/menu/%s' % orderid)
    return HttpResponse("帳號或密碼錯誤")