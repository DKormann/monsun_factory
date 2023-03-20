import math
svg_template = '''
<div >
<svg width="{}" viewBox="0 0 {} {}"  style="background:{};fill-rule:nonzero;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;"  >
{}
</svg>
</div>
'''
def svg(*items,outer_width= "40vh",width=1000,height =1000,background_color='white'): return svg_template.format(outer_width,width,height,background_color,"\n".join(items))

path_template = '''<path d="{}" fill="{}" opacity="1" stroke="{}" stroke-linecap="round" stroke-linejoin="round" stroke-width="{}"/>'''
fill_template = '''<path d="{}" fill="{}" opacity="1" stroke="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="7"/>'''

def line_from_path(content,color = '#000',fill = "none",stroke_width = 7):return path_template.format(content,fill,color,stroke_width)
def fill_from_path(content,color = '#000'):return fill_template.format(content,color)

def points_to_path(*points:tuple[float,float]):
    points = map(lambda p:str(round(p[0],3))+' '+str(round(p[1],3)),points)
    path = "M"+"L".join(points)
    return path

def line(*points,color='#000',fill= 'none',stroke_width='7'):
    return line_from_path(points_to_path(*points),color,fill,stroke_width)
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

text = lambda x,y,txt : f'<text x="{x}" y="{y}" font-size="35">{txt}</text>'

view_size = 1000
min_pad = 7

light_yellow = '#f0ee99'

"""generate a rectangular vector image grid"""
class Grid:
    def __init__(self,X,Y,width = "40vh"):
        
        self.width = width

            
        self.X,self.Y = X,Y

        #available figure size
        self.fig_size = view_size - min_pad*2

        #max side cellcount 
        W = max(X,Y)

        #cell size
        self.c = self.fig_size/W

        self.w = X*self.c
        self.h = Y*self.c

        self.lines = [
            *[line(self.rel(0,i),self.rel(X,i),color=light_yellow) for i in range(Y+1)],
            *[line(self.rel(i,0),self.rel(i,Y),color=light_yellow) for i in range(X+1)],
        ]

    def relx(self,x):return x*self.c+min_pad
    def rely(self,y):return y*self.c+min_pad
    def rel(self,x,y):return (self.relx(x),self.rely(y))

    def add_figure(self,*points,color="#000",fill= "#fff"):
        self.lines.append(line(
            *[self.rel(*point)for point in points],
            color=color,fill = fill,
        ))

    def get_html(self):
        html = svg(*self.lines,outer_width=self.width,width=self.w+min_pad*2, height= self.h+min_pad*2)
        return html


deg2rad = lambda deg: deg/180*math.pi
def rad2cart(rad:float):
    y = 1-math.cos(rad)
    x = math.sin(rad)
    return x,y
def bow_point(center, r, rad):
    y = (-math.cos(rad))*r
    x = math.sin(rad)*r
    return (center[0]+x,center[1]+y)

def bow(center,r:float,start:float,end:float):
    if end<start:
        end += 360
    
    start = deg2rad(start)
    end = deg2rad(end)

    p = []

    while start < end:
        p.append(bow_point(center,r,start))
        start += 0.2
    
    p.append(bow_point(center,r,end))

    return p
