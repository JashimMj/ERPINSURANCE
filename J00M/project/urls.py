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

    # ----------------------Software Voyage form Information---------------------------
    path('software/voyage/form/info/', views.software_voyage_form_infoV, name="software_voyage_form_info"),
    path('software/voyage/form/info/save/', views.software_voyage_form_info_saveV, name="software_voyage_form_info_save"),
    path('software/voyage/form/info/demo/pdf/<int:id>', views.software_voyage_form_info_demo_pdfV, name="software_voyage_form_info_demo_pdf"),
    path('software/voyage/form/info/pdf/<int:id>', views.software_voyage_form_info_pdfV, name="software_voyage_form_info_pdf"),

      # ----------------------Software Voyage To Information---------------------------
    path('software/voyage/to/info/', views.software_voyage_to_infoV,name="software_voyage_to_info"),
    path('software/voyage/to/info/save/', views.software_voyage_to_info_saveV,name="software_voyage_to_info_save"),
    path('software/voyage/to/info/demo/pdf/<int:id>', views.software_voyage_to_info_demo_pdfV,name="software_voyage_to_info_demo_pdf"),
    path('software/voyage/to/info/pdf/<int:id>', views.software_voyage_to_info_pdfV,name="software_voyage_to_info_pdf"),
    # ----------------------Software Voyage Via Information---------------------------
    path('software/voyage/via/info/', views.software_voyage_via_infoV,name="software_voyage_via_info"),
    path('software/voyage/via/info/save/', views.software_voyage_via_info_saveV,name="software_voyage_via_info_save"),
    path('software/voyage/via/info/demo/pdf/<int:id>', views.software_voyage_via_info_demo_pdfV,name="software_voyage_via_info_demo_pdf"),
    path('software/voyage/via/info/pdf/<int:id>', views.software_voyage_via_info_pdfV,name="software_voyage_via_info_pdf"),
    # ----------------------Software Voyage Via Information---------------------------
    path('software/transit/by/info/', views.software_transit_by_infoV,name="software_transit_by_info"),
    path('software/transit/by/info/save/', views.software_transit_by_info_saveV,name="software_transit_by_info_save"),
    path('software/transit/by/info/demo/pdf/<int:id>', views.software_transit_by_info_demo_pdfV,name="software_transit_by_info_demo_pdf"),
    path('software/transit/by/info/pdf/<int:id>', views.software_transit_by_info_pdfV,name="software_transit_by_info_pdf"),
                  # ----------------------Software Risk Cover Information---------------------------
    path('software/risk/cover/info/', views.software_risk_cover_infoV,name="software_risk_cover_info"),
    path('software/risk/cover/info/save/', views.software_risk_cover_info_saveV,name="software_risk_cover_info_save"),
    path('software/risk/cover/info/demo/pdf/<int:id>', views.software_risk_cover_info_demo_pdfV,name="software_risk_cover_info_demo_pdf"),
    path('software/risk/cover/info/pdf/<int:id>', views.software_risk_cover_info_pdfV,name="software_risk_cover_info_pdf"),
                  # ----------------------Software Insurance Type Information---------------------------
    path('software/insurance/type/info/', views.software_insurance_type_infoV,name="software_insurance_type_info"),
    path('software/insurance/type/info/save/', views.software_insurance_type_info_saveV,name="software_insurance_type_info_save"),
    path('software/insurance/type/info/demo/pdf/<int:id>', views.software_insurance_type_info_demo_pdfV,name="software_insurance_type_info_demo_pdf"),
    path('software/insurance/type/info/pdf/<int:id>', views.software_insurance_type_info_pdfV,name="software_insurance_type_info_pdf"),

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
    # ----------------------HR client Information---------------------------
    path('hr/client/info/', views.hr_client_infoV, name="hr_client_info"),
    path('hr/client/info/save/', views.hr_client_info_saveV, name="hr_client_info_save"),
    path('hr/client/info/demo/pdf/<int:id>', views.hr_client_info_demo_pdfV, name="hr_client_info_demo_pdf"),
    path('hr/client/info/pdf/<int:id>', views.hr_client_info_pdfV, name="hr_client_info_pdf"),
    # ----------------------HR client Branch Information---------------------------
    path('hr/client/branch/info/', views.hr_client_branch_infoV, name="hr_client_branch_info"),
    path('hr/client/branch/info/save/', views.hr_client_branch_info_saveV, name="hr_client_branch_info_save"),
    # path('hr/client/info/branch/demo/pdf/<int:id>', views.hr_client_branch_info_demo_pdfV,name="hr_client_branch_info_demo_pdf"),
    # path('hr/client/branch/info/pdf/<int:id>', views.hr_client_branch_info_pdfV, name="hr_client_branch_info_pdf"),




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
    # ----------------------Inventory Product Purchase Info---------------------------
    path('inventory/product/purchase/', views.invontory_product_purchase_infoV, name="inventory_product_purchase"),
    path('inventory/product/purchase/save/', views.invontory_product_purchase_saveV, name="inventory_product_purchase_save"),
    path('inventory/product/purchase/select/', views.invontory_product_purchase_select_infoV, name="invontory_product_purchase_select"),
    path('inventory/purchase/demo/pdf/<int:Invoice_no>', views.purchage_info_pdf_demoV, name="purchase_info_pdf_demo"),
    path('inventory/purchase/pdf/<int:Invoice_no>', views.purchage_info_pdfV, name="purchage_info_pdf"),
    path('inventory/purchase/adjustment/', views.purchage_info_adjustmentV, name="purchage_info_adjustment"),
    path('inventory/purchase/adjustment/save', views.purchage_info_adjustment_saveV, name="purchage_info_adjustment_save"),
    # ----------------------Inventory Product Purchase Info---------------------------
    path('inventory/product/issue/', views.invontory_product_issue_infoV, name="inventory_product_issue"),
    path('inventory/product/issue/save/', views.invontory_product_issue_saveV, name="invontory_product_issue_save"),
    path('inventory/product/issue/select/', views.invontory_product_issue_select_infoV, name="invontory_product_issue_select"),
    path('inventory/issue/demo/pdf/<int:Invoice_no>', views.issue_info_pdf_demoV, name="issue_info_pdf_demo"),
    path('inventory/issue/pdf/<int:Invoice_no>', views.issue_info_pdfV, name="issue_info_pdf"),
    path('inventory/issue/adjustment/', views.issue_info_adjustmentV, name="issue_info_adjustment"),
    path('inventory/issue/adjustment/save', views.issue_info_adjustment_saveV, name="issue_info_adjustment_save"),


    # ----------------------UNDERWRITING DEPARTMENT---------------------------
    path('uw/dashboard/', views.uw_dashboardV, name="uw_dashboard"),
    path('uw/quotation/marine/', views.uw_q_marineV, name="uw_q_marine"),
    path('uw/quotation/marine/client/select/', views.uw_q_marine_client_selectV, name="uw_q_marine_client_select"),
    path('uw/quotation/marine/bank/branch/select/', views.uw_q_marine_bank_branch_selectV, name="uw_q_marine_bank_branch_select"),
    path('uw/quotation/marine/transit/by/select/', views.uw_q_marine_transit_by_selectV, name="uw_q_marine_transitby_select"),
    path('uw/quotation/marine/date/select/', views.qmarinedateV, name="uw_q_marine_date_select"),
    path('uw/quotation/marine/save/', views.uw_q_marine_saveV, name="uw_q_marine_save"),
    path('uw/quotation/marine/search/', views.uw_q_marine_searchV, name="uw_q_marine_search"),
    path('uw/quotation/marine/cover/search/', views.uw_q_marine_cover_searchV, name="uw_q_marine_covernote_search"),
    path('uw/quotation/marine/bill/pdf/demo/<int:id>', views.uw_q_marine_demo_pdfsV, name="uw_q_marine_demo_pdf"),
    path('uw/quotation/marine/bill/pdf/<int:id>', views.uw_q_marine_pdfsV, name="uw_q_marine_pdf"),
    path('uw/quotation/marine/bill/send/email/<int:id>', views.uw_q_marine_sendV, name="uw_q_marine_send"),
    path('uw/quotation/marine/cover/note/', views.uw_q_marine_covernoteV, name="uw_q_marine_covernote"),
    path('uw/quotation/marine/cover/note/save/', views.uw_q_marine_covernote_saveV, name="uw_q_marine_covernote_save"),
    path('uw/quotation/marine/cover/pdf/', views.uw_q_marine_cover_pdfsV, name="uw_q_marine_cover_pdf"),






    # ----------------------test---------------------------
    path('test/', views.TestV, name="test"),











]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
