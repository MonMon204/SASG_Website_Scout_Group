from django.shortcuts import render, redirect
from .models import District, Member, Event, Announcement, Gallery, Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, MemberForm, AnnouncementForm, EventForm, GalleryForm
from django import forms

from badges.models import Badge, BadgeTerm, GradeAttachment, BadgeGradingSystem, BadgeApproval



def home(request):
    announcements = Announcement.objects.all()
    events = Event.objects.all()
    galleries = Gallery.objects.prefetch_related('files').order_by('-id').all()  # Prefetch related files for performance

    return render(request, 'home.html', {'announcements': announcements, 'events': events, 'galleries': galleries})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in'))
            return redirect('home')
        else:
            messages.error(request, ('Error logging in - Please try again'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Member

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)

            login(request, user)
            messages.success(request, ('You have been Registered Successfully'))
            return redirect('registerinfo')
        else:
            messages.error(request, ('Error Registering !! - Please try again'))
            
        
    else:
        return render(request, 'register.html', {'form': form})


def register_user_info(request):
    if request.user.is_authenticated:
        current_user = Member.objects.get(user=request.user)
        form = MemberForm(request.POST or None, request.FILES or None, instance=current_user)
        if form.is_valid():
            form.save()

            # login(request, current_user)
            messages.success(request, ('User Information Updated'))
            return redirect('home')
        
        return render(request, 'registerinfo.html', {'form': form})
    else:
        messages.error(request, ('Please login first'))
        return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        current_user = Member.objects.get(user=request.user)
        his_district = current_user.district
        his_role = current_user.role
        his_badges = BadgeApproval.objects.filter(member=current_user).filter(display_on_his_account=True).filter(passed=True).all()
        return render(request, 'profile.html', {'current_user': current_user, 'his_district': his_district, 'his_role': his_role, 'his_badges': his_badges})
    else:
        messages.error(request, ('Please login first'))
        return redirect('login')


def add_announcement(request):
    current_user = Member.objects.get(user=request.user)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form.cleaned_data['display_on_home']:
                messages.success(request, 'Announcement added successfully!')
            else:
                messages.success(request, 'Announcement added successfully! Contact a leader to display the announcement on the home page.')
                
            return redirect('home')  # Redirect to home or any other relevant page
        else:
            messages.error(request, 'Error adding announcement.')
    else:
        form = AnnouncementForm()
    
    return render(request, 'add_announcement.html', {'form': form, 'current_user': current_user})


def add_event(request):
    current_user = Member.objects.get(user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form.cleaned_data['display_on_home']:
                messages.success(request, 'Event added successfully!')
            else:
                messages.success(request, 'Event added successfully! Contact a leader to display the event on the home page.')
            return redirect('home')  
        else:
            messages.error(request, 'Error adding event.')
    else:
        form = EventForm()
    
    return render(request, 'add_event.html', {'form': form, 'current_user': current_user})


from django.shortcuts import render, redirect
from .forms import GalleryForm, GalleryFileForm
from .models import Gallery, GalleryFile
from django.contrib import messages

def add_gallery(request):
    if request.method == 'POST':
        gallery_form = GalleryForm(request.POST)
        gallery_file_form = GalleryFileForm(request.POST, request.FILES)

        if gallery_form.is_valid() and gallery_file_form.is_valid():
            title = gallery_form.cleaned_data['title']
            district = gallery_form.cleaned_data['district']
            description = gallery_form.cleaned_data['description']

            # Create the gallery instance
            gallery = Gallery(
                title=title,
                district=district,
                description=description,
            )
            gallery.save()  # Save the gallery object first

            # Handle multiple file uploads
            uploaded_files = request.FILES.getlist('file')
            for uploaded_file in uploaded_files:
                # Create a GalleryFile instance for each uploaded file
                gallery_file = GalleryFile(
                    gallery=gallery,  # Link the file to the created gallery
                    file=uploaded_file
                )

                # Determine file type before saving
                if uploaded_file.name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico', '.webp')):
                    gallery_file.file_type = 'image'
                elif uploaded_file.name.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm')):
                    gallery_file.file_type = 'video'
                else:
                    gallery_file.file_type = 'other'

                gallery_file.save()  # Save the file

            messages.success(request, 'Gallery added successfully!')
            return redirect('home')  # Redirect after successfully saving

    else:
        gallery_form = GalleryForm()
        gallery_file_form = GalleryFileForm()

    return render(request, 'add_gallery.html', {
        'gallery_form': gallery_form,
        'gallery_file_form': gallery_file_form
    })


from django.shortcuts import render
from .models import Gallery, District  # Assuming you have these models

def gallery_view(request):
    # Get all districts and galleries
    districts = District.objects.all()
    galleries = Gallery.objects.prefetch_related('files').order_by('-id').all()

    # Render the template with context data
    context = {
        'districts': districts,
        'galleries': galleries
    }
    return render(request, 'gallery.html', context)


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import District, Member

# views.py

def my_district(request):
    districts = District.objects.all()
    selected_district = request.GET.get('district')  # Get the district ID from the query parameters
    members = None

    if selected_district:
        # Filter members based on selected district ID
        members = Member.objects.filter(district_id=selected_district)

    return render(request, 'my_district.html', {
        'districts': districts,
        'selected_district': selected_district,  # This is now an ID
        'members': members,
    })

