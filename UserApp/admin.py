from django.contrib import admin
from UserApp.models import *
# Register your models here.



admin.site.register(Users)
admin.site.register(DishCategory)
admin.site.register(DishSubCategory)
admin.site.register(Dish)