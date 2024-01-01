from django.shortcuts import render,redirect,get_object_or_404
from posts.models import Post,Comment
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import PostCreateForm,CommentForm
from django.urls import reverse
from hitcount.views import HitCountDetailView,HitCountMixin
from hitcount.models import HitCount
from hitcount.utils import get_hitcount_model
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator


# Create your views here.

from datetime import datetime

# Example ISO 8601 formatted string
iso_string = "2022-01-15T15:30:00"

# Create a datetime object from the ISO 8601 formatted string
dt_object = datetime.fromisoformat(iso_string)


class PostView(View):
    model  = Post
    count_hit = False

    def get(self,request):
        post_list = Post.objects.filter(status=Post.Status.Verified).order_by('id')
        search_query = request.GET.get('q','')
        if search_query:
            post_list = post_list.filter(title__icontains=search_query)

        paginator = Paginator(post_list,2)
        page_num = request.GET.get('page',2)
        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj':page_obj,
            'search_query':search_query
        }
        return render(request,'posts/postList.html',context)

class PostDetail(HitCountDetailView,View):
    model = Post    
    count_hit = True
    template_name = 'posts/postDetail.html'

    def get(self,request,pk):
        post = get_object_or_404(Post,id=pk,status=Post.Status.Verified)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        context = {}
        hit_count = HitCount.objects.get_for_object(post)
        hit_count = get_hitcount_model().objects.get_for_object(post)
        hits = hit_count.hits
        hitcontext = context['hitcount'] = {'id':hit_count.id}
        hit_count_response = HitCountMixin.hit_count(request,hit_count)
        if hit_count_response.hit_counted:
            hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

        context = {
            'post':post,
            'comments':comments,
            'comment_form':comment_form,
            'hits':hits
        }
        return render(request,'posts/postDetail.html',context)

    def post(self,request,pk): # Posting comments
        post = Post.objects.get(id=pk)
        comment_form = CommentForm(data=request.POST)
        comments = post.comments.filter(active=True)
        if comment_form.is_valid():
            Comment.objects.create(
               post = post,
               author = request.user,
               text = comment_form.cleaned_data['text']               
           )
            comment_form = CommentForm()

        else:
            comment_form = CommentForm(data=request.POST)

        context = {
            'post':post,
            'comments':comments,
            'comment_form':comment_form
        }    
        return render(request,'posts/postDetail.html',context)

class WeeklyPopularPosts(View):
        
    def get(self,request):
        
        posts_list = Post.objects.filter(status=Post.Status.Verified)
        for post in posts_list:            
            context = {}
            # hitcount
            hit_count = get_hitcount_model().objects.get_for_object(post)
            hits = hit_count.hits
            hitcontext = context['hitcount'] = {'id':hit_count.id}
            hit_count_response = HitCountMixin.hit_count(request,hit_count)
            if hit_count_response.hit_counted:
                hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits            
            # Get the post list filtered by the publish time within the last week
            start_time = (timezone.now() - timedelta(days=7))
            post_list = Post.objects.filter(publish_time__gt=start_time,status=Post.Status.Verified).order_by('hit_count_generic')
            search_query = request.GET.get('q','')
            if search_query:
                post_list = post_list.filter(title__icontains=search_query)
            
            paginator = Paginator(post_list,2)
            page_num = request.GET.get('page',1)
            page_obj = paginator.get_page(page_num)


            context = {
                'post_list':post_list,
                'page_obj':page_obj,
                'search_query':search_query
            }

            return render(request,'posts/week.html',context)   

class MonthlyPopularPosts(View):

    def get(self,request):
        post_list = Post.objects.filter(status=Post.Status.Verified).order_by('id')       
        for post in post_list:
            context = {}
            hit_count = get_hitcount_model().objects.get_for_object(post)
            hits = hit_count.hits
            hitcontext = context['hitcount'] = {'id':hit_count.id}
            hit_count_response = HitCountMixin.hit_count(request,hit_count)
            if hit_count_response.hit_counted:
                hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits
            start_time = timezone.now() - timedelta(days=30)
            post_list = post_list.filter(publish_time__gt=start_time).order_by('hit_count_generic')
        search_query = request.GET.get('q','')
        if search_query:
            post_list = post_list.filter(title__icontains=search_query)
            
        paginator = Paginator(post_list,2)
        page_num = request.GET.get('page',1)
        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj':page_obj,
            'search_query':search_query
            }
        return render(request,'posts/month.html',context)

class RecommendedPostsView(View):
    
    def get(self,request):
        post_list = Post.objects.filter(recommendation=Post.Recommendation.Recommended).order_by('id')
        for post in post_list:
            context = {}
            hit_count = get_hitcount_model().objects.get_for_object(post)
            hits = hit_count.hits
            hitcontext = context['hitcount'] = {'id':hit_count.id}
            hit_count_response = HitCountMixin.hit_count(request,hit_count)
            if hit_count_response.hit_counted:
                hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
        search_query = request.GET.get('q','')
        if search_query:
            post_list = post_list.filter(title__icontains=search_query)
        
        paginator = Paginator(post_list,2)
        page_num = request.GET.get('page',1)
        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj':page_obj,
            'search_query':search_query
        }

        return render(request,'posts/recommended.html',context)
    
class PopularPostsView(View):

    def get(self,request):
        post_list = Post.objects.order_by('hit_count_generic')
        for post in post_list:
            # hitcount
            context = {}
            hit_count = get_hitcount_model().objects.get_for_object(post)
            hits = hit_count.hits
            hitcontext = context['hitcount'] = {'id':hit_count.id}
            hit_count_response = HitCountMixin.hit_count(request,hit_count)
            if hit_count_response.hit_counted:
                hits = hits + 1
                hitcontext['hit_counted'] = hit_count_response.hit_counted
                hitcontext['hit_message'] = hit_count_response.hit_message
        # q
        search_query = request.GET.get('q','')
        if search_query:
            post_list = Post.objects.filter(title__icontains=search_query)  
        # paginator objects
        paginator = Paginator(post_list,2)
        page_num = request.GET.get('page',1)
        page_obj = paginator.get_page(page_num)
        
        context = {
            'search_query':search_query,
            'page_obj':page_obj
        }
        return render(request,'posts/popular.html',context)
            

class CreatePostView(LoginRequiredMixin,View):

    def get(self,request):
        form = PostCreateForm()
        context = {
            'form':form
        }
        return render(request,'posts/postCreate.html',context)

    def post(self,request):
        form = PostCreateForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            Post.objects.create(
                author = request.user,
                title = form.cleaned_data['title'],
                picture = form.cleaned_data['picture'],
                text = form.cleaned_data['text']
            )
            return redirect('posts:post_list')
        else:
            return render(request,'posts/postCreate.html',{'form':form})




