from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    """How the post_list view works.
    - Take an optional slug parameter that has a default of None but if there is will be in the URL.
    - All published posts will be retrieved and if a published post has a tag/tags, the Tag object,
     is retrieved.
     -Posts are then filtered by the ones that have tags"""

    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # filter through the list of posts for the post instances that have the given tag/tags
        object_list = object_list.filter(tags__in=[tag])


    # we are paginating the post list using a Paginator class to make sure only 3 posts appear 
    # on the post list page at a time
    paginator = Paginator(object_list, 3) 
    page = request.GET.get('page') # this indicates the current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer return the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page of results
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'page': page,
        'tag': tag,
        }

    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    # to retrieve active comments of the post instance
    comments = post.comments.filter(active=True)  # remember it is post.comments.filter because of the related_name attribute
    # in the post field of Comment model

    # also give our users opportunity to add new comments
    # defining a new_comment variable and making it empty by assigning to None
    new_comment = None


    # CommentForms will be handled in the post_detail view 
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create Comment but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # then assign the current post to the comment
            new_comment.post = post
            # now save
            new_comment.save()
        else:
            comment_form = CommentForm()

            # note to self: save() method is available for ModelForm instances and not Form instances because
            # they are not linked to any models

    # recommending posts to user based on similarity of tags. In order to do this:
    # - returning all tags of the particular post instance
    # - get all the other posts that have any of those tags
    # - exclude the current post from the list of posts you will recommend as having similar tags
    # - the greater the number of tags shared between one post and the subject post, the greater the similarity
    # - if posts share the same number of tags choose the most recent one
    # - we limit the query to the number of posts we want to recommend


    #the values_list returns a tuple for a given field
    # convert the tags id's of the post instance into a list with flat=True because tuples are not iterables.
    post_tags_id = post.tags.values_list('id', flat=True)
    # use the post id's to search for other posts that share same tag but the particular post itself
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    # count the number of tags using the Count aggregation method, then order
    # for the posts with more tags and if share same tags for most recently published
    # negative prefix denotes descending order
    # only first 4 posts retrieved are recommended
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]



    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': commment_form,
        'new_comment': new_comment,
        'similar_posts': similar_posts,
    })


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    # after retrieving 
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            # cleaned_data acts like a dictionary that stores the validated fields
            cd = form.cleaned_data
            # send email
            # build a complete URL including HTTP schema and hostname using request.build_absolute_url with post.get_absolute_url
            # as path 
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = f"{cd['name']} {cd['email']} recommends you reading {post.title}"
            message = f"Read {post.title} at {post_url} \n{cd['name']}'s comments: {cd['comments']}"
            # [cd['to']] is a list because send_mail function takes the receipients as a list
            send_mail(subject, message, 'gabdanq@gmail.com', [cd['to']]) 
            sent = True
    else:
        # if no request post method return a new form instance 
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent,
    })

# Create your views here.


# class based listview commented out
"""class PostListView(ListView):
    # since i defined the model manager in models.py to retrive only published posts,
    # there is no need for me to create a def get_queryset() class method like i did in the polls app,
    # and can just use a queryset attribute to link to my model manager to do the filtering
    # i think this decouples my code too. Sweet!!

    # also because we were retrieving a particular set of objects,
    # we didn't use the generic attibute model = Post which would have rather fetched,
    # model = Post which is equal to Post.objects.all() queryset
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'"""


