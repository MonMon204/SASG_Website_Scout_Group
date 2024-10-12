from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Member, District
from django.contrib.auth.models import User

# This signal will only update the count when a new member is created
@receiver(post_save, sender=Member)
def update_district_members_count(sender, instance, created, **kwargs):
    if created:  # Only run this logic when a new member is created
        if instance.district is None:  # If the member is not assigned to a district
            return
        district = instance.district
        if instance.position == 'قائد':  # If position is 'Leader'
            district.leaders_count += 1
        elif instance.position == 'فرد':  # If position is 'Member'
            district.members_count += 1
        district.save()

# This signal will decrease the count when a member is deleted
@receiver(post_delete, sender=Member)
def decrease_district_members_count(sender, instance, **kwargs):
    if instance.district is None:  # If the member is not assigned to a district
            return
    district = instance.district
    if instance.position == 'قائد':  # If position is 'Leader'
        district.leaders_count -= 1
    elif instance.position == 'فرد':  # If position is 'Member'
        district.members_count -= 1
    district.save()


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Member, District, Leader

# Signal to handle member creation and leader creation
@receiver(post_save, sender=Member)
def create_leader_if_position_is_leader(sender, instance, created, **kwargs):
    if created and instance.position == 'قائد':  # Check if the member is a new 'قائد'
        # Create the Leader object automatically
        Leader.objects.create(
            first_name=instance.first_name,
            last_name=instance.last_name,
            district=instance.district
        )
        # Update district count
        district = instance.district
        district.leaders_count += 1
        district.save()
    elif created:
        # Update the member count for non-leader positions
        district = instance.district
        if district is None:
            return
        district.members_count += 1
        district.save()

# Signal to handle member deletion and leader deletion
@receiver(post_delete, sender=Member)
def delete_leader_if_position_is_leader(sender, instance, **kwargs):
    if instance.position == 'قائد':
        # Delete the Leader object if the member was a 'قائد'
        Leader.objects.filter(first_name=instance.first_name, last_name=instance.last_name, district=instance.district).delete()

        # Decrease leader count
        district = instance.district
        district.leaders_count -= 1
        district.save()
    else:
        # Decrease member count for non-leader positions
        district = instance.district
        if district is None:
            return
        district.members_count -= 1
        district.save()


