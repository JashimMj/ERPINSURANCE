from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
# Create your views here.
import random
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from pathlib import Path
import os
from num2words import num2words
import datetime

from django.db.models import F, Sum

company=Company_Information.objects.filter(id=1)

@login_required(login_url='/loging/')
def index(request):
    user_branch=Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch=Software_Permittion_Branch.objects.filter(Branch=request.user.last_name,user=request.user.id)


    return render(request,'index.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch})


def branch_changeV(request):
    branch_c = request.POST.get('brnchselect')
    print(branch_c)
    users = User.objects.get(username=request.user.username)
    users.last_name = branch_c
    users.save()

    return redirect('/')

def loginV(request):
    return render(request,'loging.html',{'company':company})

def otpV(request):
    if request.method=='POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        user = auth.authenticate(username=name, password=password)
        if user is not None:
            # auth.login(request, user)
            users = UserProfileM.objects.filter(user=user.id).first()
            otps = str(random.randint(1000, 9999))
            users.otp = otps
            users.save()
            request.session['name']=name
            request.session['password']=password
            for x in company:
                subject = f'OTP {x.Company_Name}'
                message = f'Hi {user.username}, thank you for Trying to Login. Your OTP number is {otps}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [users.Email ]
                send_mail(subject, message, email_from, recipient_list)
                return render(request,'otppages.html',{'company':company})
        messages.info(request, 'User is not valid')
    return redirect('/loging/')


def software_admin_user_create_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        username = request.POST.get('u_name')
        userid = request.POST.get('u_id')
        phone = request.POST.get('u_phone')
        email = request.POST.get('u_email')
        present = request.POST.get('u_address')
        permanent = request.POST.get('u_peraddress')
        password1 = request.POST.get('password')
        password2 = request.POST.get('re_password')
        branch_code = request.POST.getlist('branch_select')
        module_code = request.POST.getlist('module_select')
        if userid is None:
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'User Name already taken')
                    return redirect('/software/admin/user/create/')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'E-Mail already taken')
                    return redirect('/software/admin/user/create/')
                else:
                    image = request.FILES['images']
                    store = FileSystemStorage()
                    filename = store.save(image.name, image)
                    profile_pic_url = store.url(filename)
                    user = User.objects.create_user(username=username, email=email, password=password1,
                                                    last_name=1)
                    user.save()
                    sing = UserProfileM(user=user, Phone=phone, Present_Address=present, Permanant_Address=permanent,
                                        Image=image,Email=email)
                    sing.save()
                    c = min([len(branch_code)])
                    for i in range(c):
                        # users=User.objects.get(pk=request.user.id)
                        Branch = Branch_Infoamtion.objects.get(id=branch_code[i])
                        data = Software_Permittion_Branch.objects.create(user=user, Branch=Branch)
                    cds = min([len(module_code)])
                    for x in range(cds):
                        module = Software_Permittion_MainM.objects.get(id=module_code[x])
                        data_module=Software_Permittion_Module.objects.create(user=user,Software_Permition=module)
                    messages.info(request, 'Data Saved')
                return render(request, 'software_admin/forms/message.html', {'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

        else:
            c = min([len(branch_code)])
            for i in range(c):
                dd=Branch_Infoamtion.objects.get(id=branch_code[i])
                users=User.objects.get(id=userid)
                branch=Software_Permittion_Branch.objects.filter(user=users).update_or_create(Branch=dd,user=users)
                
            cds = min([len(module_code)])
            for d in range(cds):
                users = User.objects.get(id=userid)
                module = Software_Permittion_MainM.objects.get(id=module_code[d])
                data_module = Software_Permittion_Module.objects.update_or_create(user=users, Software_Permition=module)


                # for x in branch:
                #     print(x.Branch)
                #
                # if x.Branch != branch_code[c]:
                #         print(branch_code[i])



            messages.info(request, 'Data Update')
        return render(request, 'software_admin/forms/message.html', {'company': company,'user_branch':user_branch,'user_current_branch':user_current_branch})


def finalloginV(request):
    name=request.session['name']
    password=request.session['password']
    otpf = request.POST.get('otps')
    user = auth.authenticate(username=name, password=password)
    users = UserProfileM.objects.filter(user=user.id).first()
    if otpf == users.otp:
        user = User.objects.get(id=users.user.id)
        auth.login(request, user)
        return redirect('/')
    else:
        messages.info(request, 'OTP NUMBER IS WRONG')
        return render(request,'otppages.html',{'company':company})

@login_required(login_url='/loging/')
def logoutV(request):
    auth.logout(request)
    return redirect('/loging/')


def software_admin_user_createV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        user_name=User.objects.get(id=search)
        user_ss=User.objects.filter(username=user_name)
        branchs=Software_Permittion_Branch.objects.filter(user=user_name)
        permission=Software_Permittion_Module.objects.filter(user=user_name)
        users = UserProfileM.objects.all().count()
        branch_select = Branch_Infoamtion.objects.all()
        permittion_select_all = Software_Permittion_MainM.objects.raw(
            'select id,Sub_Name from project_software_permittion_mainm')
        return render(request, 'software_admin/forms/user_create.html',
                      {'branch_select': branch_select, 'permittion_select_all': permittion_select_all, 'users': users,'branchs':branchs,'permission':permission,'user_ss':user_ss,'user_current_branch':user_current_branch,'user_branch':user_branch,'company':company})
    else:
        users=UserProfileM.objects.all().count()
        branch_select = Branch_Infoamtion.objects.all()
        permittion_select_all = Software_Permittion_MainM.objects.raw('select id,Sub_Name from project_software_permittion_mainm')
        return render(request,'software_admin/forms/user_create.html',{'user_branch':user_branch,'branch_select':branch_select,'permittion_select_all':permittion_select_all,'users':users,'user_current_branch':user_current_branch,'company':company})

def software_admin_user_create_branchV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    branch_select=Branch_Infoamtion.objects.all()
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request,'software_admin/forms/branch_select_user.html',{'branch_select':branch_select,'user_current_branch':user_current_branch,'user_branch':user_branch,'company':company})


def software_admin_user_create_moduleV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    permittion_select_all = Software_Permittion_MainM.objects.raw('select DISTINCT id,Sub_Name from project_software_permittion_mainm')

    return render(request,'software_admin/forms/module_select_user.html',{'user_branch':user_branch,'permittion_select_all':permittion_select_all,'user_current_branch':user_current_branch,'company':company})



@login_required(login_url='/loging/')
def software_admin_dashboardV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request,'software_admin/software_admin_dashboard.html',{'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

@login_required(login_url='/loging/')
def software_admin_company_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Company_Information.objects.filter(id=search)
        datasall = Company_Information.objects.filter(id=search)
        bill = Company_Information.objects.all().count()
        return render(request, 'software_admin/forms/company_info.html',
                      { 'datas':datas,'datasall': datasall,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    else:
        bill=Company_Information.objects.all().count()
        return render(request,'software_admin/forms/company_info.html',{'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

@login_required(login_url='/loging/')
def software_admin_company_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = Company_Information.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        cname = request.POST.get('Cname')
        caddress = request.POST.get('Caddress')
        cphone = request.POST.get('Cphone')
        cfax = request.POST.get('Cfax')
        cemail = request.POST.get('Cemail')
        cweb = request.POST.get('Cweb')
        cshort = request.POST.get('Cshort')
        if bnumber is None:
            image = request.FILES['logo']
            store = FileSystemStorage()
            filename = store.save(image.name, image)
            profile_pic_url = store.url(filename)
            date=Company_Information(id=id,Company_Name=cname,Company_Address=caddress,Company_Email=cemail,Company_Phone=cphone,
                                     Company_Fax=cfax,create_user=createuser, Company_Web_site=cweb,Company_Short_Name=cshort,logo=image)
            date.save()
            datas = Company_Information.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = Company_Information.objects.all().count()
            return render(request, 'software_admin/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = Company_Information.objects.all().count()
            datas = Company_Information.objects.filter(id=bnumber)
            data = Company_Information.objects.get(id=bnumber)
            data.Company_Name = cname
            data.Company_Address = caddress
            data.Company_Email = cemail
            data.Company_Phone = cphone
            data.Company_Fax = cfax
            data.create_user = createuser
            data.Company_Web_site = cweb
            data.Company_Short_Name = cshort
            if request.method == 'File':
                image = request.FILES['logo']
                store = FileSystemStorage()
                filename = store.save(image.name, image)
                profile_pic_url = store.url(filename)
                data.logo=image
            else:
                datas = Company_Information.objects.filter(id=bnumber)
                for x in datas:
                    data.logo=x.logo
                    data.save()
            messages.info(request, 'Data Update')
            return render(request,'software_admin/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

def software_admin_company_info_demo_pdfV(request,id=0):

    company_info=Company_Information.objects.filter(id=id)
    template_path = 'software_admin/reports/Company_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'company_info':company_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def software_admin_company_info_pdfV(request,id=0):
    company_info = Company_Information.objects.filter(id=id)
    template_path = 'software_admin/reports/Company_info_pdf_demo.html'
    context = {'company':company,'company_info':company_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    data=Company_Information.objects.get(id=id)
    data.Edits=1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def EditV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    company_info=request.POST.get('company')
    branch_info=request.POST.get('branch')
    department_info=request.POST.get('depertment_info')
    designation_info=request.POST.get('designation_info')
    bank_info=request.POST.get('bank_info')
    bank_branch_info=request.POST.get('bank_branch_info')
    product_info=request.POST.get('product_info')
    suppler_info=request.POST.get('supplier_info')
    product_purchase_info=request.POST.get('product_purchase_info')
    if company_info:
        company_edit=Company_Information.objects.filter(id=company_info)
        return render(request, 'software_admin/forms/Edit_message.html', {'company_edit': company_edit,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif branch_info :
        branch_edit = Branch_Infoamtion.objects.filter(id=branch_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'branch_edit': branch_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif department_info :
        department_edit = DepartmentM.objects.filter(id=department_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'department_edit': department_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif designation_info :
        designation_edit = DesignationM.objects.filter(id=designation_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'designation_edit': designation_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif bank_info :
        bank_edit = BankM.objects.filter(id=bank_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'bank_edit': bank_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif bank_branch_info :
        bank_branch_edit = Bank_BranchM.objects.filter(id=bank_branch_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'bank_branch_edit': bank_branch_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif product_info :
        product_edit = Inventory_Product_Entry.objects.filter(id=product_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'product_edit': product_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif suppler_info :
        supplier_edit = Inventory_Supplier_Entry.objects.filter(id=suppler_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'supplier_edit': supplier_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    elif product_purchase_info :
            product_purchase_edit = Product_PurchaseM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no,Edits from project_product_purchasem ppp WHERE Invoice_no =%s',[product_purchase_info])
            return render(request, 'software_admin/forms/Edit_message.html',
                          {'product_purchase_edit': product_purchase_edit, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})

    return render(request,'software_admin/forms/All_Edit.html',{'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

def All_Edit_saveV(request):
    company_info = request.POST.get('Bnumber')
    cedit = request.POST.get('Cedit')
    branchids = request.POST.get('branchid')
    bedits = request.POST.get('bedit')
    department_id = request.POST.get('Department_id')
    department_edit = request.POST.get('Departemnt_edit')
    designation_id = request.POST.get('Designation_id')
    designation_edit = request.POST.get('Designation_edit')
    bank_id = request.POST.get('Bank_id')
    bank_edit = request.POST.get('Bank_edit')
    bank_branch_id = request.POST.get('Bank_branch_id')
    bank_branch_edit = request.POST.get('Bank_branch_edit')
    product_edit_id = request.POST.get('product_id')
    product_edit_edit = request.POST.get('product_edite')
    supplier_edit_id = request.POST.get('supplier_id')
    supplier_edit_edit = request.POST.get('supplier_edite')
    product_purchase_inv = request.POST.get('product_purchase_inv')
    purchase_edite = request.POST.get('purchase_edite')
    if company_info:
        company_edits = Company_Information.objects.get(id=company_info)
        company_edits.Edits=cedit
        company_edits.save()
    elif branchids:
        branch_edits=Branch_Infoamtion.objects.get(id=branchids)
        branch_edits.Edits=bedits
        branch_edits.save()
    elif department_id:
        department_edits=DepartmentM.objects.get(id=department_id)
        department_edits.Edits=department_edit
        department_edits.save()
    elif designation_id:
        designation_edits=DesignationM.objects.get(id=designation_id)
        designation_edits.Edits=designation_edit
        designation_edits.save()
    elif bank_id:
        bank_edits=BankM.objects.get(id=bank_id)
        bank_edits.Edits=bank_edit
        bank_edits.save()
    elif bank_branch_id:
        bank_branch_edits=Bank_BranchM.objects.get(id=bank_branch_id)
        bank_branch_edits.Edits=bank_branch_edit
        bank_branch_edits.save()
    elif product_edit_id:
        product_edits=Inventory_Product_Entry.objects.get(id=product_edit_id)
        product_edits.Edits=product_edit_edit
        product_edits.save()
    elif supplier_edit_id:
        supplier_edits=Inventory_Supplier_Entry.objects.get(id=supplier_edit_id)
        supplier_edits.Edits=supplier_edit_edit
        supplier_edits.save()
    elif product_purchase_inv:
        abc=Product_PurchaseM.objects.filter(Invoice_no=product_purchase_inv)
        for x in abc:
            purchasep_edits=Product_PurchaseM.objects.get(id=x.id)
            purchasep_edits.Edits=purchase_edite
            purchasep_edits.save()
    messages.info(request,'Data Update')

    return redirect('/software/admin/edit/')


def hr_dashboardV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request,'hr/hr_dashboard.html',{'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

def hr_branch_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Branch_Infoamtion.objects.filter(id=search)
        datasall = Branch_Infoamtion.objects.filter(id=search)
        bill = Branch_Infoamtion.objects.all().count()
        return render(request, 'hr/forms/branch_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    else:
        bill = Branch_Infoamtion.objects.all().count()
    return render(request,'hr/forms/branch_info.html',{'company':company,'bill':bill,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_branch_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = Branch_Infoamtion.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        bname = request.POST.get('Bname')
        baddress = request.POST.get('Baddress')
        bphone = request.POST.get('Bphone')
        bfax = request.POST.get('Bfax')
        bemail = request.POST.get('Bemail')
        bshort = request.POST.get('Bshort')
        if bnumber is None:
            date=Branch_Infoamtion(id=id,Branch_Name=bname,Branch_Address=baddress,Branch_Email=bemail,Branch_Phone=bphone,
                                     Branch_Fax=bfax,create_user=createuser,Branch_Short_Name=bshort)
            date.save()
            datas = Branch_Infoamtion.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = Branch_Infoamtion.objects.all().count()
            return render(request, 'hr/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = Branch_Infoamtion.objects.all().count()
            datas = Branch_Infoamtion.objects.filter(id=bnumber)
            data = Branch_Infoamtion.objects.get(id=bnumber)
            data.Branch_Name = bname
            data.Branch_Address = baddress
            data.Branch_Email = bemail
            data.Branch_Phone = bphone
            data.Branch_Fax = bfax
            data.create_user = createuser
            data.Branch_Short_Name = bshort
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'hr/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

def hr_branch_info_demo_pdfV(request,id=0):
    branch_info=Branch_Infoamtion.objects.filter(id=id)
    template_path = 'hr/reports/branch_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'branch_info':branch_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def hr_branch_info_pdfV(request,id=0):
    branch_info = Branch_Infoamtion.objects.filter(id=id)
    template_path = 'hr/reports/branch_info_pdf.html'
    context = {'company':company,'branch_info':branch_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    data=Branch_Infoamtion.objects.get(id=id)
    data.Edits=1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def hr_department_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = DepartmentM.objects.filter(id=search)
        datasall = DepartmentM.objects.filter(id=search)
        bill = DepartmentM.objects.all().count()
        return render(request, 'hr/forms/department_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    else:
        bill = DepartmentM.objects.all().count()
    return render(request,'hr/forms/department_info.html',{'company':company,'bill':bill,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_department_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = DepartmentM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('Dname')

        if bnumber is None:
            date=DepartmentM(id=id,Name=dname,create_user=createuser)
            date.save()
            datas = DepartmentM.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = DepartmentM.objects.all().count()
            return render(request, 'hr/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = DepartmentM.objects.all().count()
            datas = DepartmentM.objects.filter(id=bnumber)
            data = DepartmentM.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'hr/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_department_info_demo_pdfV(request,id=0):
    department_info=DepartmentM.objects.filter(id=id)
    template_path = 'hr/reports/department_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'department_info':department_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def hr_department_info_pdfV(request,id=0):
    department_info = DepartmentM.objects.filter(id=id)
    template_path = 'hr/reports/department_info_pdf.html'
    context = {'company':company,'department_info':department_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    data=DepartmentM.objects.get(id=id)
    data.Edits=1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_designation_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = DesignationM.objects.filter(id=search)
        datasall = DesignationM.objects.filter(id=search)
        bill = DesignationM.objects.all().count()
        return render(request, 'hr/forms/designation_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    else:
        bill = DesignationM.objects.all().count()
    return render(request,'hr/forms/designation_info.html',{'company':company,'bill':bill,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_designation_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = DesignationM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        designation_n = request.POST.get('Designation_n')

        if bnumber is None:
            date=DesignationM(id=id,Name=designation_n,create_user=createuser)
            date.save()
            datas = DesignationM.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = DesignationM.objects.all().count()
            return render(request, 'hr/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = DesignationM.objects.all().count()
            datas = DesignationM.objects.filter(id=bnumber)
            data = DesignationM.objects.get(id=bnumber)
            data.Name = designation_n
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'hr/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_designation_info_demo_pdfV(request,id=0):
    designation_info=DesignationM.objects.filter(id=id)
    template_path = 'hr/reports/designation_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'designation_info':designation_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_designation_info_pdfV(request,id=0):
    designation_info = DesignationM.objects.filter(id=id)
    template_path = 'hr/reports/designation_info_pdf.html'
    context = {'company':company,'designation_info':designation_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    data=DesignationM.objects.get(id=id)
    data.Edits=1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def hr_bank_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = BankM.objects.filter(id=search)
        datasall = BankM.objects.filter(id=search)
        bill = BankM.objects.all().count()
        return render(request, 'hr/forms/bank_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch})
    else:
        bill = BankM.objects.all().count()
    return render(request,'hr/forms/bank_info.html',{'company':company,'bill':bill,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_bank_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = BankM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        bank_n = request.POST.get('Bank_n')

        if bnumber is None:
            date=BankM(id=id,Name=bank_n,create_user=createuser)
            date.save()
            datas = BankM.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = BankM.objects.all().count()
            return render(request, 'hr/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = BankM.objects.all().count()
            datas = BankM.objects.filter(id=bnumber)
            data = BankM.objects.get(id=bnumber)
            data.Name = bank_n
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'hr/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_bank_info_demo_pdfV(request,id=0):
    bank_info=BankM.objects.filter(id=id)
    template_path = 'hr/reports/bank_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'bank_info':bank_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_bank_info_pdfV(request,id=0):
    bank_info = BankM.objects.filter(id=id)
    template_path = 'hr/reports/bank_info_pdf.html'
    context = {'company':company,'bank_info':bank_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    data=BankM.objects.get(id=id)
    data.Edits=1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def hr_bank_branch_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Bank_BranchM.objects.filter(id=search)
        datasall = Bank_BranchM.objects.filter(id=search)
        bill = Bank_BranchM.objects.all().count()
        bank_name=BankM.objects.all()
        return render(request, 'hr/forms/bank_branch_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,'bank_name':bank_name,'user_current_branch':user_current_branch,'user_branch':user_branch})
    else:
        bank_name = BankM.objects.all()
        bill = Bank_BranchM.objects.all().count()
    return render(request,'hr/forms/bank_branch_info.html',{'company':company,'bill':bill,'bank_name':bank_name,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_bank_branch_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = Bank_BranchM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        bank_n = request.POST.get('Bank_n')
        bankname = BankM.objects.get(id=bank_n)
        bank_branch_n = request.POST.get('Bank_Branch_n')
        bank_branch_a = request.POST.get('Bank_Branch_a')
        bank_branch_p = request.POST.get('Bank_Branch_p')
        bank_branch_m = request.POST.get('Bank_Branch_m')
        bank_branch_e = request.POST.get('Bank_Branch_e')

        if bnumber is None:
            date=Bank_BranchM(id=id,Bank_Name=bankname,Bank_Branch=bank_branch_n,Bank_Branch_Address=bank_branch_a,
                              Bank_Branch_Phone=bank_branch_p,Bank_Branch_Mobile=bank_branch_m,Bank_Branch_Email=bank_branch_e,create_user=createuser)
            date.save()
            datas = Bank_BranchM.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = Bank_BranchM.objects.all().count()
            return render(request, 'hr/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = Bank_BranchM.objects.all().count()
            datas = Bank_BranchM.objects.filter(id=bnumber)
            data = Bank_BranchM.objects.get(id=bnumber)
            data.Bank_Name = bankname
            data.Bank_Branch=bank_branch_n
            data.Bank_Branch_Address=bank_branch_a
            data.Bank_Branch_Phone=bank_branch_p
            data.Bank_Branch_Mobile=bank_branch_m
            data.Bank_Branch_Email=bank_branch_e
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'hr/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})


def hr_bank_branch_info_demo_pdfV(request,id=0):
    bank_branch_info=Bank_BranchM.objects.filter(id=id)
    template_path = 'hr/reports/bank_branch_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'bank_branch_info':bank_branch_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_bank_branch_info_pdfV(request,id=0):
    bank_branch_info = Bank_BranchM.objects.filter(id=id)
    template_path = 'hr/reports/bank_branch_info_pdf.html'
    context = {'company':company,'bank_branch_info':bank_branch_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    data=Bank_BranchM.objects.get(id=id)
    data.Edits=1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_employees_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist=DesignationM.objects.all()
    depertmentlist=DepartmentM.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Hr_Employees_infoM.objects.filter(id=search)
        datasall = Hr_Employees_infoM.objects.filter(id=search)
        bill = Hr_Employees_infoM.objects.all().count()


        return render(request, 'hr/forms/employees_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'company':company})
    else:
        bill = Hr_Employees_infoM.objects.all().count()
        return render(request,'hr/forms/employees_info.html',{'user_current_branch':user_current_branch,'user_branch':user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'bill':bill,'company':company})

def hr_employees_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = Hr_Employees_infoM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        Ename = request.POST.get('Ename')
        designation = request.POST.get('designation')
        designationss = DesignationM.objects.get(id=designation)
        department=request.POST.get('department')
        departmentss=DepartmentM.objects.get(id=department)
        paddress = request.POST.get('paddress')
        paraddress = request.POST.get('paraddress')
        ephone = request.POST.get('ephone')
        efather = request.POST.get('efather')
        emother = request.POST.get('emother')
        eblood = request.POST.get('eblood')
        nid = request.POST.get('nid')
        ebarth = request.POST.get('ebarth')
        adate = request.POST.get('adate')
        jdate = request.POST.get('jdate')
        edu = request.POST.get('edu')
        cgp = request.POST.get('cgp')

        if bnumber is None:
            date=Hr_Employees_infoM(id=id,Employees_Name=Ename,Designation=designationss,Department=departmentss,
                              Present_Address=paddress,Permanent_Address=paraddress,Phone=ephone,Employees_Father_name=efather,
                              Employees_Mother_name=emother,Employees_Blood=eblood,Employees_NID=nid,Last_Education_Qualification=edu,
                              Last_Education_CGPA=cgp,Employees_Date_of_Birth=ebarth,Appointment_Date=adate,Joining_Date=jdate,userc=createuser)
            date.save()
            datas = Hr_Employees_infoM.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = Hr_Employees_infoM.objects.all().count()
            return render(request, 'hr/forms/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch,'company':company})
        else:
            bill = Hr_Employees_infoM.objects.all().count()
            datas = Hr_Employees_infoM.objects.filter(id=bnumber)
            data = Hr_Employees_infoM.objects.get(id=bnumber)
            data.Employees_Name=Ename
            data.Designation=designationss
            data.Department=departmentss
            data.Present_Address=paddress
            data.Permanent_Address=paraddress
            data.Phone=ephone
            data.Employees_Father_name=efather
            data.Employees_Mother_name=emother
            data.Employees_Blood=eblood
            data.Employees_NID=nid
            data.Last_Education_Qualification=edu
            data.Last_Education_CGPA=cgp
            data.Employees_Date_of_Birth=ebarth
            data.Appointment_Date=adate
            data.Joining_Date=jdate
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'hr/forms/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch,'company':company})



def software_admin_user_create_branch_deleteV(request,id=0):
    if id !=0:
        branch=Software_Permittion_Branch.objects.get(pk=id)
        branch.delete()
        messages.info(request, 'Data Delete')
    return render(request,'hr/forms/message.html')

def software_admin_user_create_module_deleteV(request,id=0):
    if id !=0:
        module=Software_Permittion_Module.objects.get(pk=id)
        module.delete()
        messages.info(request, 'Data Delete')
    return render(request,'hr/forms/message.html')

def software_admin_user_create_PDFV(request,id=0):
    user_info = UserProfileM.objects.all()
    template_path = 'software_admin/reports/user_info_pdf.html'
    context = {'company':company,'user_info':user_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def inventory_dashboardV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request,'inventory/inventory_dashboard.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch})


def inventory_product_entryV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Inventory_Product_Entry.objects.filter(id=search)
        datasall = Inventory_Product_Entry.objects.filter(id=search)
        product_count=Inventory_Product_Entry.objects.all().count()
        return render(request, 'inventory/forms/product_entry.html',
                      {'datas': datas, 'datasall': datasall, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch,'product_count':product_count})
    else:
        product_count=Inventory_Product_Entry.objects.all().count()
    return render(request, 'inventory/forms/product_entry.html', {'company': company,'user_branch':user_branch,'user_current_branch':user_current_branch,'product_count':product_count})



def inventory_product_entry_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = Inventory_Product_Entry.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        product_n = request.POST.get('product_n')

        if bnumber is None:
            date=Inventory_Product_Entry(id=id,Product_Name=product_n,userc=createuser)
            date.save()
            datas = Inventory_Product_Entry.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = Inventory_Product_Entry.objects.all().count()
            return render(request, 'inventory/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = Inventory_Product_Entry.objects.all().count()
            datas = Inventory_Product_Entry.objects.filter(id=bnumber)
            data = Inventory_Product_Entry.objects.get(id=bnumber)
            data.Product_Name = product_n
            data.userc = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'inventory/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})



def inventory_product_demo_pdfV(request):
    product_info=Inventory_Product_Entry.objects.all()
    template_path = 'inventory/reports/inventory_product_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'product_info':product_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def inventory_product_pdfV(request):
    product_info = Inventory_Product_Entry.objects.all()
    template_path = 'inventory/reports/product_info_pdf.html'
    context = {'company':company,'product_info':product_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    abc=Inventory_Product_Entry.objects.filter(Edits=None)
    if abc:
        data=Inventory_Product_Entry.objects.get(Edits=None)
        data.Edits=1
        data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def inventory_supplier_entryV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Inventory_Supplier_Entry.objects.filter(id=search)
        datasall = Inventory_Supplier_Entry.objects.filter(id=search)
        supplier_count=Inventory_Supplier_Entry.objects.all().count()
        return render(request, 'inventory/forms/supplier_entry.html',
                      {'datas': datas, 'datasall': datasall, 'company': company,'user_current_branch':user_current_branch,'user_branch':user_branch,'supplier_count':supplier_count})
    else:
        supplier_count=Inventory_Supplier_Entry.objects.all().count()
    return render(request, 'inventory/forms/supplier_entry.html', {'company': company,'user_branch':user_branch,'user_current_branch':user_current_branch,'supplier_count':supplier_count})


def inventory_supplier_entry_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        counter = Inventory_Supplier_Entry.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        supplier_n = request.POST.get('supplier_n')
        supplier_a = request.POST.get('supplier_a')
        supplier_p = request.POST.get('supplier_p')
        supplier_e = request.POST.get('supplier_e')

        if bnumber is None:
            date=Inventory_Supplier_Entry(id=id,Supplier_Name=supplier_n,Supplier_Address=supplier_a,Supplier_Phone=supplier_p,Supplier_Email=supplier_e,userc=createuser)
            date.save()
            datas = Inventory_Supplier_Entry.objects.filter(id=id)
            messages.info(request,'Data Save')
            bill = Inventory_Supplier_Entry.objects.all().count()
            return render(request, 'inventory/message.html', {'datas': datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = Inventory_Supplier_Entry.objects.all().count()
            datas = Inventory_Supplier_Entry.objects.filter(id=bnumber)
            data = Inventory_Supplier_Entry.objects.get(id=bnumber)
            data.Supplier_Name=supplier_n
            data.Supplier_Address=supplier_a
            data.Supplier_Phone=supplier_p
            data.Supplier_Email=supplier_e
            data.userc = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request,'inventory/message.html',{'datas':datas,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})


def inventory_supplier_demo_pdfV(request):
    supplier_info=Inventory_Supplier_Entry.objects.all()
    template_path = 'inventory/reports/inventory_supplier_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'supplier_info':supplier_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def inventory_supplier_pdfV(request):
    supplier_info = Inventory_Supplier_Entry.objects.all()
    template_path = 'inventory/reports/supplier_info_pdf.html'
    context = {'company':company,'supplier_info':supplier_info}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    abc=Inventory_Supplier_Entry.objects.filter(Edits=None)
    if abc:
        data=Inventory_Supplier_Entry.objects.get(Edits=None)
        data.Edits=1
        data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def hr_employees_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist=DesignationM.objects.all()
    depertmentlist=DepartmentM.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Hr_Employees_infoM.objects.filter(id=search)
        datasall = Hr_Employees_infoM.objects.filter(id=search)
        bill = Hr_Employees_infoM.objects.all().count()


        return render(request, 'hr/forms/employees_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'company':company})
    else:
        bill = Hr_Employees_infoM.objects.all().count()
        return render(request,'hr/forms/employees_info.html',{'user_current_branch':user_current_branch,'user_branch':user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'bill':bill,'company':company})



def invontory_product_purchase_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist=DesignationM.objects.all()
    depertmentlist=DepartmentM.objects.all()
    products = Inventory_Product_Entry.objects.all()
    suppliers = Inventory_Supplier_Entry.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        producets_pp = Product_PurchaseM.objects.raw('select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s and User_Branch_id=%s',[search,request.user.last_name])
        datasall = Product_PurchaseM.objects.filter(Invoice_no=search,User_Branch=request.user.last_name)
        bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')


        return render(request, 'inventory/forms/product_purchage.html',
                      {'producets_pp': producets_pp, 'datasall': datasall, 'bill': bill, 'products':products,'suppliers':suppliers,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'company':company})
    else:
        bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
        return render(request,'inventory/forms/product_purchage.html',{'user_current_branch':user_current_branch,'user_branch':user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'bill':bill,'company':company,'products':products,'suppliers':suppliers})


def invontory_product_purchase_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)

    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        user = request.user.id
        branchs=Branch_Infoamtion.objects.get(id=request.user.last_name)
        createuser = User.objects.get(id=user)
        p_name = request.POST.getlist('p_name')
        s_name = request.POST.getlist('s_name')
        qtt = request.POST.getlist('qtt')
        price = request.POST.getlist('price')
        orantyy = request.POST.getlist('orantyy')
        orantysdate = request.POST.getlist('orantysdate')

        id = request.POST.getlist('id')
        invoice = request.POST.get('invoice')
        if Product_PurchaseM.objects.filter(Invoice_no=invoice).exists():
            bill = Product_PurchaseM.objects.raw(
                'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
            messages.info(request, 'Invoice Number already registered ')
            return render(request, 'inventory/message.html', {'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:

            if bnumber is None:
                c = min([len(p_name),len(s_name),len(qtt),len(price),len(orantyy),len(orantysdate)])
                for i in range(c):

                    pr_name=Inventory_Product_Entry.objects.get(id=p_name[i])
                    su_name=Inventory_Supplier_Entry.objects.get(id=s_name[i])
                    if orantysdate[i] != None:
                        date=Product_PurchaseM(Product_Name=pr_name,Product_Supplier_Name=su_name,Quantity=qtt[i],Price=price[i],User_Branch=branchs,userc=createuser,Invoice_no=invoice,Oranty_year=orantyy[i],Oranty_start_date=orantysdate[i])
                        date.save()
                    else:
                        date = Product_PurchaseM(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                                                 Price=price[i], User_Branch=branchs, userc=createuser,
                                                 Invoice_no=invoice, Oranty_year=orantyy[i],
                                                 Oranty_start_date='0001-01-01')
                        date.save()
                    bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
                messages.info(request, 'Data Save')
                return render(request, 'inventory/message.html', {'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
            else:
                bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')

                producets_pp = Product_PurchaseM.objects.raw('select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s',[bnumber])
                data=Product_PurchaseM.objects.filter(Invoice_no=bnumber)
                # for x in data

                c = min([len(p_name), len(s_name), len(qtt), len(price),len(id),len(orantyy),len(orantysdate)])
                for i in range(c):

                    pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                    su_name = Inventory_Supplier_Entry.objects.get(id=s_name[i])
                    # date = Product_PurchaseM.objects.filter(Invoice_no=a).update(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                    #                          Price=price[i], User_Branch=branchs, userc=createuser, Invoice_no=bnumber)
                    if orantysdate[i] != "":
                        data = Product_PurchaseM.objects.get(id=id[i])
                        data.Product_Name=pr_name
                        data.Product_Supplier_Name=su_name
                        data.Quantity=qtt[i]
                        data.Price=price[i]
                        data.userc = createuser
                        data.User_Branch=branchs
                        data.Invoice_no=bnumber
                        data.Oranty_year=orantyy[i]
                        data.Oranty_start_date=orantysdate[i]
                        data.save()
                    else:
                        data = Product_PurchaseM.objects.get(id=id[i])
                        data.Product_Name = pr_name
                        data.Product_Supplier_Name = su_name
                        data.Quantity = qtt[i]
                        data.Price = price[i]
                        data.userc = createuser
                        data.User_Branch = branchs
                        data.Invoice_no = bnumber
                        data.Oranty_year = orantyy[i]
                        data.Oranty_start_date = '0001-01-01'
                        data.save()
                messages.info(request, 'Data Update')
                return render(request,'inventory/message.html',{'producets_pp': producets_pp,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})



def purchage_info_pdf_demoV(request,Invoice_no=0):
    invoice_number=Product_PurchaseM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no, userc_id from project_product_purchasem ppp WHERE Invoice_no =%s and User_Branch_id=%s',[Invoice_no,request.user.last_name])
    purchase_invoice=Product_PurchaseM.objects.raw('select id=0 as id, Product_Name_id ,Product_Supplier_Name_id ,Quantity,Price, Quantity*Price as Total from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',[Invoice_no,request.user.last_name])
    totals=Product_PurchaseM.objects.raw('select id=0 as id, sum(Quantity*Price ) as ttotal from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',[Invoice_no,request.user.last_name])
    for x in totals:
        amount=num2words(x.ttotal, lang="en_IN")
    template_path = 'inventory/reports/purchage_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'purchase_invoice':purchase_invoice,'invoice_number':invoice_number,'totals':totals,'amount':amount}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def purchage_info_pdfV(request,Invoice_no=0):
    invoice_number=Product_PurchaseM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no, userc_id from project_product_purchasem ppp WHERE Invoice_no =%s  and User_Branch_id=%s',[Invoice_no, request.user.last_name])
    purchase_invoice=Product_PurchaseM.objects.raw('select id=0 as id, Product_Name_id ,Product_Supplier_Name_id ,Quantity,Price, Quantity*Price as Total from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',[Invoice_no,request.user.last_name])
    totals=Product_PurchaseM.objects.raw('select id=0 as id, sum(Quantity*Price ) as ttotal from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',[Invoice_no,request.user.last_name])
    for x in totals:
        amount=num2words(x.ttotal, lang="en_IN")
    template_path = 'inventory/reports/purchage_info_pdf.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company':company,'path':path,'purchase_invoice':purchase_invoice,'invoice_number':invoice_number,'totals':totals,'amount':amount}
    response = HttpResponse(content_type='application/pdf')
    # for downlode
    # response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    response['Content-Disposition'] = 'filename="reports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view

    abc = Product_PurchaseM.objects.filter(Edits=None,Invoice_no=Invoice_no)
    if abc:
        for x in abc:
            data = Product_PurchaseM.objects.get(id=x.id)
            data.Edits = 1
            data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def invontory_product_purchase_select_infoV(request):
    products = Inventory_Product_Entry.objects.all()
    suppliers = Inventory_Supplier_Entry.objects.all()

    return render(request,'inventory/forms/product_purchase_select.html',{'products':products,'suppliers':suppliers})


def purchage_info_adjustmentV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist=DesignationM.objects.all()
    depertmentlist=DepartmentM.objects.all()
    products = Inventory_Product_Entry.objects.all()
    suppliers = Inventory_Supplier_Entry.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        producets_pp = Product_PurchaseM.objects.raw('select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s and User_Branch_id=%s',[search,request.user.last_name])
        datasall = Product_PurchaseM.objects.filter(Invoice_no=search,User_Branch=request.user.last_name)
        bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')


        return render(request, 'inventory/forms/product_purchage_adjustment.html',
                      {'producets_pp': producets_pp, 'datasall': datasall, 'bill': bill, 'products':products,'suppliers':suppliers,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'company':company})
    else:
        bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
        return render(request,'inventory/forms/product_purchage_adjustment.html',{'user_current_branch':user_current_branch,'user_branch':user_branch,'designationlist':designationlist,'depertmentlist':depertmentlist,'bill':bill,'company':company,'products':products,'suppliers':suppliers})


def purchage_info_adjustment_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)

    if request.method=='POST':
        bnumber=request.POST.get('Bnumber')
        user = request.user.id
        branchs=Branch_Infoamtion.objects.get(id=request.user.last_name)
        createuser = User.objects.get(id=user)
        p_name = request.POST.getlist('p_name')
        s_name = request.POST.getlist('s_name')
        qtt = request.POST.getlist('qtt')
        price = request.POST.getlist('price')
        id = request.POST.getlist('id')
        invoice = request.POST.get('invoice')
        if bnumber is None:
            c = min([len(p_name),len(s_name),len(qtt),len(price)])
            for i in range(c):
                pr_name=Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name=Inventory_Supplier_Entry.objects.get(id=s_name[i])
                date=Product_PurchaseM(Product_Name=pr_name,Product_Supplier_Name=su_name,Quantity=qtt[i],Price=price[i],User_Branch=branchs,userc=createuser,Invoice_no=invoice)
                date.save()
                bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
            messages.info(request, 'Data Save')
            return render(request, 'inventory/message.html', {'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})
        else:
            bill = Product_PurchaseM.objects.raw('select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')

            producets_pp = Product_PurchaseM.objects.raw('select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s',[bnumber])
            data=Product_PurchaseM.objects.filter(Invoice_no=bnumber)
            # for x in data

            c = min([len(p_name), len(s_name), len(qtt), len(price),len(id)])
            for i in range(c):
                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Inventory_Supplier_Entry.objects.get(id=s_name[i])
                # date = Product_PurchaseM.objects.filter(Invoice_no=a).update(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                #                          Price=price[i], User_Branch=branchs, userc=createuser, Invoice_no=bnumber)
                data = Product_PurchaseM.objects.get(id=id[i])
                data.Product_Name=pr_name
                data.Product_Supplier_Name=su_name
                data.Quantity=qtt[i]
                data.Price=price[i]
                data.userc = createuser
                data.User_Branch=branchs
                data.Invoice_no=bnumber
                data.save()
            messages.info(request, 'Data Update')
            return render(request,'inventory/message.html',{'producets_pp': producets_pp,'bill':bill,'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})











def TestV(request):
    return render(request,'test.html')




