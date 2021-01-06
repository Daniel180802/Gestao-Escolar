from django.shortcuts import redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from alunos.models import Aluno
from alunos.forms import AlunoForm


class AlunoIndexView(TemplateView):
	template_name = 'alunos/index-aluno.html'


class AlunoNewView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
	model = Aluno
	template_name = 'alunos/aluno-novo.html'
	form_class = AlunoForm
	success_url = '/alunos/aluno-novo'
	success_message = 'Aluno Cadastrado com sucesso'

	def test_func(self):
		"""
		Testa se o departamento do usuario logado,
		tem acesso a funções administrativas.
		"""

		authorized_admin_access = ['ad', 'se']  # lista de acesso a funções administrativas

		if self.request.user.department in authorized_admin_access:
			return True

	def handle_no_permission(self):
		"""
		Redirecionamentos no caso do departamento do usuário logado
		não ter acesso a funções administrativas.
		"""

		if self.raise_exception or self.request.user.is_authenticated:
			return redirect('index-manager')

		return redirect('login')


class AlunoUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Aluno
	form_class = AlunoForm
	template_name = 'alunos/aluno-alterar.html'
	success_message = 'As alterações foram efectuadas com sucesso'

	def test_func(self):
		"""
		Testa se o departamento do usuario logado,
		tem acesso a funções administrativas.
		"""

		authorized_admin_access = ['ad', 'se']  # lista de acesso a funções administrativas

		if self.request.user.department in authorized_admin_access:
			return True

	def handle_no_permission(self):
		"""
		Redirecionamentos no caso do departamento do usuário logado
		não ter acesso a funções administrativas.
		"""

		if self.raise_exception or self.request.user.is_authenticated:
			return redirect('index-manager')

		return redirect('login')

	def get_success_url(self):
		"""
		Redireciona para o mesmo formulário do aluno que está sendo alterado.
		"""

		return reverse('aluno-alterar', kwargs={'pk': self.object.pk,})
