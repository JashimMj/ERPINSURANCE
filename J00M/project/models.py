from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileM(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    Phone=models.CharField(max_length=100,null=True,blank=True)
    Present_Address=models.TextField(max_length=255,null=True,blank=True)
    Permanant_Address=models.TextField(max_length=255,null=True,blank=True)
    Image=models.ImageField(upload_to='User_image',null=True,blank=True)
    otp=models.CharField(max_length=6,null=True,blank=True)
    Email=models.CharField(max_length=30,null=True,blank=True)
    objects=models.Manager()

    def uimages(self):
        try:
            urls=self.Image.url
        except:
            urls=''
        return urls



class Company_Information(models.Model):
    id = models.AutoField(primary_key=True)
    Company_Name=models.CharField(max_length=500,null=True,blank=True)
    Company_Address=models.CharField(max_length=1000,null=True,blank=True)
    Company_Email=models.EmailField(max_length=50,null=True,blank=True)
    Company_Phone=models.CharField(max_length=50,null=True,blank=True)
    Company_Fax=models.CharField(max_length=50,null=True,blank=True)
    Company_Web_site=models.CharField(max_length=50,null=True,blank=True)
    Company_Short_Name=models.CharField(max_length=50,null=True,blank=True)
    Authorization=models.ImageField(upload_to='authorization',null=True,blank=True)
    create_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    logo=models.ImageField(upload_to='logo',null=True,blank=True)
    issu_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    Edits=models.CharField(max_length=10,null=True,blank=True)
    objects = models.Manager()

    def image(self):
        try:
            urls = self.logo.url
        except:
            urls = ''
        return urls

    def authusers(self):
        try:
            agd = self.Authorization.url
        except:
            urlss = ''
        return agd

    def __str__(self):
        return self.Company_Name



class Branch_Infoamtion(models.Model):
    id = models.AutoField(primary_key=True)
    Branch_Name = models.CharField(max_length=500, null=True, blank=True)
    Branch_Address = models.CharField(max_length=1000, null=True, blank=True)
    Branch_Email = models.EmailField(max_length=50, null=True, blank=True)
    Branch_Phone = models.CharField(max_length=50, null=True, blank=True)
    Branch_Fax = models.CharField(max_length=50, null=True, blank=True)
    Branch_Short_Name = models.CharField(max_length=50, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.Branch_Name



class VoyageForm(models.Model):
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=255,null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Name

class VoyageTo(models.Model):
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=255,null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Name

class VoyageVia(models.Model):
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=255,null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Name

class TransitBy(models.Model):
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=255,null=True,blank=True)
    Stump_Rate=models.IntegerField(null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Name


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=255,null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return self.Name

class RiskCovered(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class InsuraceType(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)



class DepartmentM(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=500, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Name


class DesignationM(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=500, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Name


class BankM(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=500, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Name


class Bank_BranchM(models.Model):
    id = models.AutoField(primary_key=True)
    Bank_Name = models.ForeignKey(BankM,on_delete=models.CASCADE,null=True,blank=True)
    Bank_Branch=models.CharField(max_length=300,null=True,blank=True)
    Bank_Branch_Address=models.CharField(max_length=800,null=True,blank=True)
    Bank_Branch_Phone=models.CharField(max_length=20,null=True,blank=True)
    Bank_Branch_Mobile=models.CharField(max_length=20,null=True,blank=True)
    Bank_Branch_Email=models.EmailField(max_length=50,null=True,blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Bank_Branch

class ClinetM(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=500, null=True, blank=True)
    Branch_Info=models.ForeignKey(Branch_Infoamtion, on_delete=models.CASCADE, null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Name


class Client_BranchM(models.Model):
    id = models.AutoField(primary_key=True)
    Client_Name = models.ForeignKey(ClinetM,on_delete=models.CASCADE,null=True,blank=True)
    Client_Branch=models.CharField(max_length=300,null=True,blank=True)
    Client_Branch_Address=models.CharField(max_length=800,null=True,blank=True)
    Client_Branch_Phone=models.CharField(max_length=20,null=True,blank=True)
    Client_Branch_Mobile=models.CharField(max_length=20,null=True,blank=True)
    Client_Branch_Email=models.EmailField(max_length=50,null=True,blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Client_Branch


class Software_Permittion_MainM(models.Model):
    id = models.AutoField(primary_key=True)
    Main_Name=models.CharField(max_length=300,null=True,blank=True)
    Sub_Name=models.CharField(max_length=500,null=True,blank=True)
    objects = models.Manager()


    def __str__(self):
        return self.Main_Name
class Software_Permittion_Branch(models.Model):
    id = models.AutoField(primary_key=True)
    Branch=models.ForeignKey(Branch_Infoamtion, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

class Software_Permittion_Module(models.Model):
    id = models.AutoField(primary_key=True)
    Software_Permition=models.ForeignKey(Software_Permittion_MainM, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()


class Inventory_Product_Entry(models.Model):
    id = models.AutoField(primary_key=True)
    Product_Name=models.CharField(max_length=255,null=True,blank=True)
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.Product_Name


class Inventory_Supplier_Entry(models.Model):
    id = models.AutoField(primary_key=True)
    Supplier_Name=models.CharField(max_length=255,null=True,blank=True)
    Supplier_Address=models.CharField(max_length=500,null=True,blank=True)
    Supplier_Phone=models.CharField(max_length=15,null=True,blank=True)
    Supplier_Email=models.CharField(max_length=50,null=True,blank=True)
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    objects = models.Manager()
    # def __str__(self):
    #     return self.Supplier_Name


class Hr_Employees_infoM(models.Model):
    id = models.AutoField(primary_key=True)
    Employees_Name = models.CharField(max_length=300, null=True, blank=True)
    Designation = models.ForeignKey(DesignationM, on_delete=models.CASCADE, null=True, blank=True)
    Department = models.ForeignKey(DepartmentM, on_delete=models.CASCADE, null=True, blank=True)
    Present_Address = models.CharField(max_length=600, null=True, blank=True)
    Permanent_Address = models.CharField(max_length=600, null=True, blank=True)
    Phone=models.CharField(max_length=30,null=True,blank=True)
    Email=models.EmailField(max_length=30,null=True,blank=True)
    Employees_Father_name=models.CharField(max_length=300,null=True,blank=True)
    Employees_Mother_name=models.CharField(max_length=300,null=True,blank=True)
    Employees_Blood=models.CharField(max_length=30,null=True,blank=True)
    Employees_NID=models.CharField(max_length=30,null=True,blank=True)
    Last_Education_Qualification=models.CharField(max_length=100,null=True,blank=True)
    Last_Education_CGPA=models.CharField(max_length=100,null=True,blank=True)
    Employees_Date_of_Birth=models.DateField()
    Appointment_Date=models.DateField()
    Joining_Date=models.DateField()
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    objects = models.Manager()

class Product_PurchaseM(models.Model):
    id = models.AutoField(primary_key=True)
    Product_Name=models.ForeignKey(Inventory_Product_Entry, on_delete=models.CASCADE, null=True, blank=True)
    Product_Supplier_Name=models.ForeignKey(Inventory_Supplier_Entry, on_delete=models.CASCADE, null=True, blank=True)
    Quantity=models.DecimalField (max_digits=20,decimal_places=2)
    Price=models.DecimalField(max_digits=20,decimal_places=2)
    Oranty_year=models.IntegerField(null=True,blank=True,default=0)
    Oranty_start_date=models.DateField(null=True,blank=True,default='')
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    User_Branch=models.ForeignKey(Branch_Infoamtion, on_delete=models.CASCADE, null=True, blank=True)
    Invoice_no=models.CharField(max_length=50,null=True,blank=True)
    objects = models.Manager()


class Product_issueM(models.Model):
    id = models.AutoField(primary_key=True)
    Product_Name=models.ForeignKey(Inventory_Product_Entry, on_delete=models.CASCADE, null=True, blank=True)
    Product_Employees_Name=models.ForeignKey(Hr_Employees_infoM, on_delete=models.CASCADE, null=True, blank=True)
    Quantity=models.DecimalField (max_digits=20,decimal_places=2)
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    User_Branch=models.ForeignKey(Branch_Infoamtion, on_delete=models.CASCADE, null=True, blank=True)
    Invoice_no=models.CharField(max_length=50,null=True,blank=True)
    objects = models.Manager()


class MarineQuatationM(models.Model):
    id = models.AutoField(primary_key=True)
    Bill_date=models.DateField(null=True,blank=True)
    Bill_No=models.CharField(max_length=255,null=True,blank=True)
    Ac=models.CharField(max_length=255,null=True,blank=True)
    Insurance_Type=models.ForeignKey(InsuraceType,on_delete=models.CASCADE,null=True,blank=True)
    Client_NameM=models.ForeignKey(ClinetM,on_delete=models.CASCADE,null=True,blank=True)
    Client_AddressM=models.ForeignKey(Client_BranchM,on_delete=models.CASCADE,null=True,blank=True)
    Bank_Name=models.ForeignKey(BankM,on_delete=models.CASCADE,null=True,blank=True)
    Bank_Branch=models.ForeignKey(Bank_BranchM,on_delete=models.CASCADE,null=True,blank=True)
    Interest_covered=models.CharField(max_length=1000,null=True,blank=True)
    Voyage_From=models.ForeignKey(VoyageForm,on_delete=models.CASCADE,null=True,blank=True)
    Voyage_To=models.ForeignKey(VoyageTo,on_delete=models.CASCADE,null=True,blank=True)
    Voyage_Via=models.ForeignKey(VoyageVia,on_delete=models.CASCADE,null=True,blank=True)
    Transit_By=models.ForeignKey(TransitBy,on_delete=models.CASCADE,null=True,blank=True)
    Sdate=models.DateField(null=True,blank=True)
    Edate=models.DateField(null=True,blank=True)
    Sum_insured=models.FloatField(null=True,blank=True)
    Extra1=models.IntegerField(null=True,blank=True)
    Extra2=models.IntegerField(null=True,blank=True)
    Currency=models.CharField(max_length=20,null=True,blank=True)
    Excrate=models.FloatField(null=True,blank=True)
    Bdtamount=models.IntegerField(null=True,blank=True)
    Declaration=models.CharField(max_length=1000,null=True,blank=True)
    Discount=models.IntegerField(null=True,blank=True)
    SpDiscount=models.IntegerField(null=True,blank=True)
    Marine_Rate=models.FloatField(null=True,blank=True)
    Marine_Amount=models.IntegerField(null=True,blank=True)
    Ware_Rate=models.FloatField(null=True,blank=True)
    Ware_Amount=models.IntegerField(null=True,blank=True)
    Net_Amount=models.IntegerField(null=True,blank=True)
    Vat_Amount=models.IntegerField(null=True,blank=True)
    Stump_Amount=models.IntegerField(null=True,blank=True)
    Gross_Amount=models.IntegerField(null=True,blank=True)
    narration=models.CharField(max_length=1000,null=True,blank=True)
    sendmail=models.CharField(max_length=1000,null=True,blank=True)
    Producer=models.ForeignKey(Hr_Employees_infoM,on_delete=models.CASCADE,null=True,blank=True)
    RiskCover=models.ForeignKey(RiskCovered,on_delete=models.CASCADE,null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    User_Branch = models.ForeignKey(Branch_Infoamtion, on_delete=models.CASCADE, null=True, blank=True)
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class MarineCovernoteM(models.Model):
    id = models.AutoField(primary_key=True)
    Bill_No=models.CharField(max_length=255,null=True,blank=True)
    Cover_No=models.CharField(max_length=255,null=True,blank=True)
    Cover_No_no=models.CharField(max_length=255,null=True,blank=True)
    Cover_Date=models.DateField(null=True,blank=True)
    Ac=models.CharField(max_length=255,null=True,blank=True)
    Insurance_Type=models.ForeignKey(InsuraceType,on_delete=models.CASCADE,null=True,blank=True)
    Client_NameM=models.ForeignKey(ClinetM,on_delete=models.CASCADE,null=True,blank=True)
    Client_AddressM=models.ForeignKey(Client_BranchM,on_delete=models.CASCADE,null=True,blank=True)
    Bank_Name=models.ForeignKey(BankM,on_delete=models.CASCADE,null=True,blank=True)
    Bank_Branch=models.ForeignKey(Bank_BranchM,on_delete=models.CASCADE,null=True,blank=True)
    Interest_covered=models.CharField(max_length=1000,null=True,blank=True)
    Voyage_From=models.ForeignKey(VoyageForm,on_delete=models.CASCADE,null=True,blank=True)
    Voyage_To=models.ForeignKey(VoyageTo,on_delete=models.CASCADE,null=True,blank=True)
    Voyage_Via=models.ForeignKey(VoyageVia,on_delete=models.CASCADE,null=True,blank=True)
    Transit_By=models.ForeignKey(TransitBy,on_delete=models.CASCADE,null=True,blank=True)
    Sdate=models.DateField(null=True,blank=True)
    Edate=models.DateField(null=True,blank=True)
    Sum_insured=models.FloatField(null=True,blank=True)
    Extra1=models.IntegerField(null=True,blank=True)
    Extra2=models.IntegerField(null=True,blank=True)
    Currency=models.CharField(max_length=20,null=True,blank=True)
    Excrate=models.FloatField(null=True,blank=True)
    Bdtamount=models.IntegerField(null=True,blank=True)
    Declaration=models.CharField(max_length=1000,null=True,blank=True)
    Discount=models.IntegerField(null=True,blank=True)
    SpDiscount=models.IntegerField(null=True,blank=True)
    Marine_Rate=models.FloatField(null=True,blank=True)
    Marine_Amount=models.IntegerField(null=True,blank=True)
    Ware_Rate=models.FloatField(null=True,blank=True)
    Ware_Amount=models.IntegerField(null=True,blank=True)
    Net_Amount=models.IntegerField(null=True,blank=True)
    Vat_Amount=models.IntegerField(null=True,blank=True)
    Stump_Amount=models.IntegerField(null=True,blank=True)
    Gross_Amount=models.IntegerField(null=True,blank=True)
    narration=models.CharField(max_length=1000,null=True,blank=True)
    sendmail=models.CharField(max_length=1000,null=True,blank=True)
    Producer=models.ForeignKey(Hr_Employees_infoM,on_delete=models.CASCADE,null=True,blank=True)
    RiskCover=models.ForeignKey(RiskCovered,on_delete=models.CASCADE,null=True,blank=True)
    issu_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Edits = models.CharField(max_length=10, null=True, blank=True)
    User_Branch = models.ForeignKey(Branch_Infoamtion, on_delete=models.CASCADE, null=True, blank=True)
    userc = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)











