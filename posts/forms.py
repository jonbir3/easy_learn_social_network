from django import forms
from posts.models import Post, Comments
from users.models import Course

OTHER_CATEGORY = 'other'


class NewPost(forms.ModelForm):
    CATEGORY_CHOICES = (
        (OTHER_CATEGORY, 'Other'),
    )
    COURSES = ()
    try:
        COURSES = tuple(map(lambda course_name: (course_name, course_name), Course.objects.only('course_name')))
    except Exception as e:
        print(e)
    category_list = CATEGORY_CHOICES + COURSES
    category_rules = 'By selecting the "Other" option, only your friends can view the post. ' \
                     'Otherwise the post will be set to public.'

    category = forms.ChoiceField(help_text=category_rules, choices=category_list)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('category', 'body',)


class Comment(forms.ModelForm):
    comment = forms.CharField(max_length=250,
                              widget=forms.TextInput(attrs={'placeholder': 'write comment...'}),
                              help_text='Please write your comment (maximum 250 characters)')

    class Meta:
        model = Comments
        fields = ('comment', )
