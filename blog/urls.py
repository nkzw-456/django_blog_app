from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('detail/<str:pk>/', views.detail, name='detail'),
    path('list/', views.BlogListView.as_view(), name='list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('categorylist/', views.CategoryList.as_view(), name='category'),
    path('category_detail/<str:name_eng>', views.CategoryDetail.as_view(), name='categorydetail'),
    path('search/', views.Search, name='search'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.signup, name = 'signup'),


    # テスト用
    # path('test/', views.TestView.as_view(), name='test'),
    # path('categorylist/', views.CategoryList.as_view(), name='category'),

]