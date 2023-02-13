
from IPython.core.display import display, HTML
from typing import List,Tuple
import json
import os

html_template = ['''
<body>
    <div class = mycomps>
    ''','''
    </div>

</body>
</html>

<style>
    .mycomps{
        color:black;
        background-color: #fff8;
        --color:aliceblue;
        text-align:center;
        font-size:1.2em;
    }

    input{
        all:unset;
        background:white;
        text-align:left;
        font-size:1em;
        font-family:monospace;
    }
    svg{
        position: absolute;
        top:0px;
        left:0px;
    }
    .field{
        top:40%;
        left:60%;
        position: inherit;
        border:unset;
        width:2em;
    }
    table, tr, th{
        border:1px solid black;
    }

</style>''']


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



    html = html_template[0] + comp+html_template[1]
    
    comp.join(html_template)
    return html


"sldkfj".startswith("sld")


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


def export_component(name,content):
    f = open('./visual_components/'+name+'.comp','w')
    f.write(content)
    f.close()

def import_component(name):
    f = open('./visual_components/'+name+'.comp','r')
    res = f.read()
    f.close()
    return res

def preview_component(comp):
    html = component_to_html(comp)
    display(HTML(html))


question_template = ['''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
    <div id = content> </div>

    <div id =solution></div>

    <button onclick="finish()">finish</button>

    <div id=tip></div>
    <button onclick="tip()">tip?</button>
</body>
</html>



<script>

    var json = ''','''
    q = JSON.parse(json)
    s = JSON.parse(q.solution)
    // s = q.solution
    console.log(s);
    content = document.getElementById("content").innerHTML += q.title

    solution = document.getElementById("solution")


    function tip(){
        div = document.getElementById("tip")

        div.innerHTML = q.tip
    }

    function finish(){
        console.log('finishing ');
        inputs = document.querySelectorAll("input")
        answer = []
        inputs.forEach(element => {
            if (!element.readOnly)
            answer.push(element.value)
        });

        console.log(answer);

        error = []
        for (let i = 0; i < answer.length; i++) {
            const ans = answer[i];
            const sol = s[i]
            if (ans!=sol && sol != " "){
                error.push(i)
            }
        }

        console.log({error});

        if (error.length == 0) {
            console.log("success");
        }else{
            console.log("fail.");
            solution.innerHTML += q.title

            inps = solution.querySelectorAll("input")
            delt = 0
            for (let i = 0; i < inps.length; i++) {
                const inp = inps[i];
                if (!inp.readOnly){
                    console.log(inp)
                    console.log(s[i-delt])
                    inp.value = s[i-delt]
                    if (error.includes(i-delt)){
                        inp.style.background = '#0f0'
                    }
                }else{delt += 1}
            }
        }
    }
</script>
''']


f = open("./question_template.html")
question_template = f.read()
f.close

def browse_question(q):

    data = json.dumps(q)
    data = json.dumps(data)
    html = question_template.replace("{}",data)
    f = open ("question.html",'w')
    f.write(html)
    f.close()

    print(f"view file://{os.path.abspath('question.html')} in browser")
    