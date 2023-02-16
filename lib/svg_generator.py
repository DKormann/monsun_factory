import math
svg_template = '''
<div >
<svg height="40vh%" viewBox="0 0 1000 1000" width="40vh" style="background:white;fill-rule:nonzero;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;"  >
{}
</svg>
</div>
'''
def svg(*items): return svg_template.format("\n".join(items))

path_template = '''<path d="{}" fill="none" opacity="1" stroke="{}" stroke-linecap="round" stroke-linejoin="round" stroke-width="7"/>'''
fill_template = '''<path d="{}" fill="{}" opacity="1" stroke="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="7"/>'''

def line_from_path(content,color = '#000'):return path_template.format(content,color)
def fill_from_path(content,color = '#000'):return fill_template.format(content,color)

def points_to_path(*points:tuple[float,float]):
    points = map(lambda p:str(p[0])+' '+str(p[1]),points)
    path = "M"+"L".join(points)
    return path

def line(*points,color='#000'):
    return line_from_path(points_to_path(*points),color)
def fill(*points,color='#000'):
    return fill_from_path(points_to_path(*points),color)


def nice_subdivisions(arg,max_divisions):

    step = 10 ** int((math.log10(arg)-2))
    upper = step * max_divisions

    while True:

        for pow in [1,2,5]:
            substep = step * pow
            upper  = substep * max_divisions
            if upper >= arg:

                while upper - substep > arg:
                    upper -= substep 

                return substep
        step *= 10

nice_subdivisions(3,10)


funny_colors = ['#e44','#2e2','#55f','#dd0','#e2e']
last_funny_color = 0

def funny_color():
    global last_funny_color
    last_funny_color = (1+last_funny_color)%len(funny_colors)
    return funny_colors[last_funny_color]

def diagram(nums, names, ylabel = ""):

    h = 1000
    w = 1000
    xmax = len(nums)+0.5
    ymax = max(nums)

    stepsize = nice_subdivisions(ymax,10)
    ymax += stepsize

    
    lpad = 0.15
    rpad = 0.1
    tpad = 0.1
    bpad = 0.1

    rel = lambda x, y : (xrel(x),yrel(y))
    xrel = lambda x : (lpad +(1-lpad-rpad)*x)*w
    yrel = lambda x : ((1-bpad)-(1-bpad-tpad)*x)*h
    xworl = lambda x : xrel(x/xmax)
    yworl = lambda y : yrel(y/ymax)

    def pt(arg): return (xworl(arg[0]),yworl(arg[1]),)

    def bar(x,y):return fill(
                (xworl(x+0.5),yworl(0)),
                (xworl(x+1),yworl(0)),
                (xworl(x+1),yworl(y)),
                (xworl(x+0.5),yworl(y)),color=funny_color())

    bars = []
    for i,num in enumerate(nums):
        bars.append(bar(i,num))

    
    labels = [f'<text x="10" y="{yworl(num)+10}" font-size="35">{num}</text>' for num in range(stepsize,ymax,stepsize)]
    y = yrel(0.02)
    name_labels = [f'<text transform="rotate(-90 {xworl(i+0.75)},{y})" x="{xworl(i+0.75)}" y="{y}" font-size="35">{names[i]}</text>' for i in range(len(names))]
    vec = svg(

        *[line((xrel(0),yworl(i)),(xrel(1),yworl(i)),color="#ccc") for i in range(0,ymax,stepsize)],
        *bars,
        *[line((xrel(-0.02),yworl(i)),(xrel(0.02),yworl(i)),) for i in range(0,ymax,stepsize)],
        *labels,
        *name_labels,
        f'<text x="{xrel(-0.06)}" y="{yrel(1.06)}" font-size="35">{ylabel}</text>' ,

        line(rel(0,1.05),rel(0,0),rel(1.05,0)),
        line(rel(-.02,1),rel(0,1.05),rel(0.02,1)),
        line(rel(1,-.02),rel(1.05,0),rel(1,0.02)),
    )

    html = f'''<div style="background:white;display:inline">  {vec}</div>'''
    return html
