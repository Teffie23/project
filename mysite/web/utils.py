from .models import *
menu=[{'title':'О сайте','url_name':'reverse_top'},
      {'title':'обратая связь','url_name':'reverse_top'},
      {'title': 'главная страница', 'url_name': 'home'}
      ]
class DataMixin:
    def get_user_context(self,**kwargs):
        context=kwargs
        cats=trainer.objects.all()
        context['menu']=menu
        context['cats']=cats
        return context