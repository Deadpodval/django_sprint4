from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from blogicum.users.froms import CustomUserRegisterForm
from django.views.generic.edit import CreateView


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserRegisterForm
    success_message = "Вы были успешно зарегистрированы"
