from django.contrib import admin
from  .models  import Cake,Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','cname')

class CakeAdmin(admin.ModelAdmin):
    list_display= ('id','cake_name','price','quantity','image_url','cat_id')

admin.site.register(Cake,CakeAdmin)
admin.site.register(Category,CategoryAdmin)
