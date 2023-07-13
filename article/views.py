from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from article.forms import ArticleForm
from article.models import Article, Comment
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.

@login_required(login_url="user:login")
def index(request):
    numbers = {
        "number1": 3,
        "number2": 5,
        "number3": 7
    }
    numero = {
        "numeros": [2, 4, 6, 8, 10]
    }
    # return HttpResponse("<h3>Main Page</h3>") 
    return render(request, "index.html", numero)


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def detail(request, id):
    return HttpResponse("detail:" + str(id))


@login_required(login_url="user:login")
def dashboard(request):
    keyword = request.GET.get("keyword")
    if keyword:
        filtered_articles = Article.objects.filter(title__contains=keyword)
        paginator = Paginator(filtered_articles, 10)
        page = request.GET.get('page')
        paged_articles = paginator.get_page(page)
        return render(request, "article/dashboard.html", {"articles": paged_articles})

    articles = Article.objects.filter(author=request.user)
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        "articles": articles
    }
    return render(request, "article/dashboard.html", context)


@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        article = form.save(commit=False)  # creates only the article object
        article.author = request.user
        article.save()
        messages.success(request, "Successfully added a new article.")
        return redirect("article:dashboard")
    else:
        context = {
            "form": form
        }
        return render(request, "article/addarticle.html", context)


@login_required(login_url="user:login")
def detail(request, id):
    # article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()

    return render(request, "article/detail.html", {"article": article, "comments": comments})


@login_required(login_url="user:login")
def articleUpdate(request, id):

    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if request.POST and form.is_valid:
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Article has been successfully updated.")
        return redirect("article:dashboard")
    
    return render(request, "article/update.html", {"form": form})


@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("article:dashboard")


@login_required(login_url="user:login")
def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "article/articles.html", {"articles": articles})

    articles = Article.objects.all()

    return render(request, "article/articles.html", {"articles": articles})


@login_required(login_url="user:login")
def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author=comment_author, comment_content=comment_content)
        newComment.article = article
        newComment.save()
        messages.success(request, "Comment successfully added.")
        
    return redirect(reverse("article:detail", kwargs={"id": id}))
#/articles/article/" + str(id)