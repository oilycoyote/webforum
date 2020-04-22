from django.shortcuts import render, get_object_or_404, redirect
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


    # Gets total posts in a board
    for board in boards_list:
        board.total_posts = len(Post.objects.all().filter(board=board))

    # Gets last updated post
    for board in boards_list:
        board.post_last_modified = Post.objects.all().filter(board=board).order_by('-updated_at').first()
     

    # Context to be passed to the template
    context = {
        'boards_list': boards_list,
    }

    return render(request, 'boards/index.html', context)


# Topic's Page
def topics(request, board_id):

    # Gets board by URL's Id. (board_id passed via URL)
    board = get_object_or_404(Board, pk=board_id)

    # Gets topics per board
    topics = Topic.objects.all().filter(board=board)

    # Gets last updated post
    for topic in topics:
        topic.post_last_modified = Post.objects.all().filter(topic=topic).order_by('-updated_at').first()

    # Gets posts per topic    
    for topic in topics:
        topic.posts_published = len(topic.posts.all())



    # Context to be passed to the template
    context = {
        'board' : board,
        'topics' : topics,
    }


    return render(request,'boards/topics.html', context)

# Post new topic
@login_required
def new_topic(request, board_id):
    
    # Gets Board to relate topic and post to specific board
    board = get_object_or_404(Board, pk=board_id)
    
    # Posting a new topic and post (Method: POST) 
    if request.method == 'POST':
        topic_form = TopicNewForm(request.POST)
        post_form = PostNewForm(request.POST)

        if topic_form.is_valid() and post_form.is_valid():
            
            # Saves data to topic model (new instance of topic) 
            my_topic = topic_form.save(commit=False)
            my_topic.board = Board.objects.all().filter(id=board_id).first()
            my_topic.starter = request.user
            my_topic.save()

            # Saves data to post model (new instance of post) The first post required to create a new topic         
            my_post = post_form.save(commit=False)
            my_post.topic = Topic.objects.all().filter(id=my_topic.id).first()
            my_post.board = Board.objects.all().filter(id=board_id).first()
            my_post.created_by = request.user
            my_post.save()
            
            # Success message and redirect to post created.
            topic_subject = topic_form.cleaned_data.get('subject')
            messages.success(request, f'Subject posted: {topic_subject}')
            return redirect('post', topic_id=my_topic.id)
    
    # Gets form and sends to template.
    else:        
        topic_form = TopicNewForm()
        post_form = PostNewForm()

        context = {
            'topic_form' : topic_form,
            'post_form' : post_form,
            'board' : board,
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


def reply_post(request, topic_id):

    topic_of_posts = get_object_or_404(Topic, pk=topic_id)
    related_posts = topic_of_posts.posts.all().order_by('-created_at')

    context = {
        'related_posts' : related_posts,
        'topic_of_posts' : topic_of_posts,

    }

    print(related_posts)
    print(topic_of_posts.board)
    print(topic_of_posts.subject)


    return render(request,'boards/reply_post.html', context)