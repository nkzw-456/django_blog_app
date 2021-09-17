from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from blog.models import Blog
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, DetailView, ListView, FormView
from .models import Blog, Comment, Category
from .forms import CommentForm, ContactForm, SearchForm, LoginForm, UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

# ログイン必須の項目につける
# from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    obj = Blog.objects.order_by('-created_at')
    object_list = Paginator(obj, 3)
    page_number = request.GET.get('page')
    category_list = Category.objects.all()
    context = {
        'object_list': object_list.get_page(page_number),
        'category_list': category_list
    }
    return render(request, 'blog/index.html', context)
    # pagination含む


def detail(request, pk):
    obj = Blog.objects.get(pk=pk)
    comments = Comment.objects.filter(blog=obj)
    context = {
        'blog': obj,
        'comments': comments,
    }
    if request.method =='POST':
        if request.POST.get('like_count', None):
            obj.count += 1
            obj.save()
        # like_countのnameが入ったものにpostが実行されたときに
        # countが１増加するようになる

        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            text.blog = obj
            text.save()

        # POSTを受け取った場合,formsのCommentFormを呼び出す
        # htmlのnameとformsの変数があっているのを確認する
        # validationを行って問題なければdbに保存する

    # Blogの個別ページをobjに代入
    # それをcontext内にkey=blog, value:model変数になっている
    # ロードするときは{{blog.title}}で出力可能

    return render(request, 'blog/detail.html', context)



class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.order_by('-created_at')
    paginate_by = 10
    template_name = 'blog/blog_list.html'


class ContactView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class CategoryList(ListView):
    model = Category
    template_name = 'blog/category.html'



class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name_eng'
    slug_url_kwarg = 'name_eng'

    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(name_eng = self.kwargs['name_eng'])
        category_posts = Blog.objects.filter(category = detail_data.id).order_by('-created_at')

        context = {
            'object': detail_data,
            'category_posts': category_posts
        }

        return context


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Blog.objects.filter(Q(title__icontains = freeword)|Q(body__icontains = freeword))

            context = {
                'search_list': search_list,
            }

            return render(request, 'blog/search.html', context)
# cleanedしたfreewordを代入、Blogにfilterをかけてimport Qで検索をかける
# contextに代入して、結果を出力する

class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了 ようこそ')
        return super().form_valid(form)


class Logout(LogoutView):
    template_name = 'registration/logout.html'


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, '登録完了!')
            return redirect('login')
    return render(request, 'registration/signup.html', context)





# テストよう
# class TestView(TemplateView):
#     template_name = 'test.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         object_list = Blog.objects.all().order_by('created_at')
#         category_list = Category.objects.all()
#         context = {
#             'object_list': object_list,
#             'category_list': category_list
#         }
#         print(context)
#         return context