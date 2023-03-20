
from IPython.core.display import display, HTML
from typing import List,Tuple
import json
import os


comp_template = '''<div class = "graphic" style = "margin:auto;width:80vw;height:{}vw;position:relative">
    {}      
</div>'''

def svg_to_component(svg:str):
    w,h = get_size(svg)
    h = h/w *80
    return comp_template.format(str(h),svg)

def get_size(comp):
    viewbox_content = comp[comp.find("viewBox")+9:]
    viewbox_content = viewbox_content[:viewbox_content.find("\"")]
    _,_,w,h=map(float,viewbox_content.split(' '))
    return w,h

def component_to_html(comp:str):

    f=open('./templates/view_template.html')
    view_template = f.read()
    f.close()

    html = view_template.replace("{}",comp)
    return html

def extract_vectorimage(path:str):
    f = open(path,'r')
    lines = f.readlines()
    f.close()
    paths = filter(lambda line:line[:4]in ['<pat','<svg','</sv'],lines)
    clean = ''.join(paths)
    viewbox_content = filter(lambda line:line.find("viewBox")>0,lines).__next__()
    viewbox_content = viewbox_content[viewbox_content.find("viewBox")+9:]
    viewbox_content = viewbox_content[:viewbox_content.find("\"")]
    _,_,w,h=map(float,viewbox_content.split(' '))
    return clean

def browse_html(html,path):
    path = "views/"+path
    f = open (path,'w')
    f.write(html)
    f.close()
    print(f"view file://{os.path.abspath(path)} in browser")


def view_questions (*qs,path='index.html'):
    f = open('templates/question_div.html')
    qtemp = f.read()
    f.close()

    content = []
    for i,q in enumerate(qs):
        id = f'_id{i}_'
        data = q.dumps()
        data = json.dumps(data)
        content.append(qtemp.replace("_id_",id).replace("{}",data))

    view_components(*content,path = path)


def formatter(template):
    return lambda *x:template.format(*x)


def tabl(w,h,*content):
    content = "\n".join(content)
    return "<br><div class=table style=\"width:{}em;height:{}em\" >{}</div><br>".format(w,h,content)

trow = formatter("<div class=row >{}</div>\n")
telm = formatter("<div>{}</div>")
empty =telm("")
underline ="<div class = underline></div>\n"
inpt = "<div><input></div>"
mini_red = formatter("<div class=\"mini row\">{}</div>\n")

def htg(cont):return formatter("<{}>{{}}</{}>".format(cont,cont))

h3 = htg("h3")
p = htg("p")
span = htg('span')
div = htg("div")

def mkrow (a,style = ""):
    style += " row"
    res = ""
    for c in a:
        res += telm(c) 
    return "<div class=\"row {}\">{}</div>".format(style,res)

def mktabl(w,h,*a):
    res =""
    for l in a:
        res += mkrow(l)
    return tabl(res)

def view_components(*comps,path='index.html'):
    html = component_to_html(''.join(comps))
    browse_html(html,path)
