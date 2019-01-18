from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SingUpForm, CustomUserChangeForm
from .models import (CustomUser, BloodGroup, ClinicAppointment,
                     HospitalAppointment, DiagnosticsTest, SellerProduct)


class CustomUserAdmin(UserAdmin):
    add_form = SingUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', ]


admin.site.register(CustomUser)
admin.site.register(BloodGroup)
admin.site.register(ClinicAppointment)
admin.site.register(HospitalAppointment)
admin.site.register(DiagnosticsTest)
admin.site.register(SellerProduct)
