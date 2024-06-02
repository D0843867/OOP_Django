"""
URL configuration for webproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import webblog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webblog.views.myhome),
    path('login/', webblog.views.login),
    path('menu/<int:orderid>', webblog.views.menu),
    path('menu/add_order', webblog.views.add_order),

    path('register/', webblog.views.register),
    path('add_menu/', webblog.views.add_menu),
    path('order_list/', webblog.views.add_menu),
    path('register/add/', webblog.views.register_add),
    path('login/check/', webblog.views.login_check),
    path('menu/set_takeout/', webblog.views.set_takeout),
    path('menu/drop_food/', webblog.views.drop_food),
    path('menu/change_amount/', webblog.views.change_amount),
    path('ordercompleted/', webblog.views.ordercompleted),
]
