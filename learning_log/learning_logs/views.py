from django.shortcuts import render,get_object_or_404
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    #The home page for Learning Log
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    #Show all topics.
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request,topic_id):
    #show a single topic and all its entries
    topic=get_object_or_404(Topic, id=topic_id)
    #make sure topic belongs to current user
    check_topic_owner(topic,request)
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    #add new topics
    if request.method!='POST':
        #no data submitted,create an empty form
        form=TopicForm()
    else:
        #POST data submitted , process data
        form=TopicForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))#returns user back to topics after they enter
        
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    
    #add entry for a particular entry
    topic=Topic.objects.get(id=topic_id)
    check_topic_owner( topic,request)
    if request.method!='POST':
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
        
    context={'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    check_topic_owner(topic,request)

    if request.method!='POST':
        #initial request:pre-fill form with current entry.
        form=EntryForm(instance=entry)
    else:
        #POST data submitted;process data.
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

#check topic owner
def check_topic_owner(topic,request):
    if topic.owner!=request.user:
        raise Http404