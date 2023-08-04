from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *
from .helpers import *
from .forms import *
import os
import random
from PIL import Image
import requests as rq
from io import BytesIO

# Create your views here.

def home(request):
    context = {'blogs': BlogModel.objects.all()}
    # context={}
    return render(request, 'home.html', context)




def login_view(request):
    return render(request, 'login.html')




# def register_view(request):
#     return render(request, 'register.html')




def RegisterView(request):
    if request.method == "POST":
        postdata = request.POST.copy()
        username = postdata.get('RUsername', '')
        password = postdata.get('RPassword1', '')
        password2 = postdata.get('RPassword2', '')
        print(username,password , password2)
        # check if user does not exist
        if User.objects.filter(username=username).exists():
            username_unique_error = True
            return HttpResponse("Username must be unique")

        else :
            if password == password2:
                create_new_user = User.objects.create_user(username=username, email=username)
                create_new_user.set_password(password)
                create_new_user.save()
                token = generate_random_string(20)
                user = authenticate(username=username, password=password)
                Profile.objects.create(user=create_new_user, token=token,
                                   is_verified=True)
                print(user)
                
                print('User Logged In by signing in ')
                if create_new_user is not None:
                    if create_new_user.is_active:  
                        return redirect('login')
                    else:
                        print("The password is valid, but the account has been disabled!")
            else:
                return HttpResponse("Password and Confirm password should be same.")



    return render (request,'register.html')




def LogoutPage(request):
    logout(request)
    print('user logged out')
    return redirect('home')




def LoginUser(request):
    page_title = "Login"
    print(request.method)
    if request.method == "POST":
        data = request.POST.copy()
        username = data.get('loginUsername', '')
        password = data.get('loginPassword', '')
        print(username,password,'printed data')
        try:
            user = User.objects.filter(username=username).first()
            print(user)
            # if user is not None:
            #     login(request, user)
                
                
            if not Profile.objects.filter(user=user).first().is_verified:
                raise Exception('profile not verified')
            user_obj = authenticate(username=username,
                                    password=password)
            if user_obj:
                login(request, user_obj)
                print('User logged in')
                return redirect('home')
            else:
                print('User not logged in')
                error = True
        except:
            print('User not logged in')
            error = True

    return render(request, 'login.html', {'page_title': page_title})
    







def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            print(blog_obj)
            return redirect('/add-blog/')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)






def see_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request, 'see_blog.html', context)





def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)



def blog_update(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            # blog_obj = BlogModel.objects.create(
            #     user=user, title=title,
            #     content=content, image=image
            # )
            blog_obj.user = user
            blog_obj.title = title
            blog_obj.content = content
            blog_obj.image = image

            blog_obj.save()

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)







def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')









import pandas as pd
def CreateExcel(request):
    blog_list = BlogModel.objects.all()
    data=[]
    for i in blog_list:
        data.append({
            "title" :i.title ,
            "content" : i.content,
            "slug" : i.slug,
            "user" : i.user,
            
        })
    pd.DataFrame(data).to_excel("Report.xlsx")

    return render(request,"convertToExcel.html")










def upload_data_to_DataBase(request):

    if request.method == 'POST':
       upload_to=ExcelToDB.objects.create(file=request.FILES['files'])
       df=pd.read_excel(f"{settings.BASE_DIR}/public/static/{upload_to.file}")
       df.values.tolist()
    #    data=[]
       for i in (df.values.tolist()):
            username = str(i[4])
            password = 'password13'
            if User.objects.filter(username=username).exists():
                create_new_user = User.objects.filter(username=username)[0]
                print("User exists")
                username_unique_error = True
            else:
                create_new_user = User.objects.create_user(username=username, email=username)
                create_new_user.set_password(password)
                create_new_user.save()
                token = generate_random_string(20)
                user = authenticate(username=username, password=password)
                Profile.objects.create(user=create_new_user, token=token,
                                   is_verified=True)
       for i in (df.values.tolist()):
            # rimage = None
            # if image_files:
            #     random_image = random.choice(image_files)
            #     # response = rq.get(f"{path}//{random_image}")
            #     image_url = f"{path}//{random_image}"
            #     response = rq.get(image_url)
            #     rimage_data = response.content
            #     rimage = SimpleUploadedFile(name=random_image, content=rimage_data, content_type='image/jpeg')

            blog_obj = BlogModel.objects.create(
                user=User.objects.filter(username=i[4])[0], title=i[1],
                content=i[2],
            )
    return render(request,"upload_here.html")
        