
from IPython.core.display import display, HTML
from typing import List,Tuple
import json
import os


f=open('./view_template.html')
view_template = f.read()
f.close()

f = open("./question_template.html")
question_template = f.read()
f.close

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
    f = open (path,'w')
    f.write(html)
    f.close()
    print(f"view file://{os.path.abspath(path)} in browser")
    

def view_component(comp):
    html = component_to_html(comp)
    browse_html(html,'index.html')

def view_question(q):

    data = json.dumps(q)
    data = json.dumps(data)
    html = question_template.replace("{}",data)
    f = open ("question.html",'w')
    f.write(html)
    f.close()

    print(f"view file://{os.path.abspath('question.html')} in browser")
    