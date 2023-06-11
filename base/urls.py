from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView , RegisterPage , TaskComplete, TaskUncomplete
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),#when logout redirect to the login page
    path('register/',RegisterPage.as_view(),name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'), #pk is primary key
    path('task-create', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
    path('task-complete/<int:pk>', TaskComplete, name='task-complete'),
    path('task-uncomplete/<int:pk>', TaskUncomplete, name='task-uncomplete'),
]