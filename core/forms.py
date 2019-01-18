from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (CustomUser, ClinicAppointment, HospitalAppointment,
                     DiagnosticsTest, SellerProduct, BloodGroup, BuyerUserDetails)
from django.contrib.auth.models import Group
from django import forms
from .mixins import RequestKwargModelFormMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class UserLoginForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    # error_messages = {
    #     **AuthenticationForm.error_messages,
    #     'invalid_login': _(
    #         "Please enter the correct %(username)s and password for a staff "
    #         "account. Note that both fields may be case-sensitive."
    #     ),
    # }
    # required_css_class = 'required'

    # def confirm_login_allowed(self, user):
    #     super().confirm_login_allowed(user)
    #     if not user.is_staff:
    #         raise forms.ValidationError(
    #             self.error_messages['invalid_login'],
    #             code='invalid_login',
    #             params={'username': self.username_field.verbose_name}
    #         )


class UserPasswordChangeForm(PasswordChangeForm):
    required_css_class = 'required'


class SingUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "user_type"]
        # widgets = {
        #     "user_type": forms.ChoiceField(),
        # }

    def create_group(self, user):
        if user.user_type == "HS":
            group, created = Group.objects.get_or_create(name="Hospital")
            content_type = ContentType.objects.get_for_model(HospitalAppointment)
        elif user.user_type == "SE":
            group, created = Group.objects.get_or_create(name="Seller")
            content_type = ContentType.objects.get_for_model(BloodGroup)

        elif user.user_type == "BR":
            group, created = Group.objects.get_or_create(name="Buyer")
            content_type = ContentType.objects.get_for_model(BuyerUserDetails)

        elif user.user_type == "BB":
            BloodGroup.objects.create(blood=user)
            content_type = ContentType.objects.get_for_model(BloodGroup)
            group, created = Group.objects.get_or_create(name="Blood bank")
        elif user.user_type == "CL":
            group, created = Group.objects.get_or_create(name="Clinic")
            content_type = ContentType.objects.get_for_model(ClinicAppointment)
        elif user.user_type == "DG":
            content_type = ContentType.objects.get_for_model(DiagnosticsTest)
            group, created = Group.objects.get_or_create(name="Diagnostics")
        permission1, created = Permission.objects.get_or_create(
            codename='custom_can_view',
            name='custom can view',
            content_type=content_type)
        permission2, created = Permission.objects.get_or_create(
            codename='custom_can_add',
            name='custom can add',
            content_type=content_type)
        user.groups.add(group)
        group.permissions.add(permission1)
        group.permissions.add(permission2)
        return group

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user_type = self.cleaned_data.get("user_type")
        user.user_type = user_type
        if commit:
            user.save()
            group = self.create_group(user)
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)


class CreateSraffUserForm(RequestKwargModelFormMixin, UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", )

    def assing_group(self, user):
        # user_type = user.user_type
        group_name = "staff"
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return group

    # def add_test_permission(self, md):
    #     content_type = ContentType.objects.get_for_model(md)
    #     permission = Permission.objects.create(codename='can_add_test',
    #                                            name='Can Add Text',
    #                                            content_type=content_type)
    #     return permission

    def add_perm(self, user, codename, name):
        if user.user_type == "DG":
            content_type = ContentType.objects.get_for_model(DiagnosticsTest)
            permission, created = Permission.objects.get_or_create(codename=codename,
                                                                   name=name,
                                                                   content_type=content_type)
        user.user_permissions.add(permission)
        user.save()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "staff user"
        user.staff_user = True
        user.staffof = self.request.user
        if commit:
            print(self.request.user)
            user.save()
        # self.add_perm(user, 'can_view_test', 'Can viwe dg')
        if self.request.user.user_type == "DG":
            content_type = ContentType.objects.get_for_model(DiagnosticsTest)
        if self.request.user.user_type == "SE":
            content_type = ContentType.objects.get_for_model(SellerProduct)
        if self.request.user.user_type == "BB":
            content_type = ContentType.objects.get_for_model(BloodGroup)
        if self.request.user.user_type == "HS":
            content_type = ContentType.objects.get_for_model(HospitalAppointment)
        if self.request.user.user_type == "CL":
            content_type = ContentType.objects.get_for_model(ClinicAppointment)
        permission, created = Permission.objects.get_or_create(codename='custom_can_view',
                                                               name='custom can view',
                                                               content_type=content_type)
        user.user_permissions.add(permission)
        user.save()
        jo = CustomUser.objects.get(id=user.id)
        print(jo.has_perm("can_addtest"))
        return user


class ClinicAppointmentFrom(RequestKwargModelFormMixin, forms.ModelForm):

    class Meta:
        model = ClinicAppointment
        fields = ("date", "time", "clinic")
        widgets = {
            "date": forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def save(self, commit=True):
        ins = super().save(commit=False)
        ins.patient = self.request.user
        if commit:
            ins.save()
            return ins


class HospitalAppointmentFrom(RequestKwargModelFormMixin, forms.ModelForm):

    class Meta:
        model = HospitalAppointment
        fields = ("date", "time", "hospital")
        widgets = {
            "date": forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def save(self, commit=True):
        ins = super().save(commit=False)
        ins.hs_patient = self.request.user
        if commit:
            ins.save()
            return ins


class AddDiagnosticTestForm(RequestKwargModelFormMixin, forms.ModelForm):

    class Meta:
        model = DiagnosticsTest
        fields = ("name",)

    def save(self, commit=True):
        ins = super().save(commit=False)
        # print(self.request.user.user_type)
        if (self.request.user.user_type == "DG"):
            ins.diagnostic = self.request.user
        if commit:
            ins.save()
            return ins


class AddSellerProductForm(RequestKwargModelFormMixin, forms.ModelForm):

    class Meta:
        model = SellerProduct
        fields = ("name", "product_type", "description")

    def save(self, commit=True):
        ins = super().save(commit=False)
        # print(self.request.user.user_type)
        if (self.request.user.user_type == "SE"):
            ins.product = self.request.user
        else:
            ins.product = self.request.user.staffof
        if commit:
            ins.save()
            return ins
