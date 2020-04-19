from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Board, Topic, Post
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import TopicNewForm, PostNewForm
from django.contrib import messages


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

    return render(request, 'boards/index.html', context)


# Topic's Page
def topics(request, board_id):

    # Get board by URL's Id. (board_id passed via URL)
    board = get_object_or_404(Board, pk=board_id)

    # Get topics per board
    topics = Topic.objects.all().filter(board=board)

    # Get last updated post
    for topic in topics:
        topic.post_last_modified = Post.objects.all().filter(topic=topic).order_by('-updated_at').first()

    # Get posts per topic    
    for topic in topics:
        topic.posts_published = len(topic.posts.all())



    # Context to be passed to the template
    context = {
        'board' : board,
        'topics' : topics,
    }


    return render(request,'boards/topics.html', context)

@login_required
def new_topic(request):
    if request.method == 'POST':
        print('Fue por POST')
        topic_form = TopicNewForm(request.POST)
        post_form = PostNewForm(request.POST)

        if topic_form.is_valid() and post_form.is_valid():
            topic_form.save()
            post_form.save()
            topic_subject = topic_form.cleaned_data.get('subject')
            messages.success(request, f'Subject posted: { topic_subject}')
            return redirect('index')
    else:        
        print('Fue por GET')
        topic_form = TopicNewForm
        post_form = PostNewForm

        context = {
            'topic_form' : topic_form,
            'post_form' : post_form,
        }

        return render(request,'boards/new_topic.html', context)

# Gets posts of a topic
def post(request, topic_id):
    
    topic = get_object_or_404(Topic, pk=topic_id)
    
    posts = Post.objects.all().filter(topic=topic)

    posts_created_by = None

    if posts:
        posts_created_by = len(Post.objects.all().filter(created_by=posts[0].created_by))
        topic.views_counter = topic.views_counter + 1
        topic.save()

    context = {
        'topic': topic,
        'posts' : posts,
        'posts_created_by' :  posts_created_by,
    }

    return render(request,'boards/post.html', context)


def reply_post(request):
    return render(request,'boards/reply_post.html')