from django import forms
from .models import Badge, BadgeGradingSystem
from web.models import Member

class MemberBadgeSelectionForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.none(), label="Select Member")
    badge = forms.ModelChoiceField(queryset=Badge.objects.none(), label="Select Badge")

    def __init__(self, *args, **kwargs):
        super(MemberBadgeSelectionForm, self).__init__(*args, **kwargs)
        
        # Get members who have applied for any badges
        self.fields['member'].queryset = Member.objects.filter(grading_system__isnull=False).distinct()

        if 'member' in self.data:
            try:
                member_id = int(self.data.get('member'))
                member = Member.objects.get(id=member_id)

                # Get badges the member has applied for but hasn't passed yet
                applied_badges = BadgeGradingSystem.objects.filter(member=member).values_list('badge', flat=True)
                
                # Dynamically update badge queryset to show only applied badges
                self.fields['badge'].queryset = Badge.objects.filter(id__in=applied_badges)

            except (ValueError, TypeError, Member.DoesNotExist):
                self.fields['badge'].queryset = Badge.objects.none()
        elif self.initial.get('member'):
            member = self.initial.get('member')
            
            # Prepopulate badge queryset with the member's applied badges that are not yet passed
            applied_badges = BadgeGradingSystem.objects.filter(member=member).values_list('badge', flat=True)
            self.fields['badge'].queryset = Badge.objects.filter(id__in=applied_badges)


from django import forms
from .models import BadgeTerm, GradeAttachment, BadgeGradingSystem, Badge, BadgeApproval

class BadgeGradingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        badge_terms = kwargs.pop('badge_terms', None)
        graded_terms = kwargs.pop('graded_terms', None)
        super(BadgeGradingForm, self).__init__(*args, **kwargs)

        if badge_terms:
            for term in badge_terms:
                # Add grade input
                self.fields[f'grade_{term.id}'] = forms.CharField(
                    label=f"Grade for {term.term}",
                    required=False,
                    initial=graded_terms.get(term.id, {}).get('grade', '')
                )
                # Add file input
                self.fields[f'file_{term.id}'] = forms.FileField(
                    label=f"File for {term.term}",
                    required=False
                )
                # Prepopulate existing file
                if graded_terms.get(term.id, {}).get('file'):
                    self.fields[f'file_{term.id}'].initial = graded_terms[term.id]['file']
                
                # Add description input
                self.fields[f'description_{term.id}'] = forms.CharField(
                    label=f"Description for {term.term}",
                    widget=forms.Textarea,
                    required=False,
                    initial=graded_terms.get(term.id, {}).get('description', '')
                )
                # Add passed checkbox
                self.fields[f'passed_{term.id}'] = forms.BooleanField(
                    label=f"Passed for {term.term}",
                    required=False,
                    initial=graded_terms.get(term.id, {}).get('passed', False)
                )
    
    def save_grades(self, member, badge, badge_terms):
        """
        Saves the grades for each badge term. This method processes the form data
        and saves it to the BadgeGradingSystem and GradeAttachment models.
        """
        for term in badge_terms:
            term_id = term.id
            grade = self.cleaned_data.get(f'grade_{term_id}')
            file = self.cleaned_data.get(f'file_{term_id}')
            description = self.cleaned_data.get(f'description_{term_id}')
            passed = self.cleaned_data.get(f'passed_{term_id}', False)

            # Get or create the BadgeGradingSystem entry for this term
            grading_system, created = BadgeGradingSystem.objects.get_or_create(
                member=member,
                badge=badge,
                badge_term=term,
                defaults={'passed': passed}
            )

            # If grade exists, save/update GradeAttachment
            if grade or file or description:
                # Create or get the existing GradeAttachment for this term
                grade_attachment, _ = GradeAttachment.objects.get_or_create(
                    badge_term=term
                )

                # Only update the file if a new one is uploaded
                if file:
                    grade_attachment.file = file
                
                grade_attachment.grade = grade
                grade_attachment.description = description
                grade_attachment.save()

                # Link the grading_system to the grade_attachment
                grading_system.grade_attachment = grade_attachment
            else:
                # Retain the existing grade_attachment if no new file/description/grade
                grading_system.grade_attachment = grading_system.grade_attachment

            # Update the 'passed' status in the BadgeGradingSystem
            grading_system.passed = passed
            grading_system.save()
