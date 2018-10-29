from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from .models import POST, URL
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import short_url, os
from django.contrib.messages import get_messages
from django.db import transaction
from pathlib import Path

MYPATH = Path().absolute()

FILEPATH = str(MYPATH) + '/pastebin/pastebin_files/'
# Create your views here.

class NewPostView(generic.ListView):
    model = POST
    template_name = 'pastebin/newpostview.html'

class DisplayAllPostView(generic.ListView):
    template_name = 'pastebin/listallposts.html'
    context_object_name = 'list_object'
    model = POST
    def get_queryset(self):
        current_user_id = self.request.session.get('user_id', 0)
        if current_user_id > 0:
            return POST.objects.raw('SELECT post.id, post.file_path, post.title, post.user_id, url.id AS url_id, url.short_url  FROM pastebin_post AS post INNER JOIN pastebin_url AS url ON post.id = url.post_id WHERE user_id = %s ', [current_user_id])
            

@transaction.atomic
def savePost(request, post_id=0):
    sid = transaction.savepoint()
    if post_id==0:
        try:
            newpost = POST(post_info = request.POST['post_info'], entry_date = timezone.now())
            current_user_id = request.session.get('user_id', 0)
            if current_user_id > 0:
                newpost.user_id = current_user_id

            newpost.save()
            new_url = short_url.encode_url(newpost.id)
            file_path = newFile(current_user_id, new_url, newpost.post_info)
            POST.objects.filter(id = newpost.id).update(file_path = file_path)
            selected_url = newpost.url_set.create(short_url=new_url)
            
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return render(request, 'pastebin/newpostview.html', {
                'error_message': 'Error in saving this entry, Error Info:' + str(e),
                })
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('pastebin:DisplayPost', args=(new_url,)))
    else:
        try:
            old_post = get_object_or_404(POST, pk=post_id)
            old_post.post_info = request.POST['post_info']
            old_post.last_updated = True
            old_post.post_update = timezone.now()
            update_file = updateFile(old_post.file_path, request.POST['post_info'])
            old_post.save()
            
        except (KeyError, POST.DoesNotExist):
            transaction.savepoint_rollback(sid)
            return render(request, 'pastebin/newpostview.html', {
                'post_object': old_post,
                'error_message': "Error in fetchin/updating post",
            })
        old_url = short_url.encode_url(old_post.id)
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('pastebin:DisplayPost', args=(old_url,))) 

def displayPost(request, url):
    post_id = short_url.decode_url(url)
    try:
        p = get_object_or_404(POST, id = post_id)
        p.info_from_file = readFile(p.file_path)
    except (KeyError, POST.DoesNotExist):
        return render(request, 'pastebin/newpostview.html', {
            'error_message': "Error in fetchin/updating post",
        })

    return render(request, 'pastebin/newpostview.html', {
            'post_object' : p
            })

#new User Registration View
def NewUserView(request):
    return render(request, 'pastebin/newUser.html', )

#function to make a new file
#write the textarea into a .txt file
#takes the converted shortened url as a filename and the textarea text as the input
def newFile(user_id, filename, text):
    if user_id > 0:
        if not os.path.isdir(FILEPATH + str(user_id)):
            os.makedirs(FILEPATH + str(user_id))
        full_filename = FILEPATH + str(user_id) + '/' + filename + '.txt'
    else:
        full_filename = FILEPATH + str(filename) + '.txt' 

    if text is not None:
        try:
            f = open(full_filename, 'w+')
            f.write(text)
            f.close()
        except Exception as e:
            raise Exception(str(e))

    return full_filename

#function to update the file content
def updateFile(fullpath, text):

    if text is not None:
        try:
            f = open(fullpath, 'w+')
            f.write(text)
            f.close()
        except Exception as e:
            raise Exception(str(e))

    return fullpath

#function to read file and return the post/text
def readFile(fullpath):
    f = open(fullpath, 'r')
    post = f.read()
    f.close()

    return post