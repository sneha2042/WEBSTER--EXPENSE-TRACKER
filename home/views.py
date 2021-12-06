from django.shortcuts import render , redirect, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate,login as authLogin
from .forms import UserRegisterForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.utils.encoding import force_bytes, force_text  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.contrib.sites.shortcuts import get_current_site  
from django.core.mail import EmailMessage  
import requests

def homepage(request):
     return render(request,"homepage.html")

def signup(request):
    #print("Hello1")
    if request.method == "POST":
        #print("Hello2")
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            #print("GTfbv")
            #user.is_active=False
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            email=form.cleaned_data.get('email')
            username=form.cleaned_data.get('username')
            context={"messages":f"Welcome  {username} ! Sign up is successful "}
            return HttpResponse('Please confirm your email address to complete the registration')  
        else :
            context={"messages":f"Not Valid "}
            return render(request,'signup.html',context=context)
    else:
        form=UserRegisterForm()
        print("Hello3")
    return render(request,"signup.html",{'form':form,'title':'register here'})
   

def home(request):
    Profile.objects.create(user=request.user,income = 0,expenses=0,balance=0)
    profile = Profile.objects.filter(user = request.user).first()
    print(Profile.objects.filter(user = request.user).first())
    #expenses = Expense.objects.filter( user = request.user)
    if request.method == 'POST':
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')
        print(text)
        print(expense_type)
        expense = Expense(name = text ,amount = amount , expense_type = expense_type , user = request.user)
        expense.save()

        if expense_type == 'Positive':
            profile.balance += float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)
        
        profile.save()
        return HttpResponse('done')
    else:    
        return render(request,'home.html',{'profile': profile})
    #print(profile.balance)
    
    #context = {'profile' : profile , 'expenses' : expenses}   
    #return render(request,'home.html')

def activate(request, uidb64, token):  
    #User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')      
     
