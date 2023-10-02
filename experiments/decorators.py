from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from users.models import User_Group
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
def group_required(view_func):
    """
    Custom decorator to check if the user belongs to a specific group.
    Usage: @group_required('group_name')
    """


    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this page.")

        # Check if the user belongs to the specified group
        try:
            group = User_Group.objects.get(user=request.user.id)
        except:
            group = None

        if group:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/accounts/me')
    return _wrapped_view

