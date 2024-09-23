from django.contrib import admin
from UserApp.models import Payment
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','cardno','cvv','expiry','balance')


admin.site.register(Payment,PaymentAdmin)
