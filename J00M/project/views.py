from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
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
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from pathlib import Path
import os
from num2words import num2words
import datetime
from django.core import serializers
import json
from django.db.models import F, Sum
# send html mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .resources import *
from tablib import Dataset

from django.db import connection


company = Company_Information.objects.filter(id=1)


@login_required(login_url='/loging/')
def index(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    employees=Hr_Employees_infoM.objects.filter(Department__Name='IT')[:3]

    ds=Product_PurchaseM.objects.all()
    for y in ds:
        ass = datetime.datetime.now().date()
        dst=int(y.Oranty_year * 365)
        uudd=(y.Oranty_start_date + datetime.timedelta(days=dst))
        gf=uudd-ass
        for x in employees:
            abc=x.Email
            product_name=y.Product_Name
            if gf.days==3:
                subject = f'license expiry {product_name}'
                message = f'Dear {x.Employees_Name} , there are {gf.days} days left to license expiry of {product_name}, so take the necessary step as soon as possible.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [abc]
                send_mail(subject, message, email_from, recipient_list)

    return render(request, 'index.html',
                  {'company': company, 'user_branch': user_branch, 'user_current_branch': user_current_branch})


def branch_changeV(request):
    branch_c = request.POST.get('brnchselect')
    print(branch_c)
    users = User.objects.get(username=request.user.username)
    users.last_name = branch_c
    users.save()

    return redirect('/')


def loginV(request):
    return render(request, 'loging.html', {'company': company})


def otpV(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = auth.authenticate(username=name, password=password)
        if user is not None:
            # auth.login(request, user)
            users = UserProfileM.objects.filter(user=user.id).first()
            otps = str(random.randint(1000, 9999))
            users.otp = otps
            users.save()
            request.session['name'] = name
            request.session['password'] = password
            for x in company:
                subject = f'OTP {x.Company_Name}'
                message = f'Hi {user.username}, thank you for Trying to Login. Your OTP number is {otps}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [users.Email]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, 'otppages.html', {'company': company})
        messages.info(request, 'User is not valid')
    return redirect('/loging/')


def software_admin_user_create_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
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
                                        Image=image, Email=email)
                    sing.save()
                    c = min([len(branch_code)])
                    for i in range(c):
                        # users=User.objects.get(pk=request.user.id)
                        Branch = Branch_Infoamtion.objects.get(id=branch_code[i])
                        data = Software_Permittion_Branch.objects.create(user=user, Branch=Branch)
                    cds = min([len(module_code)])
                    for x in range(cds):
                        module = Software_Permittion_MainM.objects.get(id=module_code[x])
                        data_module = Software_Permittion_Module.objects.create(user=user, Software_Permition=module)
                    messages.info(request, 'Data Saved')
                return render(request, 'software_admin/forms/message.html',
                              {'company': company, 'user_current_branch': user_current_branch,
                               'user_branch': user_branch})

        else:
            c = min([len(branch_code)])
            for i in range(c):
                dd = Branch_Infoamtion.objects.get(id=branch_code[i])
                users = User.objects.get(id=userid)
                branch = Software_Permittion_Branch.objects.filter(user=users).update_or_create(Branch=dd, user=users)

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
        return render(request, 'software_admin/forms/message.html',
                      {'company': company, 'user_branch': user_branch, 'user_current_branch': user_current_branch})


def finalloginV(request):
    name = request.session['name']
    password = request.session['password']
    otpf = request.POST.get('otps')
    user = auth.authenticate(username=name, password=password)
    users = UserProfileM.objects.filter(user=user.id).first()
    if otpf == users.otp:
        user = User.objects.get(id=users.user.id)
        auth.login(request, user)
        return redirect('/')
    else:
        messages.info(request, 'OTP NUMBER IS WRONG')
        return render(request, 'otppages.html', {'company': company})


@login_required(login_url='/loging/')
def logoutV(request):
    auth.logout(request)
    return redirect('/loging/')


def software_admin_user_createV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        user_name = User.objects.get(id=search)
        user_ss = User.objects.filter(username=user_name)
        branchs = Software_Permittion_Branch.objects.filter(user=user_name)
        permission = Software_Permittion_Module.objects.filter(user=user_name)
        users = UserProfileM.objects.all().count()
        branch_select = Branch_Infoamtion.objects.all()
        permittion_select_all = Software_Permittion_MainM.objects.raw(
            'select id,Sub_Name from project_software_permittion_mainm')
        return render(request, 'software_admin/forms/user_create.html',
                      {'branch_select': branch_select, 'permittion_select_all': permittion_select_all, 'users': users,
                       'branchs': branchs, 'permission': permission, 'user_ss': user_ss,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch, 'company': company})
    else:
        users = UserProfileM.objects.all().count()
        branch_select = Branch_Infoamtion.objects.all()
        permittion_select_all = Software_Permittion_MainM.objects.raw(
            'select id,Sub_Name from project_software_permittion_mainm')
        return render(request, 'software_admin/forms/user_create.html',
                      {'user_branch': user_branch, 'branch_select': branch_select,
                       'permittion_select_all': permittion_select_all, 'users': users,
                       'user_current_branch': user_current_branch, 'company': company})


def software_admin_user_create_branchV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    branch_select = Branch_Infoamtion.objects.all()
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request, 'software_admin/forms/branch_select_user.html',
                  {'branch_select': branch_select, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch, 'company': company})


def software_admin_user_create_moduleV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    permittion_select_all = Software_Permittion_MainM.objects.raw(
        'select DISTINCT id,Sub_Name from project_software_permittion_mainm')

    return render(request, 'software_admin/forms/module_select_user.html',
                  {'user_branch': user_branch, 'permittion_select_all': permittion_select_all,
                   'user_current_branch': user_current_branch, 'company': company})


@login_required(login_url='/loging/')
def software_admin_dashboardV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request, 'software_admin/software_admin_dashboard.html',
                  {'company': company, 'user_current_branch': user_current_branch, 'user_branch': user_branch})


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
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = Company_Information.objects.all().count()
        return render(request, 'software_admin/forms/company_info.html',
                      {'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})


@login_required(login_url='/loging/')
def software_admin_company_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
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
            ddsa = request.FILES['authres']
            store = FileSystemStorage()
            filenames = store.save(ddsa.name, ddsa)
            profiles_pic_url = store.url(filenames)
            date = Company_Information(id=id, Company_Name=cname, Company_Address=caddress, Company_Email=cemail,
                                       Company_Phone=cphone,
                                       Company_Fax=cfax, create_user=createuser, Company_Web_site=cweb,
                                       Company_Short_Name=cshort, logo=image,Authorization=ddsa)
            date.save()
            datas = Company_Information.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Company_Information.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
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
            if request.method == 'POST' and request.FILES:
                image = request.FILES['logo']
                store = FileSystemStorage()
                filename = store.save(image.name, image)
                profile_pic_url = store.url(filename)
                data.logo = image
                ddsa = request.FILES['authres']
                store = FileSystemStorage()
                filenames = store.save(ddsa.name, ddsa)
                profiles_pic_url = store.url(filenames)
                data.Authorization = ddsa
                data.save()
            else:
                datas = Company_Information.objects.filter(id=bnumber)
                for x in datas:
                    data.logo = x.logo
                    data.Authorization = x.Authorization
                    data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def software_admin_company_info_demo_pdfV(request, id=0):
    company_info = Company_Information.objects.filter(id=id)
    template_path = 'software_admin/reports/Company_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'company_info': company_info}
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


def software_admin_company_info_pdfV(request, id=0):
    company_info = Company_Information.objects.filter(id=id)
    template_path = 'software_admin/reports/Company_info_pdf_demo.html'
    context = {'company': company, 'company_info': company_info}
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
    data = Company_Information.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def EditV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    company_info = request.POST.get('company')
    branch_info = request.POST.get('branch')
    department_info = request.POST.get('depertment_info')
    designation_info = request.POST.get('designation_info')
    bank_info = request.POST.get('bank_info')
    deposit_bank_info = request.POST.get('dbank_info')
    bank_branch_info = request.POST.get('bank_branch_info')
    deposit_bank_branch_info = request.POST.get('dbank_branch_info')
    product_info = request.POST.get('product_info')
    suppler_info = request.POST.get('supplier_info')
    product_purchase_info = request.POST.get('product_purchase_info')
    product_issue_info = request.POST.get('product_issue_info')
    voyageform_info = request.POST.get('voyageform_info')
    voyageto_info = request.POST.get('voyageto_info')
    voyagevia_info = request.POST.get('voyagevia_info')
    transit_info = request.POST.get('transit_info')
    marine_quotation = request.POST.get('marinequotation')
    if company_info:
        company_edit = Company_Information.objects.filter(id=company_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'company_edit': company_edit, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})
    elif branch_info:
        branch_edit = Branch_Infoamtion.objects.filter(id=branch_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'branch_edit': branch_edit, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})
    elif department_info:
        department_edit = DepartmentM.objects.filter(id=department_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'department_edit': department_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif designation_info:
        designation_edit = DesignationM.objects.filter(id=designation_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'designation_edit': designation_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif bank_info:
        bank_edit = BankM.objects.filter(id=bank_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'bank_edit': bank_edit, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})
    elif deposit_bank_info:
        dbank_edit = Deposit_Bank_BranchM.objects.filter(id=deposit_bank_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'dbank_edit': dbank_edit, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})
    elif bank_branch_info:
        dbank_branch_edit = Bank_BranchM.objects.filter(id=bank_branch_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'dbank_branch_edit': dbank_branch_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif deposit_bank_branch_info:
        bank_branch_edit = Deposit_Bank_BranchM.objects.filter(id=deposit_bank_branch_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'bank_branch_edit': bank_branch_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif product_info:
        product_edit = Inventory_Product_Entry.objects.filter(id=product_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'product_edit': product_edit, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})
    elif suppler_info:
        supplier_edit = Inventory_Supplier_Entry.objects.filter(id=suppler_info)
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'supplier_edit': supplier_edit, 'company': company, 'user_current_branch': user_current_branch,
                       'user_branch': user_branch})
    elif product_purchase_info:
        product_purchase_edit = Product_PurchaseM.objects.raw(
            'select DISTINCT id=0 as id,Invoice_no,Edits from project_product_purchasem ppp WHERE Invoice_no =%s',
            [product_purchase_info])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'product_purchase_edit': product_purchase_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif product_issue_info:
        product_issue_edit = Product_issueM.objects.raw(
            'select DISTINCT id=0 as id,Invoice_no,Edits from project_Product_issueM ppp WHERE Invoice_no =%s',
            [product_issue_info])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'product_issue_edit': product_issue_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})

    elif voyageform_info:
        voyageform_edit = VoyageForm.objects.raw(
            'select DISTINCT id,Edits from project_voyageform ppp WHERE id =%s',
            [voyageform_info])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'voyageform_edit': voyageform_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif voyageto_info:
        voyageto_edit = VoyageTo.objects.raw(
            'select DISTINCT id,Edits from project_VoyageTo ppp WHERE id =%s',
            [voyageto_info])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'voyageto_edit': voyageto_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif voyagevia_info:
        voyagevia_edit = VoyageVia.objects.raw(
            'select DISTINCT id,Edits from project_voyagevia ppp WHERE id =%s',
            [voyagevia_info])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'voyagevia_edit': voyagevia_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif transit_info:
        transit_edit = TransitBy.objects.raw(
            'select DISTINCT id,Edits from project_transitby ppp WHERE id =%s',
            [transit_info])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'transit_edit': transit_edit, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    elif marine_quotation:
        marinequotation = TransitBy.objects.raw(
            'select id,Bill_No,Bill_date,Marine_Amount,Ware_Amount,Net_Amount,Vat_Amount,Stump_Amount,Gross_Amount,Edits from project_marinequatationm mq where bill_no=%s',
            [marine_quotation])
        return render(request, 'software_admin/forms/Edit_message.html',
                      {'marinequotation': marinequotation, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})


    return render(request, 'software_admin/forms/All_Edit.html',
                  {'company': company, 'user_current_branch': user_current_branch, 'user_branch': user_branch})


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
    dbank_id = request.POST.get('dBank_id')
    dbank_edit = request.POST.get('dBank_edit')
    bank_branch_id = request.POST.get('Bank_branch_id')
    bank_branch_edit = request.POST.get('Bank_branch_edit')
    dbank_branch_id = request.POST.get('dBank_branch_id')
    dbank_branch_edit = request.POST.get('dBank_branch_edit')
    product_edit_id = request.POST.get('product_id')
    product_edit_edit = request.POST.get('product_edite')
    supplier_edit_id = request.POST.get('supplier_id')
    supplier_edit_edit = request.POST.get('supplier_edite')
    product_purchase_inv = request.POST.get('product_purchase_inv')
    purchase_edite = request.POST.get('purchase_edite')
    product_issue_inv = request.POST.get('product_issue_inv')
    issue_edite = request.POST.get('issue_edite')
    voyageform_inv = request.POST.get('voyageform_inv')
    voyageforms_edite = request.POST.get('voyageform_edite')
    voyageto_inv = request.POST.get('voyageto_inv')
    voyageto_edite = request.POST.get('voyageto_edite')
    voyagevia_inv = request.POST.get('voyagevia_inv')
    voyagevia_edite = request.POST.get('voyagevia_edite')
    transit_inv = request.POST.get('transit_inv')
    transit_edite = request.POST.get('transit_edite')


    Bill_nos = request.POST.get('bill_no')
    Bill_date = request.POST.get('billdate')
    marine_amount = request.POST.get('marineamount')
    ws_amount = request.POST.get('wsamount')
    net_amount = request.POST.get('netamount')
    vat_amount = request.POST.get('vatamount')
    stump_amount = request.POST.get('stumpamount')
    gross_amount = request.POST.get('grossamount')


    if company_info:
        company_edits = Company_Information.objects.get(id=company_info)
        company_edits.Edits = cedit
        company_edits.save()
    elif branchids:
        branch_edits = Branch_Infoamtion.objects.get(id=branchids)
        branch_edits.Edits = bedits
        branch_edits.save()
    elif department_id:
        department_edits = DepartmentM.objects.get(id=department_id)
        department_edits.Edits = department_edit
        department_edits.save()
    elif designation_id:
        designation_edits = DesignationM.objects.get(id=designation_id)
        designation_edits.Edits = designation_edit
        designation_edits.save()
    elif bank_id:
        bank_edits = BankM.objects.get(id=bank_id)
        bank_edits.Edits = bank_edit
        bank_edits.save()
    elif dbank_id:
        bank_edits = Deposit_BankM.objects.get(id=dbank_id)
        bank_edits.Edits = dbank_edit
        bank_edits.save()
    elif bank_branch_id:
        bank_branch_edits = Bank_BranchM.objects.get(id=bank_branch_id)
        bank_branch_edits.Edits = bank_branch_edit
        bank_branch_edits.save()
    elif dbank_branch_id:
        bank_branch_edits = Deposit_Bank_BranchM.objects.get(id=dbank_branch_id)
        bank_branch_edits.Edits = dbank_branch_edit
        bank_branch_edits.save()
    elif product_edit_id:
        product_edits = Inventory_Product_Entry.objects.get(id=product_edit_id)
        product_edits.Edits = product_edit_edit
        product_edits.save()
    elif supplier_edit_id:
        supplier_edits = Inventory_Supplier_Entry.objects.get(id=supplier_edit_id)
        supplier_edits.Edits = supplier_edit_edit
        supplier_edits.save()
    elif product_purchase_inv:
        abc = Product_PurchaseM.objects.filter(Invoice_no=product_purchase_inv)
        for x in abc:
            purchasep_edits = Product_PurchaseM.objects.get(id=x.id)
            purchasep_edits.Edits = purchase_edite
            purchasep_edits.save()
    elif product_issue_inv:
        abc = Product_issueM.objects.filter(Invoice_no=product_issue_inv)
        for x in abc:
            issue_edits = Product_issueM.objects.get(id=x.id)
            issue_edits.Edits = issue_edite
            issue_edits.save()
    elif voyageform_inv:
        abc = VoyageForm.objects.filter(id=voyageform_inv)
        for x in abc:
            issue_edits = VoyageForm.objects.get(id=x.id)
            issue_edits.Edits = voyageforms_edite
            issue_edits.save()
    elif voyageto_inv:
        abc = VoyageTo.objects.filter(id=voyageto_inv)
        for x in abc:
            issue_edits = VoyageTo.objects.get(id=x.id)
            issue_edits.Edits = voyageto_edite
            issue_edits.save()

    elif voyagevia_inv:
        abc = VoyageVia.objects.filter(id=voyagevia_inv)
        for x in abc:
            issue_edits = VoyageVia.objects.get(id=x.id)
            issue_edits.Edits = voyagevia_edite
            issue_edits.save()
    elif transit_inv:
        abc = TransitBy.objects.filter(id=transit_inv)
        for x in abc:
            issue_edits = TransitBy.objects.get(id=x.id)
            issue_edits.Edits = transit_edite
            issue_edits.save()
    elif Bill_nos:
        abc = MarineQuatationM.objects.filter(Bill_No=Bill_nos)
        for x in abc:
            issue_edits = MarineQuatationM.objects.get(id=x.id)
            issue_edits.Bill_No = Bill_nos
            issue_edits.Bill_date = Bill_date
            issue_edits.Marine_Amount = marine_amount
            issue_edits.Ware_Amount = ws_amount
            issue_edits.Net_Amount = net_amount
            issue_edits.Vat_Amount = vat_amount
            issue_edits.Stump_Amount = stump_amount
            issue_edits.Gross_Amount = gross_amount
            issue_edits.save()
    messages.info(request, 'Data Update')

    return redirect('/software/admin/edit/')


def hr_dashboardV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request, 'hr/hr_dashboard.html',
                  {'company': company, 'user_current_branch': user_current_branch, 'user_branch': user_branch})


def hr_branch_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Branch_Infoamtion.objects.filter(id=search)
        datasall = Branch_Infoamtion.objects.filter(id=search)
        bill = Branch_Infoamtion.objects.all().count()
        return render(request, 'hr/forms/branch_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = Branch_Infoamtion.objects.all().count()
    return render(request, 'hr/forms/branch_info.html',
                  {'company': company, 'bill': bill, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_branch_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
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
            date = Branch_Infoamtion(id=id, Branch_Name=bname, Branch_Address=baddress, Branch_Email=bemail,
                                     Branch_Phone=bphone,
                                     Branch_Fax=bfax, create_user=createuser, Branch_Short_Name=bshort)
            date.save()
            datas = Branch_Infoamtion.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Branch_Infoamtion.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
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
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_branch_info_demo_pdfV(request, id=0):
    branch_info = Branch_Infoamtion.objects.filter(id=id)
    template_path = 'hr/reports/branch_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'branch_info': branch_info}
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


def hr_branch_info_pdfV(request, id=0):
    branch_info = Branch_Infoamtion.objects.filter(id=id)
    template_path = 'hr/reports/branch_info_pdf.html'
    context = {'company': company, 'branch_info': branch_info}
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
    data = Branch_Infoamtion.objects.get(id=id)
    data.Edits = 1
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
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = DepartmentM.objects.all().count()
    return render(request, 'hr/forms/department_info.html',
                  {'company': company, 'bill': bill, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_department_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = DepartmentM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('Dname')

        if bnumber is None:
            date = DepartmentM(id=id, Name=dname, create_user=createuser)
            date.save()
            datas = DepartmentM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = DepartmentM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = DepartmentM.objects.all().count()
            datas = DepartmentM.objects.filter(id=bnumber)
            data = DepartmentM.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_department_info_demo_pdfV(request, id=0):
    department_info = DepartmentM.objects.filter(id=id)
    template_path = 'hr/reports/department_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'department_info': department_info}
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


def hr_department_info_pdfV(request, id=0):
    department_info = DepartmentM.objects.filter(id=id)
    template_path = 'hr/reports/department_info_pdf.html'
    context = {'company': company, 'department_info': department_info}
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
    data = DepartmentM.objects.get(id=id)
    data.Edits = 1
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
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = DesignationM.objects.all().count()
    return render(request, 'hr/forms/designation_info.html',
                  {'company': company, 'bill': bill, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_designation_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = DesignationM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        designation_n = request.POST.get('Designation_n')

        if bnumber is None:
            date = DesignationM(id=id, Name=designation_n, create_user=createuser)
            date.save()
            datas = DesignationM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = DesignationM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = DesignationM.objects.all().count()
            datas = DesignationM.objects.filter(id=bnumber)
            data = DesignationM.objects.get(id=bnumber)
            data.Name = designation_n
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_designation_info_demo_pdfV(request, id=0):
    designation_info = DesignationM.objects.filter(id=id)
    template_path = 'hr/reports/designation_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'designation_info': designation_info}
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


def hr_designation_info_pdfV(request, id=0):
    designation_info = DesignationM.objects.filter(id=id)
    template_path = 'hr/reports/designation_info_pdf.html'
    context = {'company': company, 'designation_info': designation_info}
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
    data = DesignationM.objects.get(id=id)
    data.Edits = 1
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
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = BankM.objects.all().count()
    return render(request, 'hr/forms/bank_info.html',
                  {'company': company, 'bill': bill, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_bank_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = BankM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        bank_n = request.POST.get('Bank_n')

        if bnumber is None:
            date = BankM(id=id, Name=bank_n, create_user=createuser)
            date.save()
            datas = BankM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = BankM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = BankM.objects.all().count()
            datas = BankM.objects.filter(id=bnumber)
            data = BankM.objects.get(id=bnumber)
            data.Name = bank_n
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_bank_info_demo_pdfV(request, id=0):
    bank_info = BankM.objects.filter(id=id)
    template_path = 'hr/reports/bank_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'bank_info': bank_info}
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


def hr_bank_info_pdfV(request, id=0):
    bank_info = BankM.objects.filter(id=id)
    template_path = 'hr/reports/bank_info_pdf.html'
    context = {'company': company, 'bank_info': bank_info}
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
    data = BankM.objects.get(id=id)
    data.Edits = 1
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
        bank_name = BankM.objects.all()
        return render(request, 'hr/forms/bank_branch_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company, 'bank_name': bank_name,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bank_name = BankM.objects.all()
        bill = Bank_BranchM.objects.all().count()
    return render(request, 'hr/forms/bank_branch_info.html',
                  {'company': company, 'bill': bill, 'bank_name': bank_name, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_bank_branch_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
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
            date = Bank_BranchM(id=id, Bank_Name=bankname, Bank_Branch=bank_branch_n, Bank_Branch_Address=bank_branch_a,
                                Bank_Branch_Phone=bank_branch_p, Bank_Branch_Mobile=bank_branch_m,
                                Bank_Branch_Email=bank_branch_e, create_user=createuser)
            date.save()
            datas = Bank_BranchM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Bank_BranchM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Bank_BranchM.objects.all().count()
            datas = Bank_BranchM.objects.filter(id=bnumber)
            data = Bank_BranchM.objects.get(id=bnumber)
            data.Bank_Name = bankname
            data.Bank_Branch = bank_branch_n
            data.Bank_Branch_Address = bank_branch_a
            data.Bank_Branch_Phone = bank_branch_p
            data.Bank_Branch_Mobile = bank_branch_m
            data.Bank_Branch_Email = bank_branch_e
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_bank_branch_info_demo_pdfV(request, id=0):
    bank_branch_info = Bank_BranchM.objects.filter(id=id)
    template_path = 'hr/reports/bank_branch_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'bank_branch_info': bank_branch_info}
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


def hr_bank_branch_info_pdfV(request, id=0):
    bank_branch_info = Bank_BranchM.objects.filter(id=id)
    template_path = 'hr/reports/bank_branch_info_pdf.html'
    context = {'company': company, 'bank_branch_info': bank_branch_info}
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
    data = Bank_BranchM.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response





def hr_deposit_bank_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Deposit_BankM.objects.filter(id=search)
        datasall = Deposit_BankM.objects.filter(id=search)
        bill = Deposit_BankM.objects.all().count()
        return render(request, 'hr/forms/deposit_bank_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = Deposit_BankM.objects.all().count()
    return render(request, 'hr/forms/deposit_bank_info.html',
                  {'company': company, 'bill': bill, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_deposit_bank_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = Deposit_BankM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        bank_n = request.POST.get('Bank_n')

        if bnumber is None:
            date = Deposit_BankM(id=id, Name=bank_n, create_user=createuser)
            date.save()
            datas = Deposit_BankM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Deposit_BankM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Deposit_BankM.objects.all().count()
            datas = Deposit_BankM.objects.filter(id=bnumber)
            data = Deposit_BankM.objects.get(id=bnumber)
            data.Name = bank_n
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_deposit_bank_info_demo_pdfV(request, id=0):
    bank_info = Deposit_BankM.objects.filter(id=id)
    template_path = 'hr/reports/deposit_bank_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'bank_info': bank_info}
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


def hr_deposit_bank_info_pdfV(request, id=0):
    bank_info = Deposit_BankM.objects.filter(id=id)
    template_path = 'hr/reports/deposit_bank_info_pdf.html'
    context = {'company': company, 'bank_info': bank_info}
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
    data = Deposit_BankM.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_deposit_bank_branch_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Deposit_Bank_BranchM.objects.filter(id=search)
        datasall = Deposit_Bank_BranchM.objects.filter(id=search)
        bill = Deposit_Bank_BranchM.objects.all().count()
        bank_name = Deposit_BankM.objects.all()
        return render(request, 'hr/forms/deposit_bank_branch_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company, 'bank_name': bank_name,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bank_name = Deposit_BankM.objects.all()
        bill = Deposit_Bank_BranchM.objects.all().count()
    return render(request, 'hr/forms/deposit_bank_branch_info.html',
                  {'company': company, 'bill': bill, 'bank_name': bank_name, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_deposit_bank_branch_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = Deposit_Bank_BranchM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        bank_n = request.POST.get('Bank_n')
        bankname = Deposit_BankM.objects.get(id=bank_n)
        bank_branch_n = request.POST.get('Bank_Branch_n')
        bank_branch_a = request.POST.get('Bank_Branch_a')
        bank_branch_p = request.POST.get('Bank_Branch_p')
        bank_branch_m = request.POST.get('Bank_Branch_m')
        bank_branch_e = request.POST.get('Bank_Branch_e')

        if bnumber is None:
            date = Deposit_Bank_BranchM(id=id, Bank_Name=bankname, Bank_Branch=bank_branch_n, Bank_Branch_Address=bank_branch_a,
                                Bank_Branch_Phone=bank_branch_p, Bank_Branch_Mobile=bank_branch_m,
                                Bank_Branch_Email=bank_branch_e, create_user=createuser)
            date.save()
            datas = Deposit_Bank_BranchM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Deposit_Bank_BranchM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Deposit_Bank_BranchM.objects.all().count()
            datas = Deposit_Bank_BranchM.objects.filter(id=bnumber)
            data = Deposit_Bank_BranchM.objects.get(id=bnumber)
            data.Bank_Name = bankname
            data.Bank_Branch = bank_branch_n
            data.Bank_Branch_Address = bank_branch_a
            data.Bank_Branch_Phone = bank_branch_p
            data.Bank_Branch_Mobile = bank_branch_m
            data.Bank_Branch_Email = bank_branch_e
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def hr_deposit_bank_branch_info_demo_pdfV(request, id=0):
    bank_branch_info = Deposit_Bank_BranchM.objects.filter(id=id)
    template_path = 'hr/reports/deposit_bank_branch_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'bank_branch_info': bank_branch_info}
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


def hr_deposit_bank_branch_info_pdfV(request, id=0):
    bank_branch_info = Deposit_Bank_BranchM.objects.filter(id=id)
    template_path = 'hr/reports/deposit_bank_branch_info_pdf.html'
    context = {'company': company, 'bank_branch_info': bank_branch_info}
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
    data = Deposit_Bank_BranchM.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def hr_client_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = ClinetM.objects.filter(id=search)
        datasall = ClinetM.objects.filter(id=search)
        bill = ClinetM.objects.all().count()
        return render(request, 'hr/forms/client_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = ClinetM.objects.all().count()
    return render(request, 'hr/forms/client_info.html',
                  {'company': company, 'bill': bill, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_client_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = ClinetM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        branch=Branch_Infoamtion.objects.get(id=createuser.last_name)
        cname = request.POST.get('cname')


        if bnumber is None:
            date = ClinetM(id=id, Name=cname, create_user=createuser,Branch_Info=branch)
            date.save()
            datas = ClinetM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = ClinetM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            user = request.user.id
            createuser = User.objects.get(id=user)
            branch = Branch_Infoamtion.objects.get(id=createuser.last_name)
            bill = ClinetM.objects.all().count()
            datas = ClinetM.objects.filter(id=bnumber)
            data = ClinetM.objects.get(id=bnumber)
            data.Name = cname
            data.create_user = createuser
            data.Branch_Info = branch
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})

def hr_client_info_demo_pdfV(request, id=0):
    bank_info = ClinetM.objects.filter(id=id)
    template_path = 'hr/reports/client_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'bank_info': bank_info}
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


def hr_client_info_pdfV(request, id=0):
    bank_info = ClinetM.objects.filter(id=id)
    template_path = 'hr/reports/client_info_pdf.html'
    context = {'company': company, 'bank_info': bank_info}
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
    data = ClinetM.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_client_branch_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Client_BranchM.objects.filter(id=search)
        datasall = Client_BranchM.objects.filter(id=search)
        bill = Client_BranchM.objects.all().count()
        bank_name = ClinetM.objects.all()
        return render(request, 'hr/forms/client_branch_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company, 'bank_name': bank_name,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bank_name = ClinetM.objects.all()
        bill = Client_BranchM.objects.all().count()
    return render(request, 'hr/forms/client_branch_info.html',
                  {'company': company, 'bill': bill, 'bank_name': bank_name, 'user_current_branch': user_current_branch,
                   'user_branch': user_branch})


def hr_client_branch_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = Client_BranchM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        client_n = request.POST.get('client_n')
        clientname = ClinetM.objects.get(id=client_n)
        client_branch_n = request.POST.get('client_Branch_n')
        client_branch_a = request.POST.get('client_Branch_a')
        client_branch_p = request.POST.get('client_Branch_p')
        client_branch_m = request.POST.get('client_Branch_m')
        client_branch_e = request.POST.get('client_Branch_e')

        if bnumber is None:
            date = Client_BranchM(id=id, Client_Name=clientname, Client_Branch=client_branch_n, Client_Branch_Address=client_branch_a,
                                Client_Branch_Phone=client_branch_p, Client_Branch_Mobile=client_branch_m,
                                Client_Branch_Email=client_branch_e, create_user=createuser)
            date.save()
            datas = Client_BranchM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Client_BranchM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Client_BranchM.objects.all().count()
            datas = Client_BranchM.objects.filter(id=bnumber)
            data = Client_BranchM.objects.get(id=bnumber)
            data.Client_Name = clientname
            data.Client_Branch = client_branch_n
            data.Client_Branch_Address = client_branch_a
            data.Client_Branch_Phone = client_branch_p
            data.Client_Branch_Mobile = client_branch_m
            data.Client_Branch_Email = client_branch_e
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})

def hr_employees_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist = DesignationM.objects.all()
    depertmentlist = DepartmentM.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Hr_Employees_infoM.objects.filter(id=search)
        datasall = Hr_Employees_infoM.objects.filter(id=search)
        bill = Hr_Employees_infoM.objects.all().count()

        return render(request, 'hr/forms/employees_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'company': company})
    else:
        bill = Hr_Employees_infoM.objects.all().count()
        return render(request, 'hr/forms/employees_info.html',
                      {'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'bill': bill,
                       'company': company})


def hr_employees_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = Hr_Employees_infoM.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        Ename = request.POST.get('Ename')
        designation = request.POST.get('designation')
        designationss = DesignationM.objects.get(id=designation)
        department = request.POST.get('department')
        departmentss = DepartmentM.objects.get(id=department)
        paddress = request.POST.get('paddress')
        paraddress = request.POST.get('paraddress')
        ephone = request.POST.get('ephone')
        eemail = request.POST.get('eemail')
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
            date = Hr_Employees_infoM(id=id, Employees_Name=Ename, Designation=designationss, Department=departmentss,
                                      Present_Address=paddress, Permanent_Address=paraddress, Phone=ephone,
                                      Employees_Father_name=efather,
                                      Employees_Mother_name=emother, Employees_Blood=eblood, Employees_NID=nid,
                                      Last_Education_Qualification=edu,
                                      Last_Education_CGPA=cgp, Employees_Date_of_Birth=ebarth, Appointment_Date=adate,
                                      Joining_Date=jdate, userc=createuser,Email=eemail)
            date.save()
            datas = Hr_Employees_infoM.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Hr_Employees_infoM.objects.all().count()
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch, 'company': company})
        else:
            bill = Hr_Employees_infoM.objects.all().count()
            datas = Hr_Employees_infoM.objects.filter(id=bnumber)
            data = Hr_Employees_infoM.objects.get(id=bnumber)
            data.Employees_Name = Ename
            data.Designation = designationss
            data.Department = departmentss
            data.Present_Address = paddress
            data.Permanent_Address = paraddress
            data.Phone = ephone
            data.Employees_Father_name = efather
            data.Employees_Mother_name = emother
            data.Employees_Blood = eblood
            data.Employees_NID = nid
            data.Last_Education_Qualification = edu
            data.Last_Education_CGPA = cgp
            data.Employees_Date_of_Birth = ebarth
            data.Appointment_Date = adate
            data.Joining_Date = jdate
            data.create_user = createuser
            data.Email=eemail
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'hr/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch, 'company': company})


def software_admin_user_create_branch_deleteV(request, id=0):
    if id != 0:
        branch = Software_Permittion_Branch.objects.get(pk=id)
        branch.delete()
        messages.info(request, 'Data Delete')
    return render(request, 'hr/forms/message.html')


def software_admin_user_create_module_deleteV(request, id=0):
    if id != 0:
        module = Software_Permittion_Module.objects.get(pk=id)
        module.delete()
        messages.info(request, 'Data Delete')
    return render(request, 'hr/forms/message.html')


def software_admin_user_create_PDFV(request, id=0):
    user_info = UserProfileM.objects.all()
    template_path = 'software_admin/reports/user_info_pdf.html'
    context = {'company': company, 'user_info': user_info}
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
    return render(request, 'inventory/inventory_dashboard.html',
                  {'company': company, 'user_branch': user_branch, 'user_current_branch': user_current_branch})


def inventory_product_entryV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Inventory_Product_Entry.objects.filter(id=search)
        datasall = Inventory_Product_Entry.objects.filter(id=search)
        product_count = Inventory_Product_Entry.objects.all().count()
        return render(request, 'inventory/forms/product_entry.html',
                      {'datas': datas, 'datasall': datasall, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'product_count': product_count})
    else:
        product_count = Inventory_Product_Entry.objects.all().count()
    return render(request, 'inventory/forms/product_entry.html',
                  {'company': company, 'user_branch': user_branch, 'user_current_branch': user_current_branch,
                   'product_count': product_count})


def inventory_product_entry_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = Inventory_Product_Entry.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        product_n = request.POST.get('product_n')

        if bnumber is None:
            date = Inventory_Product_Entry(id=id, Product_Name=product_n, userc=createuser)
            date.save()
            datas = Inventory_Product_Entry.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Inventory_Product_Entry.objects.all().count()
            return render(request, 'inventory/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Inventory_Product_Entry.objects.all().count()
            datas = Inventory_Product_Entry.objects.filter(id=bnumber)
            data = Inventory_Product_Entry.objects.get(id=bnumber)
            data.Product_Name = product_n
            data.userc = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'inventory/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def inventory_product_demo_pdfV(request):
    product_info = Inventory_Product_Entry.objects.all()
    template_path = 'inventory/reports/inventory_product_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'product_info': product_info}
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
    context = {'company': company, 'product_info': product_info}
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
    abc = Inventory_Product_Entry.objects.filter(Edits=None)
    if abc:
        data = Inventory_Product_Entry.objects.get(Edits=None)
        data.Edits = 1
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
        supplier_count = Inventory_Supplier_Entry.objects.all().count()
        return render(request, 'inventory/forms/supplier_entry.html',
                      {'datas': datas, 'datasall': datasall, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'supplier_count': supplier_count})
    else:
        supplier_count = Inventory_Supplier_Entry.objects.all().count()
    return render(request, 'inventory/forms/supplier_entry.html',
                  {'company': company, 'user_branch': user_branch, 'user_current_branch': user_current_branch,
                   'supplier_count': supplier_count})


def inventory_supplier_entry_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = Inventory_Supplier_Entry.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        supplier_n = request.POST.get('supplier_n')
        supplier_a = request.POST.get('supplier_a')
        supplier_p = request.POST.get('supplier_p')
        supplier_e = request.POST.get('supplier_e')

        if bnumber is None:
            date = Inventory_Supplier_Entry(id=id, Supplier_Name=supplier_n, Supplier_Address=supplier_a,
                                            Supplier_Phone=supplier_p, Supplier_Email=supplier_e, userc=createuser)
            date.save()
            datas = Inventory_Supplier_Entry.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = Inventory_Supplier_Entry.objects.all().count()
            return render(request, 'inventory/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Inventory_Supplier_Entry.objects.all().count()
            datas = Inventory_Supplier_Entry.objects.filter(id=bnumber)
            data = Inventory_Supplier_Entry.objects.get(id=bnumber)
            data.Supplier_Name = supplier_n
            data.Supplier_Address = supplier_a
            data.Supplier_Phone = supplier_p
            data.Supplier_Email = supplier_e
            data.userc = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'inventory/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def inventory_supplier_demo_pdfV(request):
    supplier_info = Inventory_Supplier_Entry.objects.all()
    template_path = 'inventory/reports/inventory_supplier_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'supplier_info': supplier_info}
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
    context = {'company': company, 'supplier_info': supplier_info}
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
    abc = Inventory_Supplier_Entry.objects.filter(Edits=None)
    if abc:
        data = Inventory_Supplier_Entry.objects.get(Edits=None)
        data.Edits = 1
        data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def hr_employees_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist = DesignationM.objects.all()
    depertmentlist = DepartmentM.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = Hr_Employees_infoM.objects.filter(id=search)
        datasall = Hr_Employees_infoM.objects.filter(id=search)
        bill = Hr_Employees_infoM.objects.all().count()

        return render(request, 'hr/forms/employees_info.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'company': company})
    else:
        bill = Hr_Employees_infoM.objects.all().count()
        return render(request, 'hr/forms/employees_info.html',
                      {'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'bill': bill,
                       'company': company})


def invontory_product_purchase_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist = DesignationM.objects.all()
    depertmentlist = DepartmentM.objects.all()
    products = Inventory_Product_Entry.objects.all()
    suppliers = Inventory_Supplier_Entry.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        producets_pp = Product_PurchaseM.objects.raw(
            'select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s and User_Branch_id=%s',
            [search, request.user.last_name])
        datasall = Product_PurchaseM.objects.filter(Invoice_no=search, User_Branch=request.user.last_name)
        bill = Product_PurchaseM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')

        return render(request, 'inventory/forms/product_purchage.html',
                      {'producets_pp': producets_pp, 'datasall': datasall, 'bill': bill, 'products': products,
                       'suppliers': suppliers,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'company': company})
    else:
        bill = Product_PurchaseM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
        return render(request, 'inventory/forms/product_purchage.html',
                      {'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'bill': bill,
                       'company': company, 'products': products, 'suppliers': suppliers})


def invontory_product_purchase_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)

    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        user = request.user.id
        branchs = Branch_Infoamtion.objects.get(id=request.user.last_name)
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
            return render(request, 'inventory/message.html',
                          {'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:

            if bnumber is None:
                c = min([len(p_name), len(s_name), len(qtt), len(price), len(orantyy), len(orantysdate)])
                for i in range(c):

                    pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                    su_name = Inventory_Supplier_Entry.objects.get(id=s_name[i])
                    if orantysdate[i] != None:
                        date = Product_PurchaseM(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                                                 Price=price[i], User_Branch=branchs, userc=createuser,
                                                 Invoice_no=invoice, Oranty_year=orantyy[i],
                                                 Oranty_start_date=orantysdate[i])
                        date.save()
                    else:
                        date = Product_PurchaseM(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                                                 Price=price[i], User_Branch=branchs, userc=createuser,
                                                 Invoice_no=invoice, Oranty_year=orantyy[i],
                                                 Oranty_start_date='0001-01-01')
                        date.save()
                    bill = Product_PurchaseM.objects.raw(
                        'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
                messages.info(request, 'Data Save')
                return render(request, 'inventory/message.html',
                              {'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                               'user_branch': user_branch})
            else:
                bill = Product_PurchaseM.objects.raw(
                    'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')

                producets_pp = Product_PurchaseM.objects.raw(
                    'select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s',
                    [bnumber])
                data = Product_PurchaseM.objects.filter(Invoice_no=bnumber)
                # for x in data

                c = min([len(p_name), len(s_name), len(qtt), len(price), len(id), len(orantyy), len(orantysdate)])
                for i in range(c):

                    pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                    su_name = Inventory_Supplier_Entry.objects.get(id=s_name[i])
                    # date = Product_PurchaseM.objects.filter(Invoice_no=a).update(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                    #                          Price=price[i], User_Branch=branchs, userc=createuser, Invoice_no=bnumber)
                    if orantysdate[i] != "":
                        data = Product_PurchaseM.objects.get(id=id[i])
                        data.Product_Name = pr_name
                        data.Product_Supplier_Name = su_name
                        data.Quantity = qtt[i]
                        data.Price = price[i]
                        data.userc = createuser
                        data.User_Branch = branchs
                        data.Invoice_no = bnumber
                        data.Oranty_year = orantyy[i]
                        data.Oranty_start_date = orantysdate[i]
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
                return render(request, 'inventory/message.html',
                              {'producets_pp': producets_pp, 'bill': bill, 'company': company,
                               'user_current_branch': user_current_branch, 'user_branch': user_branch})


def purchage_info_pdf_demoV(request, Invoice_no=0):
    invoice_number = Product_PurchaseM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no, userc_id from project_product_purchasem ppp WHERE Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    purchase_invoice = Product_PurchaseM.objects.raw(
        'select id=0 as id, Product_Name_id ,Product_Supplier_Name_id ,Quantity,Price, Quantity*Price as Total from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    totals = Product_PurchaseM.objects.raw(
        'select id=0 as id, sum(Quantity*Price ) as ttotal from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    for x in totals:
        amount = num2words(x.ttotal, lang="en_IN")
    template_path = 'inventory/reports/purchage_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'purchase_invoice': purchase_invoice, 'invoice_number': invoice_number,
               'totals': totals, 'amount': amount}
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


def purchage_info_pdfV(request, Invoice_no=0):
    invoice_number = Product_PurchaseM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no, userc_id from project_product_purchasem ppp WHERE Invoice_no =%s  and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    purchase_invoice = Product_PurchaseM.objects.raw(
        'select id=0 as id, Product_Name_id ,Product_Supplier_Name_id ,Quantity,Price, Quantity*Price as Total from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    totals = Product_PurchaseM.objects.raw(
        'select id=0 as id, sum(Quantity*Price ) as ttotal from project_product_purchasem ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    for x in totals:
        amount = num2words(x.ttotal, lang="en_IN")
    template_path = 'inventory/reports/purchage_info_pdf.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'purchase_invoice': purchase_invoice, 'invoice_number': invoice_number,
               'totals': totals, 'amount': amount}
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

    abc = Product_PurchaseM.objects.filter(Edits=None, Invoice_no=Invoice_no)
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

    return render(request, 'inventory/forms/product_purchase_select.html',
                  {'products': products, 'suppliers': suppliers})


def purchage_info_adjustmentV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist = DesignationM.objects.all()
    depertmentlist = DepartmentM.objects.all()
    products = Inventory_Product_Entry.objects.all()
    suppliers = Inventory_Supplier_Entry.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        producets_pp = Product_PurchaseM.objects.raw(
            'select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s and User_Branch_id=%s',
            [search, request.user.last_name])
        datasall = Product_PurchaseM.objects.filter(Invoice_no=search, User_Branch=request.user.last_name)
        bill = Product_PurchaseM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')

        return render(request, 'inventory/forms/product_purchage_adjustment.html',
                      {'producets_pp': producets_pp, 'datasall': datasall, 'bill': bill, 'products': products,
                       'suppliers': suppliers,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'company': company})
    else:
        bill = Product_PurchaseM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
        return render(request, 'inventory/forms/product_purchage_adjustment.html',
                      {'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'bill': bill,
                       'company': company, 'products': products, 'suppliers': suppliers})


def purchage_info_adjustment_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)

    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        user = request.user.id
        branchs = Branch_Infoamtion.objects.get(id=request.user.last_name)
        createuser = User.objects.get(id=user)
        p_name = request.POST.getlist('p_name')
        s_name = request.POST.getlist('s_name')
        qtt = request.POST.getlist('qtt')
        price = request.POST.getlist('price')
        orantyy = request.POST.getlist('orantyy')
        orantysdate = request.POST.getlist('orantysdate')

        id = request.POST.getlist('id')
        invoice = request.POST.get('invoice')

        if bnumber is None:
            c = min([len(p_name), len(s_name), len(qtt), len(price), len(orantyy), len(orantysdate)])
            for i in range(c):

                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Inventory_Supplier_Entry.objects.get(id=s_name[i])
                if orantysdate[i] != None:
                    date = Product_PurchaseM(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                                             Price=price[i], User_Branch=branchs, userc=createuser,
                                             Invoice_no=invoice, Oranty_year=orantyy[i],
                                             Oranty_start_date=orantysdate[i])
                    date.save()
                else:
                    date = Product_PurchaseM(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                                             Price=price[i], User_Branch=branchs, userc=createuser,
                                             Invoice_no=invoice, Oranty_year=orantyy[i],
                                             Oranty_start_date='0001-01-01')
                    date.save()
                bill = Product_PurchaseM.objects.raw(
                    'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')
            messages.info(request, 'Data Save')
            return render(request, 'inventory/message.html',
                          {'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Product_PurchaseM.objects.raw(
                'select id,count( DISTINCT invoice_no) as invoice_no from project_product_purchasem ppp ')

            producets_pp = Product_PurchaseM.objects.raw(
                'select  DISTINCT id=0 as id,invoice_no from project_product_purchasem ppp where invoice_no=%s',
                [bnumber])
            data = Product_PurchaseM.objects.filter(Invoice_no=bnumber)
            # for x in data

            c = min([len(p_name), len(s_name), len(qtt), len(price), len(id), len(orantyy), len(orantysdate)])
            for i in range(c):

                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Inventory_Supplier_Entry.objects.get(id=s_name[i])
                # date = Product_PurchaseM.objects.filter(Invoice_no=a).update(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                #                          Price=price[i], User_Branch=branchs, userc=createuser, Invoice_no=bnumber)
                if orantysdate[i] != "":
                    data = Product_PurchaseM.objects.get(id=id[i])
                    data.Product_Name = pr_name
                    data.Product_Supplier_Name = su_name
                    data.Quantity = qtt[i]
                    data.Price = price[i]
                    data.userc = createuser
                    data.User_Branch = branchs
                    data.Invoice_no = bnumber
                    data.Oranty_year = orantyy[i]
                    data.Oranty_start_date = orantysdate[i]
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
            return render(request, 'inventory/message.html',
                          {'producets_pp': producets_pp, 'bill': bill, 'company': company,
                           'user_current_branch': user_current_branch, 'user_branch': user_branch})



def invontory_product_issue_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist = DesignationM.objects.all()
    depertmentlist = DepartmentM.objects.all()
    products = Inventory_Product_Entry.objects.all()
    employees = Hr_Employees_infoM.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        producets_pp = Product_issueM.objects.raw(
            'select  DISTINCT id=0 as id,invoice_no,Edits from project_Product_issueM ppp where invoice_no=%s and User_Branch_id=%s',
            [search, request.user.last_name])
        datasall = Product_issueM.objects.filter(Invoice_no=search, User_Branch=request.user.last_name)
        bill = Product_issueM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_Product_issueM ppp ')

        return render(request, 'inventory/forms/product_issue.html',
                      {'producets_pp': producets_pp, 'datasall': datasall, 'bill': bill, 'products': products,
                       'employees': employees,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'company': company})
    else:
        bill = Product_issueM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_product_issuem ppp ')
        return render(request, 'inventory/forms/product_issue.html',
                      {'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'bill': bill,
                       'company': company, 'products': products, 'employees': employees})



def invontory_product_issue_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)

    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        user = request.user.id
        branchs = Branch_Infoamtion.objects.get(id=request.user.last_name)
        createuser = User.objects.get(id=user)
        p_name = request.POST.getlist('p_name')
        s_name = request.POST.getlist('s_name')
        qtt = request.POST.getlist('qtt')

        id = request.POST.getlist('id')
        invoice = request.POST.get('invoice')

        if bnumber is None:
            c = min([len(p_name), len(s_name), len(qtt)])
            for i in range(c):

                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Hr_Employees_infoM.objects.get(id=s_name[i])
                if p_name[i] != None:
                    date = Product_issueM(Product_Name=pr_name, Product_Employees_Name=su_name, Quantity=qtt[i],
                                             User_Branch=branchs, userc=createuser,
                                             Invoice_no=invoice)
                    date.save()
                else:
                    date = Product_issueM(Product_Name=pr_name, Product_Employees_Name=su_name, Quantity=qtt[i],
                                              User_Branch=branchs, userc=createuser,
                                             Invoice_no=invoice
                                             )
                    date.save()
                bill = Product_issueM.objects.raw(
                    'select id,count( DISTINCT invoice_no) as invoice_no from project_Product_issueM ppp ')
            messages.info(request, 'Data Save')
            return render(request, 'inventory/message.html',
                          {'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Product_issueM.objects.raw(
                'select id,count( DISTINCT invoice_no) as invoice_no from project_Product_issueM ppp ')

            producets_pp = Product_issueM.objects.raw(
                'select  DISTINCT id=0 as id,invoice_no from project_Product_issueM ppp where invoice_no=%s',
                [bnumber])
            data = Product_issueM.objects.filter(Invoice_no=bnumber)
            # for x in data

            c = min([len(p_name), len(s_name), len(qtt), len(id)])
            for i in range(c):

                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Hr_Employees_infoM.objects.get(id=s_name[i])
                # date = Product_PurchaseM.objects.filter(Invoice_no=a).update(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                #                          Price=price[i], User_Branch=branchs, userc=createuser, Invoice_no=bnumber)
                if p_name[i] != "":
                    data = Product_issueM.objects.get(id=id[i])
                    data.Product_Name = pr_name
                    data.Product_Employees_Name = su_name
                    data.Quantity = qtt[i]

                    data.userc = createuser
                    data.User_Branch = branchs
                    data.Invoice_no = bnumber

                    data.save()
                else:
                    data = Product_issueM.objects.get(id=id[i])
                    data.Product_Name = pr_name
                    data.Product_Employees_Name = su_name
                    data.Quantity = qtt[i]

                    data.userc = createuser
                    data.User_Branch = branchs
                    data.Invoice_no = bnumber


                    data.save()
            messages.info(request, 'Data Update')
            return render(request, 'inventory/message.html',
                          {'producets_pp': producets_pp, 'bill': bill, 'company': company,
                           'user_current_branch': user_current_branch, 'user_branch': user_branch})

def invontory_product_issue_select_infoV(request):
    products = Inventory_Product_Entry.objects.all()
    employees = Hr_Employees_infoM.objects.all()

    return render(request, 'inventory/forms/product_issue_select.html',
                  {'products': products, 'employees': employees})


def issue_info_pdf_demoV(request, Invoice_no=0):
    invoice_number = Product_issueM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no, userc_id from project_Product_issueM ppp WHERE Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    purchase_invoice = Product_issueM.objects.raw(
        'select id=0 as id, Product_Name_id ,Product_Employees_Name_id ,Quantity from project_Product_issueM ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    totals = Product_issueM.objects.raw(
        'select id=0 as id, sum(Quantity) as ttotal from project_Product_issueM ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    for x in totals:
        amount = num2words(x.ttotal, lang="en_IN")
    template_path = 'inventory/reports/issue_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'purchase_invoice': purchase_invoice, 'invoice_number': invoice_number
               ,'totals':totals,'amount':amount}
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


def issue_info_pdfV(request, Invoice_no=0):
    invoice_number = Product_issueM.objects.raw(
        'select DISTINCT id=0 as id,Invoice_no, userc_id from project_Product_issueM ppp WHERE Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    purchase_invoice = Product_issueM.objects.raw(
        'select id=0 as id, Product_Name_id ,Product_Employees_Name_id ,Quantity from project_Product_issueM ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    totals = Product_issueM.objects.raw(
        'select id=0 as id, sum(Quantity) as ttotal from project_Product_issueM ppp where Invoice_no =%s and User_Branch_id=%s',
        [Invoice_no, request.user.last_name])
    for x in totals:
        amount = num2words(x.ttotal, lang="en_IN")
    template_path = 'inventory/reports/issue_info_pdf.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'purchase_invoice': purchase_invoice, 'invoice_number': invoice_number,
               'totals': totals, 'amount': amount}
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

    abc = Product_issueM.objects.filter(Edits=None, Invoice_no=Invoice_no)
    if abc:
        for x in abc:
            data = Product_issueM.objects.get(id=x.id)
            data.Edits = 1
            data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def issue_info_adjustmentV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    designationlist = DesignationM.objects.all()
    depertmentlist = DepartmentM.objects.all()
    products = Inventory_Product_Entry.objects.all()
    employees = Hr_Employees_infoM.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        producets_pp = Product_issueM.objects.raw(
            'select  DISTINCT id=0 as id,invoice_no,Edits from project_Product_issueM ppp where invoice_no=%s and User_Branch_id=%s',
            [search, request.user.last_name])
        datasall = Product_issueM.objects.filter(Invoice_no=search, User_Branch=request.user.last_name)
        bill = Product_issueM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_Product_issueM ppp ')

        return render(request, 'inventory/forms/product_issue_adjustment.html',
                      {'producets_pp': producets_pp, 'datasall': datasall, 'bill': bill, 'products': products,
                       'employees': employees,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'company': company})
    else:
        bill = Product_issueM.objects.raw(
            'select id,count( DISTINCT invoice_no) as invoice_no from project_product_issuem ppp ')
        return render(request, 'inventory/forms/product_issue_adjustment.html',
                      {'user_current_branch': user_current_branch, 'user_branch': user_branch,
                       'designationlist': designationlist, 'depertmentlist': depertmentlist, 'bill': bill,
                       'company': company, 'products': products, 'employees': employees})



def issue_info_adjustment_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)

    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        user = request.user.id
        branchs = Branch_Infoamtion.objects.get(id=request.user.last_name)
        createuser = User.objects.get(id=user)
        p_name = request.POST.getlist('p_name')
        s_name = request.POST.getlist('s_name')
        qtt = request.POST.getlist('qtt')

        id = request.POST.getlist('id')
        invoice = request.POST.get('invoice')

        if bnumber is None:
            c = min([len(p_name), len(s_name), len(qtt)])
            for i in range(c):

                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Hr_Employees_infoM.objects.get(id=s_name[i])
                if p_name[i] != None:
                    date = Product_issueM(Product_Name=pr_name, Product_Employees_Name=su_name, Quantity=qtt[i],
                                          User_Branch=branchs, userc=createuser,
                                          Invoice_no=invoice,Edits=1)
                    date.save()
                else:
                    date = Product_issueM(Product_Name=pr_name, Product_Employees_Name=su_name, Quantity=qtt[i],
                                          User_Branch=branchs, userc=createuser,
                                          Invoice_no=invoice
                                          )
                    date.save()
                bill = Product_issueM.objects.raw(
                    'select id,count( DISTINCT invoice_no) as invoice_no from project_Product_issueM ppp ')
            messages.info(request, 'Data Save')
            return render(request, 'inventory/message.html',
                          {'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = Product_issueM.objects.raw(
                'select id,count( DISTINCT invoice_no) as invoice_no from project_Product_issueM ppp ')

            producets_pp = Product_issueM.objects.raw(
                'select  DISTINCT id=0 as id,invoice_no from project_Product_issueM ppp where invoice_no=%s',
                [bnumber])
            data = Product_issueM.objects.filter(Invoice_no=bnumber)
            # for x in data

            c = min([len(p_name), len(s_name), len(qtt), len(id)])
            for i in range(c):

                pr_name = Inventory_Product_Entry.objects.get(id=p_name[i])
                su_name = Hr_Employees_infoM.objects.get(id=s_name[i])
                # date = Product_PurchaseM.objects.filter(Invoice_no=a).update(Product_Name=pr_name, Product_Supplier_Name=su_name, Quantity=qtt[i],
                #                          Price=price[i], User_Branch=branchs, userc=createuser, Invoice_no=bnumber)
                if p_name[i] != "":
                    data = Product_issueM.objects.get(id=id[i])
                    data.Product_Name = pr_name
                    data.Product_Employees_Name = su_name
                    data.Quantity = qtt[i]

                    data.userc = createuser
                    data.User_Branch = branchs
                    data.Invoice_no = bnumber

                    data.save()
                else:
                    data = Product_issueM.objects.get(id=id[i])
                    data.Product_Name = pr_name
                    data.Product_Employees_Name = su_name
                    data.Quantity = qtt[i]

                    data.userc = createuser
                    data.User_Branch = branchs
                    data.Invoice_no = bnumber

                    data.save()
            messages.info(request, 'Data Update')
            return render(request, 'inventory/message.html',
                          {'producets_pp': producets_pp, 'bill': bill, 'company': company,
                           'user_current_branch': user_current_branch, 'user_branch': user_branch})

def software_voyage_form_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = VoyageForm.objects.filter(id=search)
        datasall = VoyageForm.objects.filter(id=search)
        bill = VoyageForm.objects.all().count()
        return render(request, 'software_admin/forms/voyage_form.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = VoyageForm.objects.all().count()
    return render(request,'software_admin/forms/voyage_form.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch,'bill':bill})

def software_voyage_form_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = VoyageForm.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('vname')

        if bnumber is None:
            date = VoyageForm(id=id, Name=dname, create_user=createuser)
            date.save()
            datas = VoyageForm.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = VoyageForm.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = VoyageForm.objects.all().count()
            datas = VoyageForm.objects.filter(id=bnumber)
            data = VoyageForm.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})


def software_voyage_form_info_demo_pdfV(request, id=0):
    voyage_info = VoyageForm.objects.filter(id=id)
    template_path = 'software_admin/reports/voyageform_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'voyage_info': voyage_info}
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

def software_voyage_form_info_pdfV(request, id=0):
    vaoyage_info = VoyageForm.objects.filter(id=id)
    template_path = 'software_admin/reports/voyageform_info_pdf.html'
    context = {'company': company, 'vaoyage_info': vaoyage_info}
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
    data = VoyageForm.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def software_voyage_to_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = VoyageTo.objects.filter(id=search)
        datasall = VoyageTo.objects.filter(id=search)
        bill = VoyageTo.objects.all().count()
        return render(request, 'software_admin/forms/voyage_to.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = VoyageTo.objects.all().count()
    return render(request,'software_admin/forms/voyage_to.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch,'bill':bill})

def software_voyage_to_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = VoyageTo.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('vname')

        if bnumber is None:
            date = VoyageTo(id=id, Name=dname, create_user=createuser)
            date.save()
            datas = VoyageTo.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = VoyageTo.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = VoyageTo.objects.all().count()
            datas = VoyageTo.objects.filter(id=bnumber)
            data = VoyageTo.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})

def software_voyage_to_info_demo_pdfV(request, id=0):
    voyage_info = VoyageTo.objects.filter(id=id)
    template_path = 'software_admin/reports/voyageto_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'voyage_info': voyage_info}
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

def software_voyage_to_info_pdfV(request, id=0):
    vaoyage_info = VoyageTo.objects.filter(id=id)
    template_path = 'software_admin/reports/voyageto_info_pdf.html'
    context = {'company': company, 'vaoyage_info': vaoyage_info}
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
    data = VoyageTo.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def software_voyage_via_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = VoyageVia.objects.filter(id=search)
        datasall = VoyageVia.objects.filter(id=search)
        bill = VoyageVia.objects.all().count()
        return render(request, 'software_admin/forms/voyage_via.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = VoyageVia.objects.all().count()
    return render(request,'software_admin/forms/voyage_via.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch,'bill':bill})

def software_voyage_via_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = VoyageVia.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('vname')

        if bnumber is None:
            date = VoyageVia(id=id, Name=dname, create_user=createuser)
            date.save()
            datas = VoyageVia.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = VoyageVia.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = VoyageVia.objects.all().count()
            datas = VoyageVia.objects.filter(id=bnumber)
            data = VoyageVia.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})

def software_voyage_via_info_demo_pdfV(request, id=0):
    voyage_info = VoyageVia.objects.filter(id=id)
    template_path = 'software_admin/reports/voyagevia_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'voyage_info': voyage_info}
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

def software_voyage_via_info_pdfV(request, id=0):
    vaoyage_info = VoyageVia.objects.filter(id=id)
    template_path = 'software_admin/reports/voyagevia_info_pdf.html'
    context = {'company': company, 'vaoyage_info': vaoyage_info}
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
    data = VoyageVia.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def software_transit_by_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = TransitBy.objects.filter(id=search)
        datasall = TransitBy.objects.filter(id=search)
        bill = TransitBy.objects.all().count()
        return render(request, 'software_admin/forms/transit_by.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = TransitBy.objects.all().count()
    return render(request,'software_admin/forms/transit_by.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch,'bill':bill})

def software_transit_by_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = TransitBy.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('vname')
        stump = request.POST.get('stump')

        if bnumber is None:
            date = TransitBy(id=id, Name=dname,Stump_Rate=stump, create_user=createuser)
            date.save()
            datas = TransitBy.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = TransitBy.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = TransitBy.objects.all().count()
            datas = TransitBy.objects.filter(id=bnumber)
            data = TransitBy.objects.get(id=bnumber)
            data.Name = dname
            data.Stump_Rate = stump
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})

def software_transit_by_info_demo_pdfV(request, id=0):
    voyage_info = TransitBy.objects.filter(id=id)
    template_path = 'software_admin/reports/transitby_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'voyage_info': voyage_info}
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
#
def software_transit_by_info_pdfV(request, id=0):
    vaoyage_info = TransitBy.objects.filter(id=id)
    template_path = 'software_admin/reports/transitby_info_pdf.html'
    context = {'company': company, 'vaoyage_info': vaoyage_info}
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
    data = TransitBy.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def software_risk_cover_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = RiskCovered.objects.filter(id=search)
        datasall = RiskCovered.objects.filter(id=search)
        bill = RiskCovered.objects.all().count()
        return render(request, 'software_admin/forms/RiskCover.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = RiskCovered.objects.all().count()
    return render(request,'software_admin/forms/RiskCover.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch,'bill':bill})

def software_risk_cover_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = RiskCovered.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('vname')

        if bnumber is None:
            date = RiskCovered(id=id, Name=dname, create_user=createuser)
            date.save()
            datas = RiskCovered.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = RiskCovered.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = RiskCovered.objects.all().count()
            datas = RiskCovered.objects.filter(id=bnumber)
            data = RiskCovered.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
#
def software_risk_cover_info_demo_pdfV(request, id=0):
    voyage_info = RiskCovered.objects.filter(id=id)
    template_path = 'software_admin/reports/riskcover_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'voyage_info': voyage_info}
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
# #
def software_risk_cover_info_pdfV(request, id=0):
    vaoyage_info = RiskCovered.objects.filter(id=id)
    template_path = 'software_admin/reports/riskcover_info_pdf.html'
    context = {'company': company, 'vaoyage_info': vaoyage_info}
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
    data = RiskCovered.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def software_insurance_type_infoV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        datas = InsuraceType.objects.filter(id=search)
        datasall = InsuraceType.objects.filter(id=search)
        bill = InsuraceType.objects.all().count()
        return render(request, 'software_admin/forms/insurancetype.html',
                      {'datas': datas, 'datasall': datasall, 'bill': bill, 'company': company,
                       'user_current_branch': user_current_branch, 'user_branch': user_branch})
    else:
        bill = InsuraceType.objects.all().count()
    return render(request,'software_admin/forms/insurancetype.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch,'bill':bill})

def software_insurance_type_info_saveV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    if request.method == 'POST':
        bnumber = request.POST.get('Bnumber')
        counter = InsuraceType.objects.all().count()
        id = counter + 1
        user = request.user.id
        createuser = User.objects.get(id=user)
        dname = request.POST.get('vname')

        if bnumber is None:
            date = InsuraceType(id=id, Name=dname, create_user=createuser)
            date.save()
            datas = InsuraceType.objects.filter(id=id)
            messages.info(request, 'Data Save')
            bill = InsuraceType.objects.all().count()
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
        else:
            bill = InsuraceType.objects.all().count()
            datas = InsuraceType.objects.filter(id=bnumber)
            data = InsuraceType.objects.get(id=bnumber)
            data.Name = dname
            data.create_user = createuser
            data.save()
            messages.info(request, 'Data Update')
            return render(request, 'software_admin/forms/message.html',
                          {'datas': datas, 'bill': bill, 'company': company, 'user_current_branch': user_current_branch,
                           'user_branch': user_branch})
# #
def software_insurance_type_info_demo_pdfV(request, id=0):
    voyage_info = InsuraceType.objects.filter(id=id)
    template_path = 'software_admin/reports/insurancetype_info_pdf_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'voyage_info': voyage_info}
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
# # #
def software_insurance_type_info_pdfV(request, id=0):
    vaoyage_info = InsuraceType.objects.filter(id=id)
    template_path = 'software_admin/reports/insurancetype_info_pdf.html'
    context = {'company': company, 'vaoyage_info': vaoyage_info}
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
    data = InsuraceType.objects.get(id=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def uw_dashboardV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request,'uw/uw_dashboard.html',{'company':company,'user_branch':user_branch,'user_current_branch':user_current_branch})


def uw_q_marineV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    bill = MarineQuatationM.objects.all().count()
    client_n=ClinetM.objects.all()
    bank_n=BankM.objects.all()
    client_add = Client_BranchM.objects.all()
    voyagefrom=VoyageForm.objects.all()
    voyageto=VoyageTo.objects.all()
    transitby=TransitBy.objects.all()
    voyagevia=VoyageVia.objects.all()
    currenct=Currency.objects.all()
    risk=RiskCovered.objects.all()
    insurance=InsuraceType.objects.all()
    producer=Hr_Employees_infoM.objects.all()
    bankbranch=Bank_BranchM.objects.all()

    return render(request,'uw/forms/quotation/marineq.html',{'company':company,'user_branch':user_branch,
                                                             'user_current_branch':user_current_branch,
                                                             'client_n':client_n,'client_add':client_add,
                                                             'bank_n':bank_n,'voyagefrom':voyagefrom,
                                                             'voyageto':voyageto,'transitby':transitby,
                                                             'voyagevia':voyagevia,'currenct':currenct,
                                                             'risk':risk,'insurance':insurance,
                                                             'producer':producer,'bankbranch':bankbranch,'bill':bill})




def uw_q_marine_client_selectV(request):
    cname=request.GET.get('client_n')
    print(cname)
    client_adds=Client_BranchM.objects.filter(Client_Name=cname)
    abc=client_adds.values()
    good=list(abc)
    return JsonResponse({'client':good}, status=200)




def uw_q_marine_bank_branch_selectV(request):
    bank=request.GET.get('bank_n')
    bank_adds=Bank_BranchM.objects.filter(Bank_Name=bank)
    abc=bank_adds.values()

    good=list(abc)
    return JsonResponse({'bank':good}, status=200)

def uw_q_marine_deposit_bank_branch_selectV(request):
    dbank=request.GET.get('dbank_n')
    bank_adds=Deposit_Bank_BranchM.objects.filter(Bank_Name=dbank)
    abc=bank_adds.values()
    good=list(abc)
    return JsonResponse({'bank':good}, status=200)

def uw_q_marine_transit_by_selectV(request):
    trys=request.GET.get('transits')
    bd=int(request.GET.get('bdamountds'))
    warenet=int(request.GET.get('warenet'))
    marinenet=int(request.GET.get('marinenet'))
    vateas=int(request.GET.get('vateas'))
    transit=TransitBy.objects.filter(id=trys)
    for x in transit:
        if x.Stump_Rate == 50:
            sdam = x.Stump_Rate
            sumg=warenet+marinenet+vateas+sdam
            # abc = sdam.values()
            # print(abc)
            # good = list(sdam)
            return JsonResponse({'trans': sdam,'sumg':sumg}, status=200)
        else:
            sdam = round(bd/1500)
            sumg = warenet + marinenet + vateas + sdam
            # abc = sdam.values()
            # good = list(abc)
            return JsonResponse({'trans': sdam,'sumg':sumg}, status=200)
    abc = transit.values()
    good = list(abc)
    return JsonResponse({'trans': good},status=200)

def qmarinedateV(request):
    fdates = request.GET.get('fdares')
    datess=datetime.datetime.strptime(fdates,'%d-%m-%Y')
    datas = (datess + datetime.timedelta(days=364)).date()
    return JsonResponse({"trans":datas},status=200)


def uw_q_marine_bank_selectV(request):
    cname=request.GET.get('bank_n')
    bank_adds=Bank_BranchM.objects.filter(Client_Name=cname)
    return render(request,'uw/forms/quotation/clientaddress.html',{'bank_adds':bank_adds})


def uw_q_marine_saveV(request):
    if request.method == 'POST':
        bnumber = request.POST.get('billnos')
        print(bnumber)
        counter = MarineQuatationM.objects.all().count()
        user = request.user.id
        createuser = User.objects.get(id=user)

        billdate = request.POST.get('billdates')
        billdates=datetime.datetime.strptime(billdate,'%d-%m-%Y')
        ac = request.POST.get('acs')
        client_n = request.POST.get('client_ns')
        client=ClinetM.objects.get(id=client_n)
        client_addres = request.POST.get('client_address')
        c_address=Client_BranchM.objects.get(id=client_addres)
        bank_names = request.POST.get('bank_namess')
        bank=BankM.objects.get(id=bank_names)
        bank_address = request.POST.get('bank_addressss')
        b_branch=Bank_BranchM.objects.get(id=bank_address)
        transit = request.POST.get('transits')
        tarnsit_by=TransitBy.objects.get(id=transit)
        vforms = request.POST.get('vformss')
        voyagef=VoyageForm.objects.get(id=vforms)
        vTos = request.POST.get('vToss')
        voyaget=VoyageTo.objects.get(id=vTos)
        interestcover = request.POST.get('interestcovers')
        vvias = request.POST.get('vviass')
        voyagevis=VoyageVia.objects.get(id=vvias)
        fdate = request.POST.get('fdates')
        from_date=datetime.datetime.strptime(fdate,'%d-%m-%Y')
        tdate = request.POST.get('tdates')
        to_date = datetime.datetime.strptime(tdate, '%d-%m-%Y')
        sinsured = request.POST.get('sinsureds')
        extra1 = request.POST.get('extra1s')
        extra2 = request.POST.get('extra2s')
        currency = request.POST.get('currents')
        rate = request.POST.get('rates')
        bdamounts = request.POST.get('bdamounts')
        declaration = request.POST.get('decss')
        riskcoder = request.POST.get('riskcoderss')
        risk=RiskCovered.objects.get(id=riskcoder)
        insurances = request.POST.get('insurancess')
        insurance_type=InsuraceType.objects.get(id=insurances)
        producers = request.POST.get('producerss')
        producer=Hr_Employees_infoM.objects.get(id=producers)
        dis = request.POST.get('diss')
        spdis = request.POST.get('spdiss')
        mrate = request.POST.get('mrates')
        mamount = request.POST.get('mamounts')
        wrates = request.POST.get('wratess')
        wamount = request.POST.get('wamounts')
        netid = request.POST.get('netids')
        vataid = request.POST.get('vataids')
        samount = request.POST.get('samounts')
        gross = request.POST.get('grosss')
        nara = request.POST.get('naras')
        tomail = request.POST.get('tomail')
        branchs = Branch_Infoamtion.objects.get(id=request.user.last_name)
        id = counter + 1
        if bnumber == '':

            date = MarineQuatationM(id=id, Bill_date=billdates,Bill_No=id,Ac=ac,Insurance_Type=insurance_type,Client_NameM=client,
                                    Client_AddressM=c_address,Bank_Name=bank,Bank_Branch=b_branch,Interest_covered=interestcover,
                                    Voyage_From=voyagef,Voyage_To=voyaget,Voyage_Via=voyagevis,Transit_By=tarnsit_by,
                                    Sdate=from_date,Edate=to_date,Sum_insured=sinsured,Extra1=extra1,Extra2=extra2,
                                    Currency=currency,Excrate=rate,Bdtamount=bdamounts,Declaration=declaration,
                                    Discount=dis,SpDiscount=spdis,Marine_Rate=mrate,Marine_Amount=mamount,
                                    Ware_Rate=wrates,Ware_Amount=wamount,Net_Amount=netid,Vat_Amount=vataid,
                                    Stump_Amount=samount,Gross_Amount=gross,Producer=producer,RiskCover=risk,
                                    narration=nara,userc=createuser,User_Branch=branchs,sendmail=tomail)
            date.save()
            # datas = MarineQuatationM.objects.filter(id=id)
            #
            # # bill = MarineQuatationM.objects.all().count()
            # abc = datas.values()
            # good = list(abc)
            # good = messages.info(request, 'Data Save')
            all = MarineQuatationM.objects.filter(Bill_No=id)
            good = serializers.serialize('json', all)
            abcs = json.loads(good)
            abc = 'Data Save'
            return JsonResponse({'id':id,'messages':abc,'abcs':abcs},status=200)
        else:
            id=bnumber
            bill = MarineQuatationM.objects.all().count()
            datas = MarineQuatationM.objects.filter(id=bnumber)
            data = MarineQuatationM.objects.get(id=bnumber)
            data.Bill_date=billdates
            data.Ac=ac
            data.Insurance_Type=insurance_type
            data.Client_NameM=client
            data.Client_AddressM=c_address
            data.Bank_Name=bank
            data.Bank_Branch=b_branch
            data.Interest_covered=interestcover
            data.Voyage_From=voyagef
            data.Voyage_To=voyaget
            data.Voyage_Via=voyagevis
            data.Transit_By=tarnsit_by
            data.Sdate=from_date
            data.Edate=to_date
            data.Sum_insured=sinsured
            data.Extra1=extra1
            data.Extra2=extra2
            data.Currency=currency
            data.Excrate=rate
            data.Bdtamount=bdamounts
            data.Declaration=declaration
            data.Discount=dis
            data.SpDiscount=spdis
            data.Marine_Rate=mrate
            data.Marine_Amount=mamount
            data.Ware_Rate=wrates
            data.Ware_Amount=wamount
            data.Net_Amount=netid
            data.Vat_Amount=vataid
            data.Stump_Amount=samount
            data.Gross_Amount=gross
            data.Producer=producer
            data.RiskCover=risk
            data.narration=nara
            data.userc=createuser
            data.sendmail=tomail
            data.save()
            all = MarineQuatationM.objects.filter(Bill_No=id)
            good = serializers.serialize('json', all)
            abcs = json.loads(good)
            abc = 'Data Update'
            return JsonResponse({'id':id,'messages':abc,'abcs':abcs},status=200,safe=False)


def uw_q_marine_searchV(request):
    search_b=request.POST.get('search')
    # all=MarineQuatationM.objects.raw('select mar.id as id ,mar.Bill_date as Bill_date  ,mar.Bill_No as Bill_No, mar.Ac as Ac ,bb.Bank_Branch ||" "|| bb.Bank_Branch_Address as Bank_Branch_id ,ban.Name as Bank_Name_id, mar.Bdtamount as Bdtamount ,clb.Client_Branch ||" "|| clb.Client_Branch_Address as Client_AddressM_id,cl.Name as Client_NameM_id ,mar.Declaration as  Declaration,mar.Discount as Discount ,mar.Edate as Edate ,mar.Edits as Edits,mar.Excrate as Excrate  ,mar.Extra1 as Extra1 ,mar.Extra2 as Extra2,mar.Gross_Amount as Gross_Amount,insu.Name as insurancetype ,mar.Interest_covered as Interest_covered ,mar.Marine_Amount as Marine_Amount ,mar.Marine_Rate as Marine_Rate ,mar.Net_Amount as Net_Amount ,hr.Employees_Name as producer ,res.Name as riskcover ,mar.Sdate as Sdate ,mar.SpDiscount as SpDiscount ,mar.Stump_Amount as Stump_Amount,mar.Sum_insured as Sum_insured,trn.Name as transit_by ,mar.Vat_Amount as Vat_Amount ,vf.Name as voyage_form ,vt.Name as voyage_to,vv.Name as voyage_via,mar.Ware_Amount as Ware_Amount,mar.Ware_Rate as Ware_Rate ,mar.issu_date as issu_date ,mar.narration as narration ,mar.Currency as Currency from project_marinequatationm mar join project_bankm ban on mar.Bank_Name_id =ban.id join project_bank_branchm bb on mar.Bank_Branch_id =bb.id join project_clinetm cl on mar.Client_NameM_id =cl.id join project_client_branchm clb on mar.Client_AddressM_id =clb.id join project_insuracetype insu on mar.Insurance_Type_id =insu.id join project_hr_employees_infom hr on mar.Producer_id =hr.id join project_riskcovered res on mar.RiskCover_id =res.id join project_transitby trn on mar.Transit_By_id =trn.id join project_voyageform vf on mar.Voyage_From_id =vf.id join project_voyageto vt on mar.Voyage_To_id =vt.id join project_voyagevia vv on mar.Voyage_Via_id =vv.id where mar.Bill_No =%s',[14])
    all=MarineQuatationM.objects.filter(Bill_No=search_b)

    good=serializers.serialize('json',all)
    abc=json.loads(good)
    return JsonResponse({'all':abc},safe=False)

def uw_q_marine_cover_searchV(request):
    search_b=request.POST.get('search')
    alls=MarineCovernoteM.objects.filter(Cover_No_no=search_b)
    for x in alls:
        all = MRTable.objects.filter(id=x.MR_Number_id)
        goods = serializers.serialize('json', all)
        abcs = json.loads(goods)
        good=serializers.serialize('json',alls)
        abc=json.loads(good)
    return JsonResponse({'all':abc,'mrcl':abcs},safe=False)


def uw_q_marine_demo_pdfsV(request,id=0):
    marine_bill = MarineQuatationM.objects.filter(Bill_No=id)
    for x in marine_bill:
        amount = num2words(x.Gross_Amount, lang="en_IN")
    template_path = 'uw/reports/marine_bill_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'marine_bill': marine_bill,'amount':amount}
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

def uw_q_marine_pdfsV(request,id=0):
    marine_bill = MarineQuatationM.objects.filter(Bill_No=id)
    for x in marine_bill:
        amount = num2words(x.Gross_Amount, lang="en_IN")
    template_path = 'uw/reports/marine_bill.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'marine_bill': marine_bill,'amount':amount}
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
    data = MarineQuatationM.objects.get(Bill_No=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def uw_q_marine_sendV(request,id=0):
    if id !=0:
        marine_bill = MarineQuatationM.objects.filter(Bill_No=id)
        for x in marine_bill:
            amount = num2words(x.Gross_Amount, lang="en_IN")
            to= x.sendmail
            my_list = to.split(",")
        html_contant=render_to_string('uw/reports/marine_bill_email.html',{'company':company,'marine_bill':marine_bill,'amount':amount})
        text_contant=strip_tags(html_contant)
        email=EmailMultiAlternatives(
            #subject
            'test',
            text_contant,
            settings.EMAIL_HOST_USER,
            my_list,

        )
        email.attach_alternative(html_contant,'text/html')
        email.send()
        return HttpResponse('Send your Email')
    else:
        return HttpResponse('Error your Email')


def uw_q_marine_covernoteV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    bill = MarineCovernoteM.objects.all().count()
    client_n = ClinetM.objects.all()
    bank_n = BankM.objects.all()
    client_add = Client_BranchM.objects.all()
    voyagefrom = VoyageForm.objects.all()
    voyageto = VoyageTo.objects.all()
    transitby = TransitBy.objects.all()
    voyagevia = VoyageVia.objects.all()
    currenct = Currency.objects.all()
    risk = RiskCovered.objects.all()
    insurance = InsuraceType.objects.all()
    producer = Hr_Employees_infoM.objects.all()
    bankbranch = Bank_BranchM.objects.all()
    modof=ModOfPayment.objects.all()
    depositbank_n = Deposit_BankM.objects.all()
    depositbank_branch_n = Deposit_Bank_BranchM.objects.all()
    return render(request, 'uw/forms/covernot/marinecovernote.html', {'company': company, 'user_branch': user_branch,
                                                               'user_current_branch': user_current_branch,
                                                               'client_n': client_n, 'client_add': client_add,
                                                               'bank_n': bank_n, 'voyagefrom': voyagefrom,
                                                               'voyageto': voyageto, 'transitby': transitby,
                                                               'voyagevia': voyagevia, 'currenct': currenct,
                                                               'risk': risk, 'insurance': insurance,
                                                               'producer': producer, 'bankbranch': bankbranch,
                                                               'bill': bill,'modof':modof,'depositbank_n':depositbank_n,
                                                                      'depositbank_branch_n':depositbank_branch_n})


def uw_q_marine_covernote_saveV(request):
    if request.method == 'POST':
        bnumber = request.POST.get('billnos')
        counter = MarineCovernoteM.objects.all().count()
        id = counter + 1
        cover = request.POST.get('coverno')
        short=Company_Information.objects.all()
        branchs = Branch_Infoamtion.objects.get(id=request.user.last_name)
        dates=datetime.date.today()
        moth_date=dates.month
        year_date=dates.year
        for x in short:
            short=x.Company_Short_Name
            coberno = short + "/" + branchs.Branch_Short_Name + "/" + "MC" + "-" +str(id)+"/"+str(moth_date)+"/"+str(year_date)

        user = request.user.id
        createuser = User.objects.get(id=user)

        billdate = request.POST.get('billdates')
        billdates=datetime.datetime.strptime(billdate,'%d-%m-%Y')
        ac = request.POST.get('acs')
        client_n = request.POST.get('client_ns')
        client=ClinetM.objects.get(id=client_n)
        client_addres = request.POST.get('client_address')
        c_address=Client_BranchM.objects.get(id=client_addres)
        bank_names = request.POST.get('bank_namess')
        bank=BankM.objects.get(id=bank_names)
        bank_address = request.POST.get('bank_addressss')
        b_branch=Bank_BranchM.objects.get(id=bank_address)
        transit = request.POST.get('transits')
        tarnsit_by=TransitBy.objects.get(id=transit)
        vforms = request.POST.get('vformss')
        voyagef=VoyageForm.objects.get(id=vforms)
        vTos = request.POST.get('vToss')
        voyaget=VoyageTo.objects.get(id=vTos)
        interestcover = request.POST.get('interestcovers')
        vvias = request.POST.get('vviass')
        voyagevis=VoyageVia.objects.get(id=vvias)
        fdate = request.POST.get('fdates')
        from_date=datetime.datetime.strptime(fdate,'%d-%m-%Y')
        tdate = request.POST.get('tdates')
        to_date = datetime.datetime.strptime(tdate, '%d-%m-%Y')
        sinsured = request.POST.get('sinsureds')
        extra1 = request.POST.get('extra1s')
        extra2 = request.POST.get('extra2s')
        currency = request.POST.get('currents')
        rate = request.POST.get('rates')
        bdamounts = request.POST.get('bdamounts')
        declaration = request.POST.get('decss')
        riskcoder = request.POST.get('riskcoderss')
        risk=RiskCovered.objects.get(id=riskcoder)
        insurances = request.POST.get('insurancess')
        insurance_type=InsuraceType.objects.get(id=insurances)
        producers = request.POST.get('producerss')
        producer=Hr_Employees_infoM.objects.get(id=producers)
        dis = request.POST.get('diss')
        spdis = request.POST.get('spdiss')
        mrate = request.POST.get('mrates')
        mamount = request.POST.get('mamounts')
        wrates = request.POST.get('wratess')
        wamount = request.POST.get('wamounts')
        netid = request.POST.get('netids')
        vataid = request.POST.get('vataids')
        samount = request.POST.get('samounts')
        gross = request.POST.get('grosss')
        nara = request.POST.get('naras')
        tomail = request.POST.get('tomail')
        prints = request.POST.get('Print')
        Mr = request.POST.get('Mr')
        Mrdate = request.POST.get('Mrdate')

        mrd=datetime.datetime.strptime(Mrdate,'%d-%m-%Y')
        cdate = request.POST.get('cdate')
        if cdate =='':
            caquedate= None
        else:
            caquedate=datetime.datetime.strptime(cdate,'%d-%m-%Y')

        Numbers = request.POST.get('Numbers')
        Mop = request.POST.get('Mop')
        Dbnames = request.POST.get('Dbname')
        Dbbranchs = request.POST.get('Dbbranch')
        mrcount=MRTable.objects.all().count()
        mrnum= mrcount + 1
        coinsur=request.POST.get('coin')
        nonlider=request.POST.get('Nonleader')
        leaderpersent=request.POST.get('leaderpersents')
        leadercom=request.POST.get('leadercom')
        ldocu=request.POST.get('ldocu')



        if cover == '':
            if Dbnames =='':
                mrdatass = MRTable(id=mrnum, Mrno=mrnum, Mrno_date=mrd, Mod=Mop, Cheque_no=Numbers,Net_Amount=netid,Vat_Amount=vataid,
                                    Stump_Amount=samount,Gross_Amount=gross,class_insurance='Marine Cargo',User_Branch=branchs,Cdate=caquedate )
                mrdatass.save()
            elif Dbbranchs == '' :
                deposit_b = Deposit_BankM.objects.get(id=Dbnames)
                mrdatass = MRTable(id=mrnum, Mrno=mrnum, Mrno_date=mrd, Mod=Mop, Cheque_no=Numbers,Bank_name=deposit_b,Net_Amount=netid,Vat_Amount=vataid,
                                    Stump_Amount=samount,Gross_Amount=gross,class_insurance='Marine Cargo',User_Branch=branchs,Cdate=caquedate)
                mrdatass.save()
            else:
                deposit_b = Deposit_BankM.objects.get(id=Dbnames)
                deposit_bankadd = Deposit_Bank_BranchM.objects.get(id=Dbbranchs)
                mrdatass=MRTable(id=mrnum,Mrno=mrnum,Mrno_date=mrd,Mod=Mop,Cheque_no=Numbers,Bank_name=deposit_b,Bank_address=deposit_bankadd,Net_Amount=netid,Vat_Amount=vataid,
                                    Stump_Amount=samount,Gross_Amount=gross,class_insurance='Marine Cargo',User_Branch=branchs,Cdate=caquedate)
                mrdatass.save()
            mrnusss=MRTable.objects.get(id=mrnum)
            date = MarineCovernoteM(id=id, Cover_Date=billdates,Bill_No=bnumber,Cover_No=coberno,Ac=ac,Insurance_Type=insurance_type,Client_NameM=client,
                                    Client_AddressM=c_address,Bank_Name=bank,Bank_Branch=b_branch,Interest_covered=interestcover,
                                    Voyage_From=voyagef,Voyage_To=voyaget,Voyage_Via=voyagevis,Transit_By=tarnsit_by,
                                    Sdate=from_date,Edate=to_date,Sum_insured=sinsured,Extra1=extra1,Extra2=extra2,
                                    Currency=currency,Excrate=rate,Bdtamount=bdamounts,Declaration=declaration,
                                    Discount=dis,SpDiscount=spdis,Marine_Rate=mrate,Marine_Amount=mamount,
                                    Ware_Rate=wrates,Ware_Amount=wamount,Net_Amount=netid,Vat_Amount=vataid,
                                    Stump_Amount=samount,Gross_Amount=gross,Producer=producer,RiskCover=risk,
                                    narration=nara,userc=createuser,User_Branch=branchs,sendmail=tomail,Cover_No_no=id, Printed_No=prints,MR_Number=mrnusss,
                                    Coins_Leader=coinsur, Coins_None_Leader=nonlider, Coins_Leader_Persent=leaderpersent, Coins_Leader_Doc=ldocu, Coins_Leader_Name=leadercom)
            date.save()
            # datas = MarineQuatationM.objects.filter(id=id)
            #
            # # bill = MarineQuatationM.objects.all().count()
            # abc = datas.values()
            # good = list(abc)
            # good = messages.info(request, 'Data Save')
            all = MarineCovernoteM.objects.raw('select * from project_marinecovernotem mc, project_mrtable pm where mc.MR_Number_id = pm.id and mc.Cover_No_no = %s',[id])
            good = serializers.serialize('json', all)
            abcs = json.loads(good)
            abc = 'Data Save'
            return JsonResponse({'id':id,'messages':abc,'abcs':abcs},status=200)
        else:
            mrnusss = MRTable.objects.get(id=Mr)
            if Dbnames == '':
                mrnusss.Mod=Mop
                mrnusss.Cheque_no=Numbers
                mrnusss.Net_Amount = netid
                mrnusss.Vat_Amount = vataid
                mrnusss.Stump_Amount = samount
                mrnusss.Gross_Amount = gross
                mrnusss.class_insurance='Marine Cargo'
                mrnusss.User_Branch=branchs
                mrnusss.Cdate=caquedate
                mrnusss.save()
            elif Dbbranchs == '':
                deposit_b = Deposit_BankM.objects.get(id=Dbnames)
                mrnusss.Bank_name=deposit_b
                mrnusss.Mod = Mop
                mrnusss.Cheque_no = Numbers
                mrnusss.Net_Amount = netid
                mrnusss.Vat_Amount = vataid
                mrnusss.Stump_Amount = samount
                mrnusss.Gross_Amount = gross
                mrnusss.class_insurance='Marine Cargo'
                mrnusss.User_Branch=branchs
                mrnusss.Cdate=caquedate
                mrnusss.save()
            else:
                deposit_b = Deposit_BankM.objects.get(id=Dbnames)
                deposit_bankadd = Deposit_Bank_BranchM.objects.get(id=Dbbranchs)
                mrnusss.Bank_name = deposit_b
                mrnusss.Bank_address=deposit_bankadd
                mrnusss.Mod = Mop
                mrnusss.Cheque_no = Numbers
                mrnusss.Net_Amount = netid
                mrnusss.Vat_Amount = vataid
                mrnusss.Stump_Amount = samount
                mrnusss.Gross_Amount = gross
                mrnusss.class_insurance='Marine Cargo'
                mrnusss.User_Branch=branchs
                mrnusss.Cdate=caquedate
                mrnusss.save()

            id=cover
            bill = MarineCovernoteM.objects.all().count()
            datas = MarineCovernoteM.objects.filter(Cover_No=cover)
            data = MarineCovernoteM.objects.get(Cover_No=cover)
            # data.Bill_date=billdates
            data.Ac=ac
            data.Insurance_Type=insurance_type
            data.Client_NameM=client
            data.Client_AddressM=c_address
            data.Bank_Name=bank
            data.Bank_Branch=b_branch
            data.Interest_covered=interestcover
            data.Voyage_From=voyagef
            data.Voyage_To=voyaget
            data.Voyage_Via=voyagevis
            data.Transit_By=tarnsit_by
            data.Sdate=from_date
            data.Edate=to_date
            data.Sum_insured=sinsured
            data.Extra1=extra1
            data.Extra2=extra2
            data.Currency=currency
            data.Excrate=rate
            data.Bdtamount=bdamounts
            data.Declaration=declaration
            data.Discount=dis
            data.SpDiscount=spdis
            data.Marine_Rate=mrate
            data.Marine_Amount=mamount
            data.Ware_Rate=wrates
            data.Ware_Amount=wamount
            data.Net_Amount=netid
            data.Vat_Amount=vataid
            data.Stump_Amount=samount
            data.Gross_Amount=gross
            data.Producer=producer
            data.RiskCover=risk
            data.narration=nara
            data.userc=createuser
            data.sendmail=tomail
            data.Printed_No=prints
            data.MR_Number=mrnusss
            data.Coins_Leader=coinsur
            data.Coins_None_Leader=nonlider
            data.Coins_Leader_Persent=leaderpersent
            data.Coins_Leader_Doc=ldocu
            data.Coins_Leader_Name=leadercom
            data.save()
            all = MarineQuatationM.objects.filter(Bill_No=id)
            good = serializers.serialize('json', all)
            abcs = json.loads(good)
            abc = 'Data Update'
            return JsonResponse({'id':id,'messages':abc,'abcs':abcs},status=200,safe=False)


def uw_q_marine_cover_pdfsV(request, id=0):
    cv_banner=covernover_banner.objects.all()
    marine_bill = MarineCovernoteM.objects.filter(Cover_No_no=id)
    for x in marine_bill:
        amount = num2words(x.Bdtamount, lang="en_IN")
        mrcl = MRTable.objects.filter(id=x.MR_Number_id)
    template_path = 'uw/reports/marine_cover_note_f.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'marine_bill': marine_bill,'amount':amount,'cv_banner':cv_banner,'mrcl':mrcl}
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
    data = MarineCovernoteM.objects.get(Cover_No_no=id)
    data.Edits = 1
    data.save()
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def uw_q_marine_cover_demo_pdfsV(request, id=0):
    cv_banner=covernover_banner.objects.all()
    marine_bill = MarineCovernoteM.objects.filter(Cover_No_no=id)
    for x in marine_bill:
        amount = num2words(x.Bdtamount, lang="en_IN")
        mrcl = MRTable.objects.filter(id=x.MR_Number_id)
    template_path = 'uw/reports/marine_cover_note_f_demo.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'marine_bill': marine_bill,'amount':amount,'cv_banner':cv_banner,'mrcl':mrcl}
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



def uw_mr_marine_cover_demo_pdfsV(request, id=0):
    marine_bill = MarineCovernoteM.objects.filter(Cover_No_no=id)
    for x in marine_bill:
        mrcl = MRTable.objects.filter(id=x.MR_Number_id)
        for y in mrcl:
            if y.Service_Charge is None:
                amount = num2words(y.Gross_Amount, lang="en_IN")
            else:
                abc=y.Gross_Amount-y.Service_Charge
                amount = num2words(abc, lang="en_IN")
    template_path = 'uw/mrreport/mr.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'marine_bill': marine_bill,'amount':amount,'mrcl':mrcl}
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
    data = MarineCovernoteM.objects.get(Cover_No_no=id)
    data.Edits = 1
    data.save()

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def uw_mr_leader_marine_cover_demo_pdfsV(request, id=0):
    marine_bill = MarineCovernoteM.objects.filter(Cover_No_no=id)
    for x in marine_bill:
        mrcl = MRTable.objects.filter(id=x.MR_Number_id)
        for y in mrcl:
            if y.Service_Charge is None:
                amount = num2words(y.Gross_Amount, lang="en_IN")
            else:
                abc=y.Gross_Amount-y.Service_Charge
                amount = num2words(abc, lang="en_IN")
    template_path = 'uw/mrreport/mr_leader.html'
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'project\static')
    context = {'company': company, 'path': path, 'marine_bill': marine_bill,'amount':amount,'mrcl':mrcl}
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
    data = MarineCovernoteM.objects.get(Cover_No_no=id)
    data.Edits = 1
    data.save()

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def hr_bank_info_excleV(request):
    user_branch = Software_Permittion_Branch.objects.filter(user=request.user.id)
    user_current_branch = Software_Permittion_Branch.objects.filter(Branch=request.user.last_name, user=request.user.id)
    return render(request,'hr/forms/bank_info_excel.html',{'company':company,'user_current_branch':user_current_branch,'user_branch':user_branch})

def hr_bank_info_exclesavev(request):
    if request.method == 'POST':
        person_resource = Bank_nameResource()
        dataset = Dataset()
        new_persons = request.FILES['Bank_n']
        if not new_persons.name.endswith('xlsx'):
            messages.info(request,'Format Does Not Match')
        else:
            imported_data = dataset.load(new_persons.read(), format='xlsx')
            # print(imported_data)
            for data in imported_data:
                print(data[1])
                value = BankM(
                    data[0],
                    data[1]

                )
                value.save()

                messages.info(request,'Data saved')

            # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'hr/forms/message.html')

def uw_marine_addendumV(request):
    return render(request,'uw/forms/addendum/marineaddendum.html')

def TestV(request):
    marine_bill = MarineCovernoteM.objects.filter(Cover_No_no=1)
    for x in marine_bill:
        amount = num2words(x.Gross_Amount, lang="en_IN")
    return render(request, 'uw/reports/marine_cover_note_f.html',{'company':company,'marine_bill':marine_bill,'amount':amount})


