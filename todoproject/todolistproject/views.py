from datetime import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse 
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from todolistproject.models import Profile, Todo
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _



def index(request):
    profile = User.objects.filter(username=request.user)
    return render(request,'authentication\index.html',{'profile':profile})
def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST.get('password1')
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username is already taken')
        if User.objects.filter(email=email).exists():
            return HttpResponse('Email is already taken')
        if password != password1:
            return HttpResponse('password not matched')
        else:

             userregister = User.objects.create(username=username, email=email, password=password)
             userregister.first_name = fname
             userregister.last_name = lname

             userregister.save()
             messages.success(request, 'Account created successfully')
             return render(request, 'authentication\signin.html')
    return render(request, 'authentication\signup.html')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']  # Accept email or username
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)  # Use the custom backend
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'authentication/signin.html')
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    user_profile = Profile.objects.filter(user=request.user)
    current_user = request.user
    todolist = Todo.objects.filter(user=request.user)
    if request.method == 'POST':
        search = request.POST['search']
        todolist = Todo.objects.filter(user=request.user, task__icontains=search)
        if not todolist.exists():
            messages.error(request, 'No task found')

    sort_by = request.POST.get('sort', 'added_date') 
    if sort_by == 'added_date':
        todolist = todolist.order_by('id')
    elif sort_by == 'due_date':
        todolist = todolist.order_by('due')
    elif sort_by == 'priority':
        todolist = todolist.order_by('priority')
    else:
        messages.error(request, 'Invalid sorting option')
    
    return render(request, 'authentication/dashboard.html', {'todolist': todolist,
                                                             'profile': user_profile,
                                                               'current_user': current_user,
                                                               })
                                                             
@login_required
def delete(request, id):
    try:
        todo = Todo.objects.get(id=id)
        todo.delete()
        return redirect('dashboard')
    except Todo.DoesNotExist:
       messages.error(request, 'Task does not exist')
    return redirect('dashboard')
    

@login_required
def addtask(request):
    try:
        if request.method == 'POST':
            task=request.POST['todo']
            description=request.POST['description']
            priority=request.POST['priority']
            due=request.POST['duedate']
            todo = Todo.objects.create(user=request.user, task=task, description=description, priority=priority, due=due)
            todo.save()
            messages.success(request, 'Task added successfully')
    except:
        messages.error(request, 'Task not added')
    return render(request,'authentication/addtodo.html')

@login_required
def update(request, id):
    try:
        todo_up=Todo.objects.get(id=id, user=request.user)
    except:
        messages.error(request,'Task does not exits')
        return render(request, 'authentication/update.html')
    if request.method=='POST':
        todo_up.task=request.POST['todo']
        todo_up.description=request.POST['description']
        todo_up.priority=request.POST['priority']
        todo_up.due=request.POST['duedate']
        todo_up.save()
        messages.success(request, 'Task updated successfully')
        return redirect('dashboard')
    return render(request,'authentication/update.html',{'todo_up':todo_up})  

@login_required
def notfication(request):
    notification = Todo.objects.filter(user=request.user, due__lt=timezone.now(), completed=False)
    #retrieve all tasks that are overdue and not completed
    todo_due = Todo.objects.filter(user=request.user, due__lt=timezone.now(), completed=False)
    if todo_due.due < timezone.now():
        messages.warning(request, _('You have overdue tasks'))
    else:
        messages.success(request, _('No overdue tasks'))
    return render(request, 'authentication/msp2.html', {'notification': notification, 'todo_due': todo_due})



