from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
def verified_dairy_user(fun):
    """
    this decorator checks if the user is verified dairy owner or not if
    not this will raise forbidden error
    """
    def inner(request,*args,**kwargs):
        print("hey i am called man")
        if request.user.has_verified_dairy:
            return fun(request,*args,**kwargs)
        else:
            raise PermissionDenied('sorry,wait for to be verified dairy owner')
    return inner

# def verified_dairy_user(view_method):
#     @method_decorator
#     def inner(cls, *args, **kwargs):
#         print("hey i am called man")
#         if args[1].user.has_verified_dairy:
#             return view_method(cls, *args, **kwargs)
#         else:
#             raise PermissionDenied('Sorry, you need to be a verified dairy owner')
#     return inner