from django.urls import path

from . import views, user_module

app_name = 'pastebin'
urlpatterns = [
    path('', views.NewPostView.as_view(), name='NewPost'),
    path('savePost/', views.savePost, name='SavenewPost'),
    path('<int:post_id>/savePost/', views.savePost, name='SavePost'),
    path('<str:url>/displayPost/', views.displayPost, name='DisplayPost'),
    path('newUserRegistration/', views.NewUserView, name='NewUserView'),
    path('<int:user_id>/viewallpost/', views.DisplayAllPostView.as_view(), name='DisplayAllPost'),
    path('saveUser/', user_module.saveNewUser, name='saveNewUser'),
    path('login/', user_module.authenticateUser, name='LoginUser'),
    path('logout/', user_module.logOutUser, name='LogOutView'),
]