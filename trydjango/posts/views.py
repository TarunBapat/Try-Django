from urllib.parse import quote_plus
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,get_object_or_404,redirect
from . models import Post
from .forms import PostForm

# Create your views here.
def post_home(request):
    return HttpResponse("<h1>Hello</h1>")

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form=PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request,"successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    else:
        messages.error(request,"not successfully created")    
    #if request.method=='POST':
     #   print (request.POST.get("content"))
      #  print (request.POST.get("title"))
    return render(request,'post_form.html',{'form':form})
        

def post_list(request):
    if request.user.is_authenticated:
        queryset_list=Post.objects.all()#.order_by("-timestamp")
        paginator = Paginator(queryset_list,10)
        page_request_var="page"
        page=request.GET.get(page_request_var)
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)

        context={
        "object_list":queryset,    
        "value":"some text value",
        "page_request_var":page_request_var
         }
    else:
        context={
            "value":"normal values"
        }
    return render(request,'post_list.html',context)
    #return HttpResponse("<h1>create</h1>")    

def post_detail(request,id):
    instance=get_object_or_404(Post,id=id)
    share_string=quote_plus(instance.content)
    context={
        "title":instance.title,
        "instance":instance,
        "share_string":share_string
    }
    return render(request,'post_detail.html',context)
    #return HttpResponse("<h1>detail</h1>")

def post_update(request,id):
    instance=get_object_or_404(Post,id=id)
    form=PostForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request,"item saved",extra_tags="added tag")
        return HttpResponseRedirect(instance.get_absolute_url())
    context={
        "title":instance.title,
        "instance":instance,
        "form":form
    }    
    
    return render(request,'post_form.html',context)

def post_delete(request,id):
    instance=get_object_or_404(Post,id=id)
    instance.delete()
    return redirect("posts:list")    



   