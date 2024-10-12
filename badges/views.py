from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Badge, BadgeTerm, GradeAttachment, BadgeGradingSystem
from django.shortcuts import get_object_or_404
from web.models import Member

def badges_home(request):
    badges = Badge.objects.all()
    return render(request, 'badges.html', {'badges': badges})


def badge_details(request, id):
    badge = get_object_or_404(Badge, id=id)  # Assuming Badge is your model name
    return render(request, 'badge_details.html', {'badge': badge})


def badge_term_detail(request, badge_id, term_id):
    badge = Badge.objects.get(id=badge_id)
    term = BadgeTerm.objects.get(id=term_id)
    attachments = GradeAttachment.objects.filter(badge_term=term)
    return render(request, 'badge_term_detail.html', {'badge': badge, 'term': term, 'attachments': attachments})

def apply_badge(request, badge_id):
    if request.method == 'POST':
        badge = get_object_or_404(Badge, id=badge_id)
        current_user = request.user  # Assuming you have the current user in the request
        member = get_object_or_404(Member, user=current_user)  # Replace with your method to get the member instance
        badge_terms = BadgeTerm.objects.filter(badge=badge)

        # Create a BadgeGradingSystem entry for each badge term
        for term in badge_terms:
            BadgeGradingSystem.objects.create(
                member=member,
                badge=badge,
                badge_term=term,
                passed=False
            )
        
        return redirect('home')

    

# views.py
from django.shortcuts import render, redirect
from .forms import MemberBadgeSelectionForm
from .models import  Badge, BadgeTerm
from web.models import Member

def badge_grading(request):
    # Ensure only leaders ('قائد') can access the page
    current_user = Member.objects.get(user=request.user)
    if  current_user.role.name != 'قائد':
        messages.error(request, ('You are not authorized to access this page'))
        return redirect('home')

    if request.method == 'POST':
        form = MemberBadgeSelectionForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            badge = form.cleaned_data['badge']
            return redirect('badge_grading_details', member_id=member.id, badge_id=badge.id)
    else:
        form = MemberBadgeSelectionForm()

    return render(request, 'badge_grading.html', {'form': form})


from django.core.files.storage import FileSystemStorage
from .models import BadgeTerm, GradeAttachment
from .forms import BadgeGradingForm

def badge_grading_details(request, member_id, badge_id):
    # Ensure only leaders ('قائد') can access the page
    current_user = Member.objects.get(user=request.user)
    if  current_user.role.name != 'قائد':
        messages.error(request, ('You are not authorized to access this page'))
        return redirect('home')

    member = Member.objects.get(id=member_id)
    badge = Badge.objects.get(id=badge_id)
    badge_terms = BadgeTerm.objects.filter(badge=badge)

    graded_terms = {}
    for term in badge_terms:
        grading_system = BadgeGradingSystem.objects.filter(member=member, badge_term=term).first()
        if grading_system and grading_system.grade_attachment:
            graded_terms[term.id] = {
                'grade': grading_system.grade_attachment.grade,
                'description': grading_system.grade_attachment.description,
                'file': grading_system.grade_attachment.file,
                'passed': grading_system.passed,
            }
        else:
            graded_terms[term.id] = {
                'grade': '',
                'description': '',
                'file': None,
                'passed': False,
            }

    if request.method == 'POST':
        form = BadgeGradingForm(request.POST, request.FILES, badge_terms=badge_terms, graded_terms=graded_terms)
        if form.is_valid():
            form.save_grades(member, badge, badge_terms)
            return redirect('home')
    else:
        form = BadgeGradingForm(badge_terms=badge_terms, graded_terms=graded_terms)

    return render(request, 'badge_grading_details.html', {
        'member': member,
        'badge': badge,
        'badge_terms': badge_terms,
        'form': form,
        'form_fields': [
            {
                'term': term,
                'grade': form[f'grade_{term.id}'],
                'file': form[f'file_{term.id}'],
                'description': form[f'description_{term.id}'],
                'passed': form[f'passed_{term.id}'],
            }
            for term in badge_terms
        ],
    })