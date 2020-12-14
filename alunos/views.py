from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from alunos.models import Aluno
from alunos.forms import AlunoForm


class AlunoIndexView(TemplateView):
	template_name = 'alunos/index-aluno.html'


@method_decorator(login_required, name='dispatch')
class AlunoNewView(SuccessMessageMixin, CreateView):
	model = Aluno
	template_name = 'alunos/aluno-novo.html'
	form_class = AlunoForm
	success_url = '/alunos/aluno-novo'
	success_message = 'Aluno Cadastrado com sucesso'

	def get(self, request, *args, **kwargs):

		context = {
			'aluno_obj': Aluno.objects.all(),
			'form': AlunoForm()
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = AlunoForm(request.POST)

		if form.is_valid():
			form_model = form.save(commit=False)
			form_model.save()
			form.save_m2m()
			messages.success(request, self.success_message)

			return redirect(self.success_url)

		else:
			context = {
				'aluno_obj': Aluno.objects.all(),
				'form': AlunoForm(request.POST)
			}

			return render(request, self.template_name, context)


class AlunoUpdateView(SuccessMessageMixin, UpdateView):
	model = Aluno
	form_class = AlunoForm
	template_name = 'alunos/aluno-alterar.html'
	success_message = 'As alterações foram efectuadas com sucesso'

	def get_form(self, form_class=None):

		form = super(AlunoUpdateView, self).get_form(form_class)

		return form

	def get_success_url(self):

		return reverse('aluno-alterar', kwargs={'pk': self.object.pk,})
