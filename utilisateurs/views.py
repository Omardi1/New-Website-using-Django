from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

User = get_user_model()

def user(request):
    if request.method == "POST":
       username = request.POST.get("username")
       first_name = request.POST.get("firstname")
       last_name = request.POST.get("lastname")
       email = request.POST.get("email")
       password = request.POST.get("password")
       
       user = User.objects.create_user(username=username,
                                password=password, first_name=first_name, last_name=last_name, email=email)
       login(request, user)
       return redirect('index')
       
    return render(request, 'utilisateurs/user.html')
 
def logout_user(request):
    logout(request)
    return redirect('index')
