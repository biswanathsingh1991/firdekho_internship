from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from .forms import UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import (SingUpForm, CreateSraffUserForm, ClinicAppointmentFrom,
                    HospitalAppointmentFrom, DiagnosticsTest, AddDiagnosticTestForm,
                    AddSellerProductForm)
from django.views.generic import DetailView, ListView
from . models import (CustomUser, ClinicAppointment, HospitalAppointment,
                      SellerProduct, BloodGroup)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .mixins import RequestFormKwargsMixin
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveDestroyAPIView
from .serializers import (BloodGroupSerializer,)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict


class IndexView(FormView):

    template_name = 'index.html'
    form_class = UserLoginForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('core:userdetail')
        # return reverse_lazy('core:userdetail', kwargs={"pk": self.request.user.id})


class SingUpView(CreateView):
    template_name = 'usercreation2.html'
    form_class = SingUpForm
    success_url = reverse_lazy('login1')


# class UserDetailView(LoginRequiredMixin, DetailView):
#     template_name = 'userdetail.html'
#     pk_url_kwarg = 'pk'
#     model = CustomUser
#     # queryset = CustomUser.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         req_user = self.request.user
#         for key, value in self.request.META.items():
#             print(key, value)
#         manager = req_user.customuser_set.filter(staff_type="MN")
#         employee = req_user.customuser_set.filter(staff_type="EM")
#         context['manager'] = manager
#         context['employee'] = employee
#         return context

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)

@login_required(login_url="http://127.0.0.1:8000/login/")
def userdetailview(request):
    # req_user = request.user
    context = {}
    req_user_type = request.user.user_type
    obj = CustomUser.objects.get(username=request.user.username)
    context["obj"] = obj

    context["staff_list"] = request.user.staff_of_back.all()
    if req_user_type == "BR":
        app_list = ClinicAppointment.objects.filter(patient=request.user)
        hs_app_list = HospitalAppointment.objects.filter(hs_patient=request.user)
        context["app_list"] = app_list
        context["hs_app_list"] = hs_app_list
        return render(request, template_name='buyer/buyeruserdetail.html', context=context)

    elif req_user_type == "CL":
        context["appointment"] = ClinicAppointment.objects.filter(clinic=request.user)

        return render(request, template_name='clinicdetail.html', context=context)
    elif req_user_type == "SE":
        context["pro_list"] = request.user.pro_rel.all()
        context["staff_list"] = request.user.staff_of_back.all()
        return render(request, template_name='seller/sellerprofile.html',
                      context=context)
    elif req_user_type == "BB":
        context["staff_list"] = request.user.staff_of_back.all()
        context["bloodgroup"] = request.user.bloodgroup
        return render(request, template_name='bloodbank/bloodbankdetail.html',
                      context=context)
    elif req_user_type == "DG":
        context["test_li"] = DiagnosticsTest.objects.filter(diagnostic=request.user)
        context["staff_list"] = request.user.staff_of_back.all()
        return render(request, template_name='diagnosticdetail.html',
                      context=context)
    elif req_user_type == "HS":
        return render(request, template_name='hospital/hospitaldetail.html',
                      context=context)
    elif (request.user.staff_type == "EM") and (request.user.staffof.user_type == "BB"):
        org = request.user.staffof
        bank = org.bloodgroup
        bank1 = model_to_dict(bank)
        bank1.pop("id")
        bank1.pop("blood")
        context["bank1"] = bank1
        context["bank"] = bank
        return render(request, template_name='bloodbank/staffuserdetail.html',
                      context=context)
    elif (request.user.staff_type == "EM") and (request.user.staffof.user_type == "DG"):
        org = request.user.staffof
        return render(request, template_name='diagnostic/staffuserdgdetail.html', context=context)
    elif (request.user.staff_type == "EM") and (request.user.staffof.user_type == "SE"):
        context["pro_list"] = request.user.staffof.pro_rel.all()
        return render(request, template_name='seller/staffuserdetail.html', context=context)
    elif (request.user.staff_type == "EM") and (request.user.staffof.user_type == "CL"):
        print(request.user.staffof)
        print(ClinicAppointment.objects.filter(clinic=request.user.staffof))
        context["app_list"] = ClinicAppointment.objects.filter(clinic=request.user.staffof)
        return render(request, template_name='clinic/staffuserdetail.html', context=context)


class CreateStaffUserView(RequestFormKwargsMixin, CreateView):
    template_name = 'createstafuser.html'
    form_class = CreateSraffUserForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('core:userdetail')
        # return reverse_lazy('core:userdetail', kwargs={"pk": self.request.user.id})


class MyLoginView(LoginView):

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('core:userdetail')
        # return url or reverse('core:userdetail', kwargs={'pk': self.request.user.pk})


class HospitalListView(LoginRequiredMixin, ListView):

    template_name = 'hospital_list.html'
    queryset = CustomUser.objects.filter(user_type="HS")


class BloodBankListView(LoginRequiredMixin, ListView):

    template_name = 'bloodbank_list.html'
    queryset = CustomUser.objects.filter(user_type="BB")


class ClinicListView(LoginRequiredMixin, ListView):

    template_name = 'clinic_list.html'
    queryset = CustomUser.objects.filter(user_type="CL")


class DiagnosticsListView(LoginRequiredMixin, ListView):

    template_name = 'diagonostics_list.html'
    queryset = CustomUser.objects.filter(user_type="DG")


@login_required(login_url="http://127.0.0.1:8000/login/")
def staffListView(request):
    context = {}
    context["manager"] = request.user.customuser_set.filter(staff_type="MN")
    context["employee"] = request.user.customuser_set.filter(staff_type="EM")
    return render(request, 'staff_list.html', context=context)


@api_view(['POST'])
def updateBankView(request):
    ty = request.data.get("bl_type")
    obj = request.user.staffof.bloodgroup
    li = ty.split("-")
    if li[1] == "add":
        tru = getattr(obj, li[0])
        tru += 1
        setattr(obj, li[0], tru)
        obj.save()
    if li[1] == "rm":
        tru = getattr(obj, li[0])
        tru -= 1
        setattr(obj, li[0], tru)
        obj.save()
    return Response("success")


class ClinicAppointmentView(PermissionRequiredMixin, CreateView):

    form_class = ClinicAppointmentFrom
    template_name = 'clinic/addappoint_clinic.html'
    success_url = reverse_lazy('core:userdetail')
    permission_required = ("core.custom_can_add",)


class HospitalAppointmentView(RequestFormKwargsMixin, CreateView):

    form_class = HospitalAppointmentFrom
    template_name = 'hospital/addappoint_hospital.html'
    success_url = reverse_lazy('core:userdetail')


class AddBaseView(RequestFormKwargsMixin, CreateView):
    pass


class AddDiagnosticTestView(PermissionRequiredMixin, AddBaseView):
    form_class = AddDiagnosticTestForm
    template_name = 'diagnostic/add_diagnostic_test.html'
    success_url = reverse_lazy('core:userdetail')
    permission_required = ("core.custom_can_add",)


class TestUserList(DetailView):
    template_name = 'diagnostic_test_user_list.html'
    pk_url_kwarg = 'pk'
    model = DiagnosticsTest


@api_view(['POST'])
def parmissionupdate(request):
    data = request.data.get("data")
    li = data.split("-")
    usr = CustomUser.objects.get(pk=li[0])
    if li[2] == "hs":
        content_type = ContentType.objects.get_for_model(HospitalAppointment)
    if li[2] == "se":
        content_type = ContentType.objects.get_for_model(SellerProduct)
    if li[2] == "dg":
        content_type = ContentType.objects.get_for_model(DiagnosticsTest)
    if li[2] == "bb":
        content_type = ContentType.objects.get_for_model(BloodGroup)
    if li[2] == "cl":
        content_type = ContentType.objects.get_for_model(ClinicAppointment)

    # content_type = ContentType.objects.get_for_model(DiagnosticsTest)
    if li[1] == "view":

        permission, created = Permission.objects.get_or_create(codename='custom_can_view',
                                                               name='custom can view',
                                                               content_type=content_type)
        if usr.has_perm("core.custom_can_view"):
            usr.user_permissions.remove(permission)
        else:
            usr.user_permissions.add(permission)
    if li[1] == "add":
        # content_type = ContentType.objects.get_for_model(DiagnosticsTest)
        permission, created = Permission.objects.get_or_create(codename='custom_can_add',
                                                               name='custom can add',
                                                               content_type=content_type)
        if usr.has_perm("core.custom_can_add"):
            usr.user_permissions.remove(permission)
        else:
            usr.user_permissions.add(permission)
    return Response("success")


class AddSellerProductView(PermissionRequiredMixin, AddBaseView):
    form_class = AddSellerProductForm
    template_name = 'seller/add_seller_product.html'
    success_url = reverse_lazy('core:userdetail')
    permission_required = ("core.custom_can_add",)


class ProductBuyerList(DetailView):
    template_name = 'diagnostic_test_user_list.html'
    pk_url_kwarg = 'pk'
    model = SellerProduct


class BloodBankManage(TemplateView):
    template_name = 'bloodbank/bloodbankmanage.html'
    # pk_url_kwarg = 'pk'
    # model = SellerProduct


class PurchaseProduct(LoginRequiredMixin, ListView):

    template_name = 'buyer/all_product_list.html'
    queryset = SellerProduct.objects.all()
