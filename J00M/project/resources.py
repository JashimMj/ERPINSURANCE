from import_export import resources
from .models import *

class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency
        fields='id,Name,issu_date,Edits,create_user'

class RiskResource(resources.ModelResource):
    class Meta:
        model = RiskCovered
        fields='id,Name,issu_date,Edits,create_user'

class Bank_nameResource(resources.ModelResource):
    class Meta:
        model=BankM