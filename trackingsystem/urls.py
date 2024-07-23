from django.urls import path
from .views import main_page, \
    search_results, create_par, \
    par_list, create_email_task, \
    change_par_status,\
    dash, user_pars,edit_par, edit_pars, par_detail, sign_pdf, save_signed_pdf


urlpatterns = [
    path('', user_pars, name='main_page'),
    path('search/',  search_results, name='search_results'),
    path('create/', create_par, name='create_par'),
    path('list/', par_list, name='par_list'),
    path('create_email_task/', create_email_task, name='create_email_task'),
    path('change_par_status/<int:par_id>/', change_par_status, name='change_par_status'),
    path('dashboard/', dash, name='dashboard'),
    path('user_pars/', user_pars, name='user_pars'),
    path('api/edit_par', edit_par),
    path('edit_par/<int:par_id>/', edit_pars, name='edit_par'),
    path('par_detail/<int:par_id>/', par_detail, name='par_detail'),
    path('sign_pdf/<int:par_id>/', sign_pdf, name='sign_pdf'),
    path('save_signed_pdf/<int:par_id>/', save_signed_pdf, name='save_signed_pdf'),

]


