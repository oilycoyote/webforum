from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Board, Topic, Post
from datetime import datetime


# Homepage (Boards)

def index(request):
    boards_list = Board.objects.all()

    # Appends the number of topics per board
    for board in boards_list:
        board.num_topics= len(Topic.objects.all().filter(board=board))


    # Get total posts in a board
    for board in boards_list:
        board.total_posts = len(Post.objects.all().filter(board=board))

    # Get last updated post
    for board in boards_list:
        board.post_last_modified = Post.objects.all().filter(board=board).order_by('-updated_at').first()
     

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

    # Get posts pero topic    
    for topic in topics:
        topic.posts_published = len(topic.posts.all())


    # Context to be passed to the template
    context = {
        'board' : board,
        'topics' : topics,
    }


    return render(request,'topics.html', context)


def new_topic(request):
    return render(request,'new_topic.html')


def post(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    posts = Post.objects.all().filter(topic=topic)

    posts_created_by = None

    if posts:
        posts_created_by = len(Post.objects.all().filter(created_by=posts[0].created_by))

    context = {
        'topic': topic,
        'posts' : posts,
        'posts_created_by' :  posts_created_by,
    }

    return render(request,'post.html', context)


def reply_post(request):
    return render(request,'reply_post.html')