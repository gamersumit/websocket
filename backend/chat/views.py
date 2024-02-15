from django.shortcuts import render
from .models import Chat, Group
from django.http import JsonResponse
# Create your views here.
def create_group(request, groupname):
    group = Group.objects.filter(name = groupname).first()
    chats = []
    if group:
        chats = [obj.content for obj in Chat.objects.filter(group = group)]
    else :
        group = Group(name = groupname)
        group.save()
    
    
    return JsonResponse({'status': True, 'chats': chats, 'group' : groupname}, status=200)