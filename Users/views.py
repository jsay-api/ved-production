from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.http import Http404

def form(request):
	return render(request, 'login.html')


def login(request):
	if request.method == 'POST':
		# print ("POST data =", request.POST)
		username = request.POST.get('login')
		password = request.POST.get('password')
		# print(username)
		user = auth.authenticate(username = username, password = password)
		# print ('login -> user = ', user)
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'login.html', {'username': username, 'errors': True})
	raise Http404

