from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post  # 같은폴더에 있기 때문에 상대경로로 사용하는게 나음
from django.utils import timezone
from django.contrib.auth import get_user_model
from .forms import PostCreateForm

User = get_user_model()


def post_list(request):
    # posts 변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋)를 대입
    # posts변수에 ORM을 이용해서 published_date timezone을 이용해서
    # 최근 이전에 퍼블리쉬 되었던 글들만 전달
    posts = Post.objects.all().order_by('-created_date')
    # posts = Post.objects.filter(published_date__lte=timezone.now())
    context = {
        'title': 'PostList from post_list view',
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context=context)


def post_detail(request, pk):  # pk라는 파라미터를 줘야함
    print('post_detail pk', pk)
    # post라는 키값으로 Post객체 중 pk또는 id값이 매개변수로 주어진 pk변수와 같은 Post객체를 전달
    # posts = Post.objects.get(id=pk)
    context = {
        'post': Post.objects.get(id=pk)

    }
    return render(request, 'blog/post_detail.html', context=context)


def post_create(request):
    if request.method == 'GET':
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_create.html', context)
    elif request.method == 'POST':
        # Form클래스의 생성자에 POST데이터를 전달하여 Form인스턴스를 생성
        form = PostCreateForm(request.POST)
        # Form인스턴스의 유효성을 검사하는 is_valid메서드
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            user = User.objects.first()
            post = Post.objects.create(
                title=title,
                text=text,
                author=user,
            )
            return redirect('post_detail', pk=post.pk)
        # 유효성 검사를 통과하지 못했을 경우 error가 담긴 form을 이용해 기존페이지를 보여줌
        else:
            context = {
                'form': form,
            }
            return render(request, 'blog/post_create.html', context=context)
            # create를 실행하는 순간 데이터베이스에 들어감


def post_modify(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        # POST요청(request)가 올 경우 전달받은 데이터의 title, text값을 사용해서
        # 해당하는 Post인스턴스 (post)의 title, text속성값에 덮어씌우고
        # DB에 업데이트하는 save()메서드 실행
        data = request.POST
        title = data['title']
        text = data['text']
        post.title = title
        post.text = text
        post.save()
        return redirect('post_detail', pk=post.pk)
    elif request.method == 'GET':
        # pk에 해당하는 Post인스턴스를 전달

        context = {
            'post': post,
        }
        return render(request, 'blog/post_modify.html', context)
