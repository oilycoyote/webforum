from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Board, Topic


# Homepage (Boards)

def index(request):
    boards_list = Board.objects.all()

    # Appends the number of topics per board
    for board in boards_list:
        board.num_topics= len(Topic.objects.all().filter(board=board))

    # Context to be passed to the template
    context = {
        'boards_list': boards_list,
    }

    return render(request, 'index.html', context)


# Topic's Page
def topics(request, board_id):

    # Get board by URL's Id. (board_id passed via URL)
    board = get_object_or_404(Board, pk=board_id)

    # Get topics per board
    topics = Topic.objects.all().filter(board=board)

    # Context to be passed to the template
    context = {
        'board' : board,
        'topics' : topics,
    }


    return render(request,'topics.html', context)


def new_topic(request):
    return render(request,'new_topic.html')


def post(request):
    return render(request,'post.html')


def reply_post(request):
    return render(request,'reply_post.html')