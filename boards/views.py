from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User

from .models import Board,Topic,Post

def home(request):
    boards = Board.objects.all()
    """boards_names=list()

    for board in boards:
        boards_names.append(board.name)
    response_html = '<br>'.join(boards_names)
    return HttpResponse(response_html)"""
    return render(request,'home.html', {'boards':boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html',{'board':board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        user = User.objects.first() #get the currently logged in user
        topic = Topic.objects.create(subject=subject,board=board,starter=user)
        post=Post.objects.create(message=message,topic=topic,created_by=user)
        return redirect('board_topics',pk=board.pk) # redirect to the created topic page
    return render(request, 'new_topic.html',{'board':board})
