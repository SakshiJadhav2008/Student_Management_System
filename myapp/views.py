from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Students
from django.shortcuts import get_object_or_404

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return render(request,'signup.html')
        
        if len(pass1)<7:
            return HttpResponse("Please Enter a valid Password")

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists!")
        
        my_user = User.objects.create_user(uname,email,pass1)
        my_user.save()
        return redirect('sign_in')
    
    return render(request, 'signup.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('menu')
        else:
            return HttpResponse("Please check password and username again")

    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')

def logout_page(request):
    logout(request)
    return redirect('sign_in')


def first_page(request):
    query = request.GET.get('search')
    if query:
        students = Students.objects.filter(fname__icontains=query)
    else:
        students = Students.objects.all()
    # std=Students.objects.all()
    # context={
    #     'std_key':std
    # }

    return render(request,"show.html",{'students': students})

def create(request):
    if request.method=="POST":
        fname=request.POST.get('username')
        lname=request.POST.get('lastname')
        age=request.POST.get('age')
        address=request.POST.get('address')

        std=Students(fname=fname,lname=lname,age=age,address=address)
        std.save()
        return redirect('first_page')
    
    return render(request,"create.html")


def update(request,pk):
    student=get_object_or_404(Students,pk=pk)

    if request.method=="POST":
        student.fname=request.POST.get('first_name')
        student.lname=request.POST.get('last_name')
        student.age=request.POST.get('age')
        student.address=request.POST.get('address')
        student.save()
        return redirect('first_page')



    return render(request,"update.html",{'student':student})

#left side pk=refers to the field name in the model(here pk stands for primary key)
#right side pk=refers to the function parameter passed to the view(def update(request,pk))

def delete(request,rid):
    std=Students.objects.get(id=rid)
    std.delete()
    return redirect('first_page')


@login_required(login_url='sign_in')
def menu(request):
    return render(request,"menu.html")

def contact(request):
    return render(request,"contact.html")

def detail_student(request, id):
    student = get_object_or_404(Students, id=id)
    return render(request, 'detail.html', {'student': student})

