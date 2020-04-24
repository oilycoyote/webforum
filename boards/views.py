from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board, Topic, Post
# from datetime import datetime
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
        board.total_posts = 0

        topics_in_board = Topic.objects.all().filter(board=board)
        
        for topic in topics_in_board:
            
            posts_in_topic = Post.objects.all().filter(topic=topic)
            board.total_posts += len(posts_in_topic)


    # Gets last updated post    
    for board in boards_list:

        # Picks one to be able to compare and attach object to outter loop.
        board.post_last_modified = Post.objects.all().first()

        topics_in_board = Topic.objects.all().filter(board=board)
        
        for topic in topics_in_board:
            
            latest_post = Post.objects.all().filter(topic=topic).order_by('-updated_at').first()

            if latest_post is not None:
                # Compares new latest date with saved date. Saves latest date. 
                if latest_post.updated_at > board.post_last_modified.updated_at:
                    board.post_last_modified = latest_post    
     

    # Context to pass to template
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
            my_post.board = my_post.topic.board
            my_post.created_by = request.user
            my_post.save()
            
            # Success message and redirect to post created.
            topic_subject = topic_form.cleaned_data.get('subject')
            messages.success(request, f'Subject posted: {topic_subject}')
            return redirect('post', topic_id=my_topic.id)


    # Gets form and sends to template. (Method: GET)
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


@login_required
def reply_post(request, topic_id):

    if request.method == 'POST':
        reply_post_form = PostNewForm(request.POST)

        if reply_post_form.is_valid():
            new_post = reply_post_form.save(commit=False)
            new_post.topic = Topic.objects.get(id=topic_id)
            new_post.created_by = request.user
            new_post.save()

            # Success message and redirect to post created.
            messages.success(request, f'Thank you. Your reply has been posted')
            return redirect('post', topic_id=new_post.topic.id)


    else: 
        reply_post_f = PostNewForm()
        
        
        topic_of_posts = get_object_or_404(Topic, pk=topic_id)
        related_posts = topic_of_posts.posts.all().order_by('-created_at')

        context = {
            'reply_post_f' : reply_post_f,
            'related_posts' : related_posts,
            'topic_of_posts' : topic_of_posts,
        }

        return render(request,'boards/reply_post.html', context)


@login_required    
def edit_post(request, post_id):

    post_to_edit = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        edit_post_f = PostNewForm(request.POST, instance=post_to_edit)

        if edit_post_f.is_valid():
            new_post = edit_post_f.save()

            messages.success(request, f'Thank you. Your post has been edited succesfully.')
            return redirect('post', topic_id=new_post.topic.id)

    else:
        edit_post_f = PostNewForm(instance=post_to_edit)

    related_posts = post_to_edit.topic.posts.all().order_by('-created_at')

    context = {
        'post_to_edit' : post_to_edit,
        'edit_post_f' : edit_post_f,
        'related_posts': related_posts,
    }
    
    return render(request, 'boards/edit_post.html', context)



