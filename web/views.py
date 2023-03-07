from django.shortcuts import render,redirect
# Create your views here.
from django.views.generic import CreateView,FormView,TemplateView,ListView,UpdateView
from .forms import LoginForm,UserRegistrationForm,PostForm,UpdateProfile,ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from api.models import Posts,Comments
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from api.models import *


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decs=[signin_required,never_cache]  

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})


@method_decorator(decs,name="dispatch")
class IndexView(ListView):
    template_name="index.html"
    model=Posts
    context_object_name="posts"


    
    def get_queryset(self):
        return Posts.objects.all()

class AddPost(CreateView):
    template_name="addpost.html"
    form_class=PostForm
    success_url=reverse_lazy("profile")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"you post added succesfully")
        return super().form_valid(form)

decs
def add_comments(request,*args,**kwargs):
    id=kwargs.get("id")
    pst=Posts.objects.get(id=id)
    cmt=request.POST.get("comment")
    Comments.objects.create(post=pst,
        comment=cmt,
        user=request.user)
    messages.success(request,"you answer posted successfully")
    return redirect("index")  

def like_post_view(request,*args,**kwargs):
    id=kwargs.get("id")
    pst=Posts.objects.get(id=id)
    if pst.like.contains(request.user):
        pst.like.remove(request.user)
    else:
        pst.like.add(request.user)
    return redirect("index")

def profile_delete_view(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()
    messages.success(request,"Removed successfully")
    return redirect("profile")

@method_decorator(decs,name="dispatch")
class ListPeopleView(ListView):
    template_name="follow/following.html"
    model = User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)

decs
def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")

class ProfileView(ListView):
    template_name="profile/profile.html"
    model=Posts
    context_object_name="posts"

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")

def edit_profile(request,*args,**kw):
    usr=User.objects.get(id=request.user.id)
    if request.method=="POST":
        form=UpdateProfile(request.POST,request.FILES,instance=usr)
        if form.is_valid():
            form.save()
            return redirect("profile")
        else:
            return render(request, "profile/edit_profile.html",{"form":form})
    else:
        form=UpdateProfile(instance=usr)
        return render(request,"profile/edit_profile.html",{"form":form})

class AddProfileView(CreateView):
    template_name="profile/profilepic.html"
    form_class=ProfileForm
    success_url=reverse_lazy("profile")

    def post(self, request,*args,**kw):    
        form=ProfileForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("index")
        else:
            return render(request,"profile.html",{"form":form})

            
#  profile pic change 
class EditprofileView(UpdateView):
    template_name="profile/edit.html"
    form_class=ProfileForm
    model=Userprofile
    pk_url_kwarg="id"
    success_url=reverse_lazy("profile")

decs
def comment_delete(request,*args,**kw):
    id=kw.get("id")
    Comments.objects.get(id=id).delete()
    return redirect("index")



def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")


