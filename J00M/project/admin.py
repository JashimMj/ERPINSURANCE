from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .resources import *


# Register your models here.

admin.site.register(Company_Information)
admin.site.register(MRTable)
admin.site.register(UserProfileM)
admin.site.register(Branch_Infoamtion)
admin.site.register(DepartmentM)
admin.site.register(DesignationM)
admin.site.register(BankM)
admin.site.register(Bank_BranchM)
admin.site.register(Software_Permittion_Branch)
admin.site.register(Inventory_Product_Entry)
admin.site.register(Inventory_Supplier_Entry)
admin.site.register(Product_PurchaseM)
admin.site.register(ModOfPayment)
admin.site.register(covernover_banner)
admin.site.register(Product_issueM)
class BookAdmin(ImportExportModelAdmin):
    resource_class = CurrencyResource
admin.site.register(Currency, BookAdmin)

class RiskAdmin(ImportExportModelAdmin):
    resource_class = RiskResource
admin.site.register(RiskCovered, RiskAdmin)
