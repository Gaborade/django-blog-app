from django import forms
from .models import Comment


# Django has two Form base classes, forms.Form and forms.ModelForm
# forms.Form are to create independent form models
# forms.ModelForm are to create forms dynamically from other classes in model.py

class EmailPostForm(forms.Form):
    """A form to send emails of posts"""
    # forms.CharField is rendered as <input type="text"> HTML element.
    # every form field has a default widget.
    name = forms.CharField(max_length=25)
    # if an email isn't typed in this field an forms.ValidationError will occur 
    # and form will not validate
    email = forms.EmailField()
    to = forms.EmailField()
    # we overrided comments CharField form to rather be a like a TextArea
    # we make comments field optional by making required=False
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """A  dynamic form to handle comments of blog posts"""

    class Meta:
        # to create a form from the model, you indicate the model you want to use in the class Meta
        # by default Django uses all the model fields for the Form fields unless you explictly define
        # the fields list attribute shows which fields to add,
        # an exclude attribute shows the lists of fields to exclude from the CommentForm fields
        model = Comment
        fields = ('name', 'email', 'body')



    