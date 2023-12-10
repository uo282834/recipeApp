from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm, SignUpForm, SignInForm

@login_required(login_url='/login')
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

@login_required(login_url='/login')
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)

            # Check if the user is authenticated before assigning the author
            if request.user.is_authenticated:
                recipe.author = request.user
            else:
                # Handle the case where the user is not authenticated according to your needs
                # You can redirect to a login page, display a message, etc.
                return redirect('login')  # Change 'login' to the URL of your login view

            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})
@login_required(login_url='/login')
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('recipe_list')  # Cambia 'home' por la URL a la que quieres redirigir al usuario después de registrarse
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('recipe_list')  # Cambia 'home' por la URL a la que quieres redirigir al usuario después de iniciar sesión
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def my_recipes(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'my_recipes.html', {'recipes': recipes})

@login_required(login_url='/login')
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Verifica si el usuario actual es el autor de la receta
    if request.user == recipe.author:
        # Elimina la receta
        recipe.delete()
        return redirect('recipe_list')
    else:
        # Redirige a algún lugar si el usuario no tiene permisos para eliminar
        return redirect('recipe_list')

@login_required(login_url='/login')
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Verifica si el usuario actual es el autor de la receta
    if request.user == recipe.author:
        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            if form.is_valid():
                form.save()
                return redirect('recipe_list')
        else:
            form = RecipeForm(instance=recipe)
        return render(request, 'recipe_edit.html', {'form': form})
    else:
        # Redirige a algún lugar si el usuario no tiene permisos para editar
        return redirect('recipe_list')


