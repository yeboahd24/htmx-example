from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from user.forms import RegisterForm, EmployeeForm, MarriedForm, MovieForm
from user.models import Film, Employee, Married, Movie
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.http import require_POST

# API Views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    template_name = 'registration/login.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)




class FilmList(LoginRequiredMixin, ListView):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        user = self.request.user
        return user.films.all()


def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")


@login_required
def add_film(request):
    name = request.POST.get('filmname')

    # add film
    film = Film.objects.get_or_create(name=name)[0]

    # add the film to the user's list
    request.user.films.add(film)

    # return template fragment with all the user's films
    films = request.user.films.all()
    messages.success(request, f"Added {name} to list of films")
    return render(request, 'partials/film-list.html', {'films': films})


@require_http_methods(['DELETE'])
@login_required
def delete_film(request, pk):
    # remove the film from the user's list
    request.user.films.remove(pk)

    # return template fragment with all the user's films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})


@login_required
def search_film(request):
    search_text = request.POST.get('search')

    # look up all films that contain the text
    # exclude user films
    userfilms = request.user.films.all()
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list('name', flat=True)
    )
    context = {"results": results}
    return render(request, 'partials/search-results.html', context)


def clear(request):
    return HttpResponse("")


def list_employees(request):
    employees = Employee.objects.all()
    return render(request, 'user.html', {'employees': employees})


# Update employee status

# def set_employee_status_active(request, pk):
#     employee = Employee.objects.get(pk=pk)
#     employee.status = 'Active'
#     employee.save()
#     return render(request, 'user.html')


def set_employee_status_active(request, pk):
    employee = Employee.objects.get(pk=pk)
    if employee.status == 'Active':
        employee.status = 'Inactive'
    else:
        employee.status = 'Active'
    employee.save()
    return render(request, 'user.html', {'employees': Employee.objects.all()})


def activate(request):
    if request.method == 'POST':
       ids = request.POST.getlist('ids')
       for id in ids:
           int_id = int(id)
           employee = Employee.objects.get(pk=int_id)
           employee.status = 'Active'
           employee.save()

    return render(request, 'bulk.html', {'employees': Employee.objects.all()})


def deactivate(request):
    if request.method == 'POST':
       ids = request.POST.getlist('ids')
       for id in ids:
           int_id = int(id)
           employee = Employee.objects.get(pk=int_id)
           employee.status = 'Inactive'
           employee.save()

    return render(request, 'bulk.html', {'employees': Employee.objects.all()})


class EmployeeUpdate(UpdateView):
    model = Employee
    fields = ['name']
    template_name = 'edit-user.html'
    context_object_name = 'form'
    success_url = reverse_lazy('list')


def employee_view(request):
    employee = Employee.objects.all()
    return render(request, 'edit.html', {'employees': employee})


# Get random three users
def random_employees(request):
    employees = Employee.objects.all().order_by('?')[:3]
    return render(request, 'auto_user.html', {'employees': employees})

# Married
def married(request):
    if request.method == 'POST':
        form = Married()
        
        form.name = request.POST.get('name')
        form.status = request.POST.get('status')
        form.wife = request.POST.get('wife')

        form.save()
        return HttpResponse('Thank you for your input')
    else:
        return render(request, 'married.html')


def married_htmx(request):
    if request.method == 'POST':
        form = MarriedForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your input')
    else:
        form = MarriedForm()
    return render(request, 'married.html', {'form': form})



# Movie view
def index(request):
    return render(request, 'movie_index.html')



def movie_list(request):
    return render(request, 'movie_list.html', {
        'movies': Movie.objects.all(),
    })


def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{movie.title} added."
                    })
                })
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {
        'form': form,
    })


def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{movie.title} updated."
                    })
                }
            )
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.html', {
        'form': form,
        'movie': movie,
    })


@ require_POST
def remove_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": f"{movie.title} deleted."
            })
        })

