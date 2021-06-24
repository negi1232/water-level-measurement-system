from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article
from .forms import SearchForm
from .forms import ArticleForm
import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import matplotlib
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def index(request):
    searchForm = SearchForm(request.GET)
    if searchForm.is_valid():
        keyword = searchForm.cleaned_data['keyword']
        articles = Article.objects.filter(user_name__contains=keyword).order_by("-id")
    else:
        searchForm = SearchForm()
        #articles = Article.objects.all()
        articles = Article.objects.order_by("-id")
    if 'pageNo' in request.GET:
        pageNo = request.GET['pageNo']
    else :
        pageNo=1
    
    #articles=reversed(articles.object)
    #articles=Article.objects.order_by('id').reverse().first()
    

    paginator  = Paginator(articles, 50)
    articles = paginator.get_page(int(pageNo))
    if searchForm.is_valid():
        context = {
            'message': '水位測定システム',
            'articles': articles,
            'searchForm': searchForm,
            'pageNo':pageNo,
            'keyword':keyword
        }
    else:
        context = {
            'message': '水位測定システム',
            'articles': articles,
            'searchForm': searchForm,
            'pageNo':pageNo,
        }
    return render(request, 'bbs/index.html', context)



def detail(request, id):
    article = get_object_or_404(Article, pk=id)
    context = {
        'message': 'Show Article ' + str(id),
        'article': article,
    }
    return render(request, 'bbs/detail.html', context)

# def new(request):
#     articleForm = ArticleForm()

#     context = {
#         'message': '',
#         'articleForm': articleForm,
#     }
#     return render(request, 'bbs/new.html', context)
    
def new(request):
    articleForm = ArticleForm()

    context = {
        'message': '',
        'articleForm': articleForm,
    }
    return render(request, 'bbs/new.html', context)
    
def post(request,unitNo ,param):
    dt_now = datetime.datetime.now()
    print(request)
    article = Article(content=param,user_name=unitNo,day_now=str(datetime.date.today()),time_now=str(dt_now.hour)+"時"+str(dt_now.minute)+"分"+str(dt_now.second)+"秒")
    article.save()
    return HttpResponse("UnitNo."+str(unitNo)+",value."+str(param)+"cm")

def create(request):
    print(ArticleForm(request.POST))
    if request.method == 'POST':
        articleForm = ArticleForm(request.POST)
        if articleForm.is_valid():
            article = articleForm.save()

    context = {
        'message': 'Create article ' + str(article.id),
        'article': article,
    }
    return render(request, 'bbs/detail.html', context)

def edit(request, id):
    article = get_object_or_404(Article, pk=id)
    articleForm = ArticleForm(instance=article)

    context = {
        'message': 'Edit Article',
        'article': article,
        'articleForm': articleForm,
    }
    return render(request, 'bbs/edit.html', context)

def update(request, id):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=id)
        articleForm = ArticleForm(request.POST, instance=article)
        if articleForm.is_valid():
            articleForm.save()

    context = {
        'message': 'Update article ' + str(id),
        'article': article,
    }
    return render(request, 'bbs/detail.html', context)

def delete(request, id):
    article = get_object_or_404(Article, pk=i)
    article.delete()

    articles = Article.objects.all()
    context = {
        'message': 'Delete article ' + str(id),
        'articles': articles,
    }
    return render(request, 'bbs/index.html', context)


def get_svg(request):
    setPlt()  
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

def setPlt():
    #x = ["0:00", "1:00", "07/03", "07/04", "07/05", "07/06", "07/07"]
    #articles = Article.objects.filter(day_now="2021-02-06")
    print(articles)
    x=list()
    y=list()
    for i in range(0,24,4):
        x.append(str(i)+":00")
        y.append(2+i)
    
    print(x)
    print(y)
    plt.bar(x, y, color='#00d5ff')
    plt.title(r"$\bf{Running Trend  -2020/07/07}$", color='#3407ba')
    plt.xlabel("Date")
    plt.ylabel("km")

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s