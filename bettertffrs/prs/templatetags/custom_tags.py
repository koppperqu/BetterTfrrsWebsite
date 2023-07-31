from django import template
from prs.models import College
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent


register = template.Library()

@register.simple_tag
def college_links():
    colleges = College.objects.all()
    slugs=[]
    for college in colleges:
        slug = slugify(college.college_name)
        slugs.append(slug)
    links = ''
    for college in colleges:
        url = reverse('college', kwargs={'college_slug': slugify(college.college_name)})
        link = f'<li class="nav-item"><a class="nav-link" href="{url}">{college.college_name}</a></li>'
        links += link
    return mark_safe(links)

@register.simple_tag
def most_recent_prs(college_slug):
    recentPrsFile=BASE_DIR / f'{college_slug}_recentrPRs.json'
    import json  
    f = open(recentPrsFile)
    prsJson = json.load(f)
    f.close()
    html=''
    for eachMeet in prsJson:
        html+=f'''
        <div class = "justify-content-center">
			<div class = "text-center content">
			<h2 class="custom-header p-2 mt-2 rounded">{eachMeet['meetname']}</h2>
			<h3>{eachMeet['meetdate']}</h3>
			<h5 class="pb-3">{eachMeet['numberofprs']} total pr's | {eachMeet['uniqueprs']} people pr'd</h5>
			</div>
		</div>
        <div class="justify-content-center container">
				<p class = "fs-5">'''
        for eachPR in eachMeet['prsatmeet']:
            html+=f'{eachPR["athletename"]} set a pr of {eachPR["pr"]} in {eachPR["eventname"]}<br>'
        html+='</div>'
    if(html==''):
        html='''
            <h1>No Recent PRs<h1>
            <p class="fs-4 px-4">There have been no recent prs in the last two meets please feel free to look at the prs sorted by event or athlete by using the links above!</p>
            '''
    return mark_safe(html)
