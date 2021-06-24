from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('new', views.new, name='new'),
    path('create', views.create, name='create'),
    path('<int:id>/edit', views.edit, name='edit'),
    path('<int:id>/update', views.update, name='update'),
    path('<int:id>/delete', views.delete, name='delete'),
    path('post/<int:unitNo>/<int:param>', views.post, name='post'),
    path('plot/', views.get_svg, name='plot'),
]
