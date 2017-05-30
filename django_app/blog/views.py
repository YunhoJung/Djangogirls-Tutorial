from django.http import HttpResponse
from django.shortcuts import render
from .models import Post # 같은폴더에 있기 때문에 상대경로로 사용하는게 나
from django.utils import timezone


def post_list(request):
    # posts 변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋)를 대입
    # posts변수에 ORM을 이용해서 published_date timezone을 이용해서
    # 최근 이전에 퍼블리쉬 되었던 글들만 전달
    posts = Post.objects.filter(published_date__lte=timezone.now())
    context = {
        'title': 'PostList from post_list view',
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context=context)

def post_detail(request, pk): #pk라는 파라미터를 줘야함
    print('post_detail pk', pk)
    # post라는 키값으로 Post객체 중 pk또는 id값이 매개변수로 주어진 pk변수와 같은 Post객체를 전달
    # posts = Post.objects.get(id=pk)
    context = {
        'post':Post.objects.get(id=pk)

    }
    return render(request, 'blog/post_detail.html', context)
