from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Project, ProjectImage, User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True)
    student_id = forms.CharField(max_length=30, required=False)
    course = forms.CharField(max_length=100, required=False)
    year_level = forms.IntegerField(min_value=1, max_value=8, required=False)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'student_id', 'course', 'year_level', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.student_id = self.cleaned_data.get('student_id', '')
        user.course = self.cleaned_data.get('course', '')
        user.year_level = self.cleaned_data.get('year_level', 1)
        user.email_verified = False
        user.is_active = False
        if commit:
            user.save()
        return user


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'summary',
            'description',
            'category',
            'technologies',
            'featured_image',
            'demo_url',
            'source_url',
        )
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 8}),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ('image', 'caption')
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Optional caption'}),
        }


class ProjectImageUploadForm(forms.Form):
    image = forms.ImageField(required=True)
    caption = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional caption'}))
