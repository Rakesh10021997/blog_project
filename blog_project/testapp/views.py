from django.shortcuts import render,get_object_or_404
from testapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag
from django.core.mail import send_mail
from testapp.forms import EmailSendForm
# Create your views here.

def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()

    tags=None#if tags in None program execute according to old flow other tag_slug condition in enter
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])


        paginator=Paginator(post_list,2)
        page_number=request.GET.get('page')
        try:
            post_list=paginator.page(page_number)
        except PageNotAnInteger:
            post_list=paginator.page(1)
        except EmptyPage:
            post_list=paginator.page(paginator.num_pages)
            return render(request,'testapp/post_list.html',{'post_list':post_list,'tag':tag})
    return render(request,'testapp/post_list.html',{'post_list':post_list})

#email

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='Published')
    send=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommand you to read "{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_url(post.get_absolute_url()) #get com pelte url  127.0.0.0:8000/2018/10/31/software-information
            message='Read Post At :\n {} \n\n{}\'s commants:\n{}'.format(post_url,cd['name'],cd['commennts'])
            send_mail('subject','message','Django9920@gmail.com',[cd['to']])
            send=True
    else:
        form=EmailSendForm()
        return render(request,'testapp/sharebymail.html',{'form':form,'post':post,'send':send})


from testapp.forms import CommentForm
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='Published',
                                           publish_year=year,
                                           publish_month=month,
                                           publish_day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'testapp/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})
