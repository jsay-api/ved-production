from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.template import loader
from django.views.generic.base import View
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(redirect_field_name='')
def home(request):
	menu = 'disabled'
	context = {
		"menu0": menu
	}

	return render(request, 'index.html', context)

def BO(request):
	if request.is_ajax():
		menu = 'disabled'
		tab0 = 'active'
		query = request.POST['query']
		print(query)
		queryset_list = BeneficiariesOffshores.objects.all().order_by("offshore__off_name")
		
		if query:
			queryset_list = queryset_list.filter(
				Q(offshore__off_name__icontains=query) |
				Q(offshore__off_jurisdiction__icontains=query) |
				Q(offshore__off_parent__icontains=query) |
				Q(beneficiary__ben_name__icontains=query) |
				Q(beneficiary__ben_lastname__icontains=query) |
				Q(beneficiary__ben_holding__icontains=query) |
				Q(share__icontains=query) |
				Q(source__icontains=query) 
				).distinct()

		# paginator = Paginator(queryset_list, 5)
		# page = request.GET.get("page")
		# try:
		# 	queryset = paginator.page(page)
		# except PageNotAnInteger:
		# 	queryset = paginator.page(1)
		# except EmptyPage:
		# 	queryset = paginator.page(paginator.num_pages)
		context = {
			"inst_list" : queryset_list,
			"menu0": menu,
			"tab0": tab0
		}
		html = loader.render_to_string('BO.html', context)
		data = {'html': html}

		return JsonResponse(data)
	raise Http404


def AB(request):
	if request.is_ajax():
		menu = 'disabled'
		tab1 = 'active'
		query = request.POST['query']
		queryset_list = AssetsBeneficiaries.objects.all().order_by("asset__asset_name")
		# query = request.GET.get("q")
		
		if query:
			queryset_list = queryset_list.filter(
				Q(asset__asset_name__icontains=query) |
				Q(beneficiary__ben_name__icontains=query) |
				Q(beneficiary__ben_lastname__icontains=query) |
				Q(beneficiary__ben_holding__icontains=query) |
				Q(share__icontains=query) |
				Q(source__icontains=query) 
				).distinct()

		context = {
			"inst_list" : queryset_list,
			"menu0": menu,
			"tab1": tab1
		}
		html = loader.render_to_string('AB.html', context)
		data = {'html': html}

		return JsonResponse(data)


def AO(request):
	if request.is_ajax():
		menu = 'disabled'
		tab2 = 'active'
		query = request.POST['query']
		queryset_list = OffshoresAssets.objects.all().order_by("asset__asset_name")
		
		if query:
			queryset_list = queryset_list.filter(
				Q(asset__asset_name__icontains=query) |
				Q(offshore__off_name__icontains=query) |
				Q(offshore__off_jurisdiction__icontains=query) |
				Q(offshore__off_parent__icontains=query) |
				Q(share__icontains=query) |
				Q(source__icontains=query) 
				).distinct()

		context = {
			"inst_list" : queryset_list,
			"menu0": menu,
			"tab2": tab2
		}
		html = loader.render_to_string('AO.html', context)
		data = {'html': html}

		return JsonResponse(data)

class InstanceView(LoginRequiredMixin, DetailView):
	login_url = '/login/'
	redirect_field_name = ''
	model = None
	template_name = None

	def get_object(self):
		object = super(InstanceView, self).get_object()
		return object


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')

@login_required(redirect_field_name='')
def faq(request):
	menu = 'disabled'
	return render(request, 'faq.html', {"menu1": menu})


