from django import template
from prs.models import College
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    recentPrsFile=f'{college_slug}_recentrPRs.json'
    import json  
    f = open(recentPrsFile)
    prsJson = json.load(f)
    f.close()
    html=''
    for eachMeet in prsJson:
        html+=f'''
        <div class = "justify-content-center d-inline-block">
			<div class = "text-center">
			<h2 class="col-12 display-4 custom-header p-2 rounded">{eachMeet['meetname']}</h2>
			<h3>{eachMeet['meetdate']}</h3>
			<h5>{eachMeet['numberofprs']} total pr's | {eachMeet['uniqueprs']} people pr'd</h5>
			</div>
		</div>
        <div class="container d-inline-block">
				<ul class = "list-unstyled justify-content-center">'''
        for eachPR in eachMeet['prsatmeet']:
            html+=f'<li class="custom-pr-li w-fit rounded shadow">{eachPR["athletename"]} set a pr of {eachPR["pr"]} in {eachPR["eventname"]}</li>'
        html+='''</ul>
            </div>
            '''
    return mark_safe(html)


# return render(request, 'prs/recentPRs.html', {'data':data})

# <div class = "d-flex justify-content-center">
# <h1 class="p-2 m-3 content w-fit rounded">Most Recent PR's</h1>
# </div>
