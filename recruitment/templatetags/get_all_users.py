from django import template
from django.template.base import Node,TemplateSyntaxError
from django.contrib.auth.models import User

register = template.Library()

class GetAllUsers(Node):
    def __init__(self, varname):
        # Save the variable that we will assigning the users to
        self.varname = varname
def render(self, context):
        # Save all the user objects to the variable and return the context to the template
        context[self.varname] = User.objects.all()
        return ''

@register.tag(name="get_all_users") 
def get_all_users(parser, token):
    # First break up the arguments that have been passed to the template tag
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_all_users tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "1st argument to get_all_users tag must be 'as'"
    return GetAllUsers(bits[2])
