from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tournament, Player
from .forms import TournamentForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

def check_user_login(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You need to login to create a tournament.')
            return redirect(reverse('login'))  # Redirect to the login page
    return wrapper

@check_user_login
def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.organizer = request.user
            tournament.save()
            return redirect('tournament_detail', pk=tournament.pk)
    else:
        form = TournamentForm()
    return render(request, 'create_tournament.html', {'form': form})


def join_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    user = request.user
    
    # Check if the player is already in the tournament
    if tournament.players.filter(user=user).exists():
        return render(request, 'already_joined.html', {'tournament': tournament})
    
    # If not, add the player to the tournament
    player = Player(tournament=tournament, user=user)
    player.save()
    
    return redirect('tournament_detail', pk=tournament_id)

@check_user_login
def tournament_detail(request, pk):
    tournament = Tournament.objects.get(pk=pk)
    return render(request, 'tournament_detail.html', {'tournament': tournament})

def home(request):
    return render(request, 'home.html')
@check_user_login
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament_list.html', {'tournaments': tournaments})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a page where the navbar can display the number of available tournaments
            return redirect('home')
        else:
            # Invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        
        return render(request, 'login.html')

def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')  # Redirect to the login page after registration
    else:
        return render(request, 'registration.html')

def logout_view(request):
    logout(request)
    return redirect('home') 