from django.contrib import admin
from .models import GroupMaster, Requisition, DailySub, Offer

# Register your models here.
admin.site.register(GroupMaster)
admin.site.register(DailySub)
admin.site.register(Offer)
admin.site.register(Requisition)