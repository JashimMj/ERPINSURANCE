from django.urls import path
from .models import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index,name ="index"),
    path('otp/', views.otpV,name='otps'),
    path('login/otp/', views.finalloginV,name='loginotp'),
    path('loging/', views.loginV, name="logning"),
    path('logout/', views.logoutV, name="logout"),

    # ----------------------Software Admin---------------------------
    path('software/admin/dashboard/', views.software_admin_dashboardV, name="software_admin_dashboard"),
    # ----------------------Software Company Information---------------------------
    path('software/admin/Company/info/', views.software_admin_company_infoV, name="software_admin_company_info"),
    path('software/admin/Company/info/save/', views.software_admin_company_info_saveV, name="software_admin_company_info_save"),
    path('software/admin/Company/info/demo/pdf/<int:id>/', views.software_admin_company_info_demo_pdfV, name="software_admin_company_info_demo_pdf"),
    path('software/admin/Company/info/pdf/<int:id>/', views.software_admin_company_info_pdfV, name="software_admin_company_info_pdf"),

    # ----------------------Edit Admin---------------------------
    path('software/admin/edit/', views.EditV, name="software_admin_Edit"),
    path('software/admin/edit/save/', views.All_Edit_saveV, name="software_admin_Edit_save"),

    # ----------------------HR---------------------------
    path('hr/dashboard/', views.hr_dashboardV, name="hr_dashboard"),
    # ----------------------HR Branch Information---------------------------
    path('hr/branch/info/', views.hr_branch_infoV, name="hr_branch_info"),
    path('hr/branch/info/save/', views.hr_branch_info_saveV, name="hr_branch_info_save"),
    path('hr/branch/info/demo/pdf/<int:id>', views.hr_branch_info_demo_pdfV, name="hr_branch_info_demo_pdf"),
    path('hr/branch/info/pdf/<int:id>', views.hr_branch_info_pdfV, name="hr_branch_info_pdf"),
    # ----------------------HR Department Information---------------------------
    path('hr/department/info/', views.hr_department_infoV, name="hr_department_info"),
    path('hr/department/info/save/', views.hr_department_info_saveV, name="hr_department_info_save"),
    path('hr/department/info/demo/pdf/<int:id>', views.hr_department_info_demo_pdfV, name="hr_department_info_demo_pdf"),
    path('hr/department/info/pdf/<int:id>', views.hr_department_info_pdfV, name="hr_department_info_pdf"),
    # ----------------------HR Designation Information---------------------------
    path('hr/designation/info/', views.hr_designation_infoV, name="hr_designation_info"),
    path('hr/designation/info/save/', views.hr_designation_info_saveV, name="hr_designation_info_save"),
    path('hr/designation/info/demo/pdf/<int:id>', views.hr_designation_info_demo_pdfV, name="hr_designation_info_demo_pdf"),
    path('hr/designation/info/pdf/<int:id>', views.hr_designation_info_pdfV, name="hr_designation_info_pdf"),
    # ----------------------HR Bank Information---------------------------
    path('hr/bank/info/', views.hr_bank_infoV, name="hr_bank_info"),
    path('hr/bank/info/save/', views.hr_bank_info_saveV, name="hr_bank_info_save"),
    path('hr/bank/info/demo/pdf/<int:id>', views.hr_bank_info_demo_pdfV, name="hr_bank_info_demo_pdf"),
    path('hr/bank/info/pdf/<int:id>', views.hr_bank_info_pdfV, name="hr_bank_info_pdf"),
    # ----------------------HR Bank Branch Information---------------------------
    path('hr/bank/Branch/info/', views.hr_bank_branch_infoV, name="hr_bank_branch_info"),
    path('hr/bank/Branch/info/save/', views.hr_bank_branch_info_saveV, name="hr_bank_branch_info_save"),
    path('hr/bank/Branch/info/demo/pdf/<int:id>', views.hr_bank_branch_info_demo_pdfV, name="hr_bank_branch_info_demo_pdf"),
    path('hr/bank/Branch/info/pdf/<int:id>', views.hr_bank_branch_info_pdfV, name="hr_bank_branch_info_pdf"),
    # ----------------------HR Branch Information---------------------------
    path('hr/employees/info/', views.hr_employees_infoV, name="hr_employees_info"),
    path('hr/employees/info/save/', views.hr_employees_info_saveV, name="hr_employees_info_save"),

    # ----------------------Software Admin Create user---------------------------
    path('software/admin/user/create/', views.software_admin_user_createV, name="software_admin_user_create"),
    path('software/admin/user/create/save/', views.software_admin_user_create_saveV, name="software_admin_user_create_save"),
    path('software/admin/user/branch/', views.software_admin_user_create_branchV, name="software_admin_user_create_branch"),
    path('software/admin/user/branch/delete/<int:id>/', views.software_admin_user_create_branch_deleteV, name="software_admin_user_create_branch_delete"),
    path('software/admin/user/module/delete/<int:id>/', views.software_admin_user_create_module_deleteV, name="software_admin_user_create_module_delete"),
    path('software/admin/user/module/', views.software_admin_user_create_moduleV, name="software_admin_user_create_module"),
    path('branch/change/', views.branch_changeV, name="branch_change"),
    path('software/admin/user/create/pdf/', views.software_admin_user_create_PDFV, name="software_admin_user_create_PDF"),

    # ----------------------Inventory Product Info---------------------------
    path('inventory/dashboard/', views.inventory_dashboardV, name="inventory_dashboard"),
    path('inventory/product/entry/', views.inventory_product_entryV, name="inventory_product_entry"),
    path('inventory/product/entry/save/', views.inventory_product_entry_saveV, name="inventory_product_entry_save"),
    path('inventory/product/demo/pdf/', views.inventory_product_demo_pdfV, name="inventory_product_demo_pdf"),
    path('inventory/product/pdf/', views.inventory_product_pdfV, name="inventory_product_pdf"),

    # ----------------------Inventory Supplier Info---------------------------
    path('inventory/supplier/entry/', views.inventory_supplier_entryV, name="inventory_supplier_entry"),
    path('inventory/supplier/entry/save/', views.inventory_supplier_entry_saveV, name="inventory_supplier_entry_save"),
    path('inventory/supplier/demo/pdf/', views.inventory_supplier_demo_pdfV, name="inventory_supplier_demo_pdf"),
    path('inventory/supplier/pdf/', views.inventory_supplier_pdfV, name="inventory_supplier_pdf"),



    # ----------------------test---------------------------
    path('test/', views.TestV, name="test"),











]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
