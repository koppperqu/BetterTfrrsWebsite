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
    html='<div class="content w-fit rounded">'
    for eachMeet in prsJson:
        html+=f'''
        <div class = "d-flex justify-content-center">
			<div class = "text-center myls w-fit">
			<h2>{eachMeet['meetname']}</h2>
			<h3>{eachMeet['meetdate']}</h3>
			<h5>{eachMeet['numberofprs']} total prs <br> {eachMeet['uniqueprs']} people pr'd</h5>
			<h4>PRs</h4>
			</div>
		</div>
        <div class="container">
				<ul class = "list-unstyled d-flex justify-content-center align-content-start flex-wrap">'''
        for eachPR in eachMeet['prsatmeet']:
            html+=f'<li class="rounded shadow" id = "listItem">{eachPR["athletename"]} set a pr of {eachPR["pr"]} in {eachPR["eventname"]}</li>'
        html+='''</ul>
            </div>
            '''
    html+='</div>'
    return mark_safe(html)


# return render(request, 'prs/recentPRs.html', {'data':data})

# <div class = "d-flex justify-content-center">
# <h1 class="p-2 m-3 content w-fit rounded">Most Recent PR's</h1>
# </div>
