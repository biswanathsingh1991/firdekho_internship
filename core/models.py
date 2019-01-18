from django.db import models
from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser,
from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django.urls import reverse
from django.db.models import Q


class CustomUser(AbstractUser):
    user_t = (('BR', 'Buyer'), ('SE', 'Seller'),
              ('HS', 'Hospital'), ('BB', 'Blood bank'),
              ('CL', 'Clinic'), ('DG', 'Diagnostics'))
    staff_ty = (("MN", "Manager"), ("EM", "Employee"))

    user_type = models.CharField(
        max_length=120, choices=user_t, default="BR", blank=False)
    staff_user = models.BooleanField(default=False)
    staff_type = models.CharField(max_length=120, choices=staff_ty, default="EM", blank=True)
    staffof = models.ForeignKey("self", related_name="staff_of_back",
                                on_delete=models.DO_NOTHING, null=True, blank=True)
    # pro_buyer = models.ManyToManyField(,
    #                                    related_name="pro_buyer_back", null=True,
    #                                    blank=True)
    # test_paitent = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
    #                                  related_name="test_paitent", null=True,
    #                                  blank=True)
    # patient = models.ForeignKey("self", related_name="patient", on_delete=models.DO_NOTHING, null=True)
    # fields for Buyer
    # test_paitent = models.ForeignKey(DiagnosticsTest, on_delete=models.DO_NOTHING,
    #                                  related_name="test_paitent", null=True,
    #                                  blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})


class UserDetails(models.Model):
    rel_user_type = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class BloodGroup(models.Model):
    blood = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    a_positive = models.PositiveIntegerField(default=0)
    o_positive = models.PositiveIntegerField(default=0)
    b_positive = models.PositiveIntegerField(default=0)
    ab_positive = models.PositiveIntegerField(default=0)
    a_negative = models.PositiveIntegerField(default=0)
    o_negative = models.PositiveIntegerField(default=0)
    b_negative = models.PositiveIntegerField(default=0)
    ab_negative = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.blood.username


cl = Q(user_type__contains="CL")


class ClinicAppointment(models.Model):

    date = models.DateField()
    time = models.IntegerField()
    clinic = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                  related_name='clinic_ap',
                                  limit_choices_to=cl)
    patient = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING,
                                   related_name='patient_ap', null=True)

    def __str__(self):
        return self.clinic.username


hs = Q(user_type__contains="hs")


class HospitalAppointment(models.Model):

    date = models.DateField()
    time = models.IntegerField()
    hospital = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                    related_name='clinic_hs',
                                    limit_choices_to=hs)
    hs_patient = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING,
                                      related_name='patient_hs', null=True)

    def __str__(self):
        return self.hospital.username


class DiagnosticsTest(models.Model):
    name = models.CharField(max_length=120)
    diagnostic = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                      related_name="dg_test", blank=True,
                                      null=True)
    test_paitent = models.ManyToManyField(CustomUser,
                                          related_name="test_paitent", null=True,
                                          blank=True)

    def __str__(self):
        return self.name


class SellerProduct(models.Model):
    product = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                related_name="pro_rel", blank=True,
                                null=True)
    name = models.CharField(max_length=120)
    added = models.DateTimeField(auto_now=True)
    product_type = models.CharField(max_length=120)
    description = models.CharField(max_length=1000)
    buyer = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name


class BuyerUserDetails(models.Model):
    name = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
