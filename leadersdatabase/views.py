from django.shortcuts import render
from .models import resource, camp_sites, resources_files, camp_sites_files


def resources(request):
    resources = resource.objects.all()
    return render(request, 'resource_list.html', {'resources': resources})


def camp_sites(request):
    camp_sites = camp_sites.objects.all()
    return render(request, 'camp_sites_list.html', {'camp_sites': camp_sites})

def resource_detail(request, pk):
    Resource = resource.objects.get(pk=pk)
    return render(request, 'resource_detail.html', {'resource': Resource})

def camp_site_detail(request, pk):
    camp_site = camp_sites.objects.get(pk=pk)
    return render(request, 'camp_site_detail.html', {'camp_site': camp_site})


