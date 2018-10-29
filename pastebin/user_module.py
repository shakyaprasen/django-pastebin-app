from django.http import HttpResponseRedirect
from django.urls import reverse, resolve
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.core.validators import validate_email


LOGINERROR = 50
#login function
def authenticateUser(request):
    current_path = request.build_absolute_uri()

    if 'username' not in request.POST:
        messages.add_message(request, LOGINERROR, 'No user specified')
        return HttpResponseRedirect(reverse('pastebin:NewPost',))
        
    else:
        user_name = request.POST['username']
        passwrd = request.POST['password']
        user = authenticate(request, username=user_name, password=passwrd)
        logged_in = loginFunction(request, user)

        if logged_in:
            return HttpResponseRedirect(reverse('pastebin:NewPost',))
        else:
            messages.add_message(request, LOGINERROR, 'Error in login, wrong username or password')
            return HttpResponseRedirect(reverse('pastebin:NewPost',))
            # return render(request, current_path, {
            #         'login_error_message': "Error in login",
            #     })

def loginFunction(request, user):

    if user is not None:
        request.session['current_user'] = user.username
        request.session['user_id'] = user.id
        login(request, user)
        return True
    else:
        return False


def saveNewUser(request):
        
    try:  
        validate_email(request.POST['email'])
        passValidator(request.POST['password'], 'password')
        nameValidator(request.POST['firstname'], 'firstname')
        nameValidator(request.POST['lastname'], 'lastname')
    except Exception as e:
        return render(request, 'pastebin/newUser.html', {
                'error_message': "Error in Validating Data, , Error Info:: " + str(e),
            })

    try:
        user_name = request.POST['username']
        passwrd = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        user = User.objects.create_user(username=user_name, password=passwrd, first_name=firstname, last_name=lastname, email=email, last_login=timezone.now())
        user.save()
    except Exception as e:
        return render(request, 'pastebin/newUser.html', {
                'error_message': "Error in Saving new User, Error Info:" + str(e),
            })

    logged_in = loginFunction(request, user)

    if logged_in:
        return HttpResponseRedirect(reverse('pastebin:NewPost',)) 

    else:
        messages.add_message(request, LOGINERROR, 'Error in login')
        return HttpResponseRedirect(reverse('pastebin:NewPost',))


def logOutUser(request):
    if 'user_id' in request.session:
        del request.session['current_user']
        del request.session['user_id']

    logout(request)
    return HttpResponseRedirect(reverse('pastebin:NewPost',)) 


def nameValidator(value, fieldname, constraint_length = 10):
    if (any(char.isdigit() for char in value)) :
        raise Exception('Field: %s should contain no numbers' % fieldname)
    elif len(value) > constraint_length:
        raise Exception('Field: %s should be shorter than %d characters' % (fieldname, constraint_length)) 
    else:
        return value

def passValidator(value, fieldname, constraint_length = 5):
    if len(value) < constraint_length:
        raise Exception('Field: %s should be longer than %d characters' % (fieldname, constraint_length)) 
    else:
        return value
