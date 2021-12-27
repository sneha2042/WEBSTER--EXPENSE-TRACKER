from django.shortcuts import render , redirect, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate,login as authLogin
from .forms import UserRegisterForm,LoginForm
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
            #Profile.objects.create(user=request.user,income = 0,expenses=0,balance=0)
            #profile = Profile.objects.filter(user = request.user).first()
            return HttpResponse('Please confirm your email address to complete the registration')  
        else :
            print(form.errors)
            context={"messages":f"Not Valid "}
            return render(request,'signup.html',context=context)
    else:
        form=UserRegisterForm()
        print("Hello3")
    return render(request,"signup.html",{'form':form,'title':'register here'})
   

def home(request):
    user=request.user
    print(user)
    profile = Profile.objects.filter(user = request.user).first()
    #Profile.objects.create(user=request.user,income = 0,expenses=0,balance=0)
    #profile = Profile.objects.filter(user = request.user).first()
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
            print(amount)
            profile.balance += float(amount)
            profile.pos+=float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)
            profile.neg+=float(amount)
        
        profile.save()
        return HttpResponse('done')
    else:    
        print(profile)
        return render(request,'home.html',{'profile': profile,'mode':True})
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
        Profile.objects.create(user=user,income = 0,expenses=0,balance=0)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')      

      
def signin(request):
        form = LoginForm(request.POST)
        #next_ = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        #if next_ == '':
         #   next_ = settings.LOGIN_REDIRECT_URL
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #remember = form.cleaned_data['remember']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                profile = Profile.objects.filter(user = user).first()
                
                print("got")
                #redirect("expense")
                return render(request,'dashboard.html',{'user':user,'profile':profile,'mode':True})
                #return render(request,'home.html',{'profile': profile,'mode':True})
            #else:
                #form.add_error(None, "Unable to authorize user. Try again!")
        else:
            return render(request, "signin.html", {'form': form}) 

def category(request):
     user=request.user
     food=Expense.objects.filter(user=user,name="food")
     #transactions = Expense.objects.filter(user = request.user).first()
     profile = Profile.objects.filter(user = user).first()
     return render(request,"category.html",{'profile':profile,'food':food})

def history(request):
     user=request.user
     transaction=Expense.objects.filter(user=user)
     #profile=Profile.objects.filter(user=user).first()
     return render(request,"history.html",{'transaction':transaction})   

def graph(request):
    user=request.user
    profile=Profile.objects.filter(user=user).first()

    return render(request,"graph.html",{'itemp':profile.pos,'itemn':profile.neg})         

def expenses(request):
    return render(request,"dashboard.html")  
