from rest_framework import permissions
from .models import Modelnames

class Read(permissions.BasePermission):
    def has_permission(self,request,view):
        return  request.user.read_P

class Write(permissions.BasePermission):
    def has_permission(self,request,view):
        return  request.user.write_P
    
class User1(permissions.BasePermission):
    def has_permission(self,request,view):
        return  request.user.user1
    
class User2(permissions.BasePermission):
    def has_permission(self,request,view):
        return  request.user.user2
    
    
class No (permissions.BasePermission):
    def has_permission(self,request,view):
        return  False