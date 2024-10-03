from django.shortcuts import render,redirect
from django.views.generic import View
from notes.forms import TaskForm
from notes.models import Task
from django.contrib import messages
from django import forms
from django.db.models import Q
from django.db.models import Count

# Create your views here.

class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()

        return render(request,"task_create.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"Task Added Succesfully")

            return redirect("task-list")
        
        else:

            messages.error(request,"Failed to Add Task")

            return render(request,"task_create.html",{"form":form_instance})


class TaskListView(View):

    def get(self,request,*args,**kwargs):

        search=request.GET.get("search")

        selected_category=request.GET.get("category","all")

        if selected_category == "all":

            qs=Task.objects.all()

        else:

            qs=Task.objects.filter(category=selected_category)

        if search != None:

            qs=Task.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return render(request,"task_list.html",{"tasks":qs,
                                                "selected":selected_category
                                                })
    
class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"tasks":qs})
    
class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        # extracting pk from kwargs
        id=kwargs.get("pk")

        # fetching details from pk
        task_obj=Task.objects.get(id=id)

        # initialize taskform with task_obj
        form_instance=TaskForm(instance=task_obj)

        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select mb-3"}),initial=task_obj.status)

        return render(request,"task_edit.html",{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(request.POST,instance=task_obj)

        if form_instance.is_valid():

            form_instance.instance.status=request.POST.get("status")

            form_instance.save()

            return redirect("task-list")
        
        else:

            return redirect(request,"task_list.html",{"form":form_instance})
        
class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        Task.objects.get(id=kwargs.get("pk")).delete()

        return redirect("task-list")
    
# task Summary

class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.all()

        total_tasks_count=qs.count()
        
        category_summary=qs.values("category").annotate(cat_count=Count("category"))

        status_summary=qs.values("status").annotate(sta_count=Count("status"))

        context={

            "total_tasks_count":total_tasks_count,
            "category_summary":category_summary,
            "status_summary":status_summary,

        }

        return render(request,"task_summary.html",context)