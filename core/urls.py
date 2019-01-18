from django.urls import path, include, re_path
from .views import(IndexView, SingUpView, CreateStaffUserView,
                   HospitalListView, BloodBankListView, ClinicListView,
                   DiagnosticsListView, ClinicAppointmentView, HospitalAppointmentView,
                   AddDiagnosticTestView, TestUserList, AddSellerProductView,
                   ProductBuyerList, BloodBankManage, PurchaseProduct)
from . import views

app_name = "core"

urlpatterns = [
    path('', SingUpView.as_view(), name="singup"),
    # path('userdetail/<int:pk>/', UserDetailView.as_view(), name="userdetail"),
    path('userdetail/', views.userdetailview, name="userdetail"),
    path('staffusercreation/', CreateStaffUserView.as_view(), name="createstaffuser"),
    path('hospitallist/', HospitalListView.as_view(), name="hospitallist"),
    path('bloodbanklist/', BloodBankListView.as_view(), name="bloodbanklist"),
    path('cliniclist/', ClinicListView.as_view(), name="cliniclist"),
    path('diagnosticslist/', DiagnosticsListView.as_view(), name="diagnosticslist"),
    path('stafflist/', views.staffListView, name="stafflist"),
    path('bankmanageview/', BloodBankManage.as_view(), name="bankmanageview"),
    path('updatebankview/', views.updateBankView, name="updatebankview"),
    path('clinicappointment/', ClinicAppointmentView.as_view(), name="clinicappointment"),
    path('hospitalappointment/', HospitalAppointmentView.as_view(), name="hospitalappointment"),
    path('adddignostictest/', AddDiagnosticTestView.as_view(), name="adddignostictest"),
    path('testuserlist/<int:pk>/', TestUserList.as_view(), name="testuserlist"),
    path('uddgaddpermission', views.parmissionupdate, name="uddgaddpermission"),
    path('addsellerproduct/', AddSellerProductView.as_view(), name="addsellerproduct"),
    path('productbuyerlist/<int:pk>/', ProductBuyerList.as_view(), name="productbuyerlist"),
    path('purchaseproduct/', PurchaseProduct.as_view(), name="purchaseproduct")

]
