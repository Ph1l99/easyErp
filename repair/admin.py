from django.contrib import admin

from repair.models import RepairStatus, Repair


class RepairStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'is_active', 'order', 'class_name')


class RepairAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'title', 'delivery_date', 'insert_date_time')


admin.site.register(RepairStatus, RepairStatusAdmin)
admin.site.register(Repair, RepairAdmin)
