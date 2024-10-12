from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Member  # Make sure to import the Member model
from .models import District, Role, Announcement, Gallery, Contact, Event


class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'})
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'})
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Styling the form fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'User Name'
        })

        # Styling additional fields
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'




class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),
        required=False
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
        required=False
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Styling the form fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'User Name'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

        # Styling additional fields
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'


class MemberForm(forms.ModelForm):
    user = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
        required=False
    )
    first_name = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=False
    )
    last_name = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=False
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control, width: auto'}),
        required=False
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control, width: auto'}),
        required=False
    )
    email = forms.EmailField(
        label='', 
        required=False, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
    )
    phone = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        required=False
    )
    address = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
        required=False
    )
    date_of_birth = forms.DateField(
        label='', 
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        required=False
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    dads_name = forms.CharField(
        label='', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"})
    )
    moms_name = forms.CharField(
        label='', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's Name"})
    )
    dads_phone = forms.CharField(
        label='', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Phone"})
    )
    moms_phone = forms.CharField(
        label='', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's Phone"})
    )
    
    class Meta:
        model = Member
        fields = [
             'first_name', 'last_name', 'district', 'role', 'email', 'phone', 'address', 
            'date_of_birth', 'profile_picture', 'dads_name', 'moms_name', 'dads_phone', 'moms_phone'
        ]

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'image', 'date', 'display_on_home']
        
        # Customizing the form widgets for the fields
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(attrs={'class': 'filled', 'rows': 3, 'cols': 40}),
            'image': forms.ClearableFileInput(attrs={'class': 'filled'}),
            'date': forms.DateInput(attrs={'class': 'filled', 'type': 'date'}),
            'display_on_home': forms.CheckboxInput(attrs={'class': 'filled'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'location', 'description', 'image', 'display_on_home']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter event title'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'input-field'}),
            'location': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Event location'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Enter event description'}),
            'image': forms.FileInput(attrs={'class': 'input-field'}),
            'display_on_home': forms.CheckboxInput(attrs={'class': 'filled'}),
        }


from django import forms
from .models import Gallery

# Custom widget to allow multiple file uploads
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class GalleryForm(forms.ModelForm):

    district = forms.ModelChoiceField(
        queryset=District.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control, width: auto'}),
        required=False
    )

    class Meta:
        model = Gallery
        fields = ['title', 'district', 'description']

class GalleryFileForm(forms.Form):
    file = MultipleFileField(label='Select files', required=False)
