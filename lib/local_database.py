
import json
import random
from typing import Mapping


courses = ["math"]
niveaus = ["A","B","C","D","E","F","G","H","msa"]


class Question:

    def __init__(self,title,solution,tip,explanation ='',course='math',niveau='C',series_name =''):
        self.title = title
        self.solution = solution
        self.tip = tip
        self.explanation = explanation
        self.series_name = series_name
        self.rating = -1
        self.name = f'{course}_{niveau}'

    def dumps(self):
        return json.dumps(self.__dict__)
    def load(data:dict):
        self = object.__new__(Question)
        self.__dict__ = data
        return self

    #static
    def standart(tit:str,sol,tit_params = [],tip = "",explanation=""):

        assert type(tit) != Question , "cant call standart on object. only use `Question.standart`"
        assert tit.count('{}') == tit.count('{') , "title wrong format if u want to include css do it in the style parameter"
        assert len ( tit_params) >= tit.count('{}'), 'params has not enough items to fill the title'
        assert type(tip) == str, f"tip needs to be a string but is {type(tip)}"

        if type(sol) in [int,float]:
            sol = [sol]
        if type(sol) == str:
            sol:str = sol
            if sol.find("[") == -1:
                sol = [sol]
        if type (sol) ==list:
            sol = json.dumps(sol)

        return Question(
            tit.format(*tit_params),
            solution=sol,
            tip = tip,
            explanation=explanation
        )

    def multiple_choice(title:str,correct_options:list[str],wrong_options:list[str],tip,explanation=''):
        title = f"<h3>{title}</h3><br>"
        options = correct_options + wrong_options
        options = random.sample(options,len(options))
        for option in options:
            title += f"<button>{option}</button>\n"
        
        correct_options = list(map(str, correct_options))

        return Question.standart(title,correct_options,[],tip,explanation)
    
    def __repr__(self) -> str:

        return f'<Q: {self.series_name} {self.title[:40]} : {self.solution}>'

class Series:
    def __init__(
            self,
            name,
            questions = None,
            rating_increment =0):

        self.name = name
        self.questions = [] if questions == None else questions
        self.rating_increment = rating_increment

class Collection:

    def load(name):
        with open('./education_data/'+name+'.json','r') as file:
            data:list[dict] = json.load(file)
            
        q_list = list(map(Question.load,data))

        with open('./education_data/'+name+"_info.json",'r') as file:
            info = json.load(file)

        series_names:list[str] = info['series_names']
        series_dict = {}

        for sname in series_names:
            series_dict[sname] = Series(sname)

        last_series = series_dict[series_names[0]]

        last_series_max_rating = 0

        for q in q_list:

            if q.series_name != last_series.name:
                last_series_max_rating += last_series.rating_increment
                last_series = series_dict[q.series_name]

            last_series.rating_increment = q.rating - last_series_max_rating
            last_series.questions.append(q)
        
        return Collection(info['course'],info['niveau'],series_names,series_dict)

    def save(self):

        name = f"{self.course}_{self.niveau}"

        rating_range = 0
        q_list:list[Question] = []
        for s_name in self.series_names:
            series = self.series_dict[s_name]
            q_num  =len(series.questions)
            r_step = series.rating_increment/q_num
            print(f"sname: {s_name} rstep: {r_step}")
            for q in series.questions:
                q.series_name = s_name
                rating_range += r_step
                q.rating = rating_range
                q.collection = self.name
                q_list.append(q)

        with open('./education_data/'+name+'.json','w') as file:
            q_data = ',\n'.join(map(lambda q : q.dumps(),q_list)) 
            file.write(f'[{q_data}]')

        info = {
            "course":self.course,
            "niveau":self.niveau,
            "series_names":self.series_names,
            "rating_range":rating_range,
        }

        with open('./education_data/'+name+"_info.json",'w') as file:
            json.dump(info,file,indent = 4)

    def __init__(self,course = "math", niveau = "C",series_names = None, series_dict = None):


        self.course = course
        self.niveau = niveau
        self.name = f"{course}_{niveau}"

        '''includes the actual series data'''
        self.series_dict= {} if series_dict==None else series_dict

        '''this decides the rankings of the serieses'''
        self.series_names = [] if series_names == None else series_names

    def remove_series(self,name):
        if name not in self.series_dict:
            print("error: series not included.")
            return
        self.series_names.remove(name)
        del self.series_dict[name]

    def rename_series(self,prev,next):
        self.series_names[self.series_names.index(prev)] = next
        self.series_dict[next] = self.series_dict.pop(prev)

    def add_series(self,questions:list[Question],rating_increment:int,name:str,replace = False):
        new_series = Series(name,questions,rating_increment)
        if name in self.series_dict:
            if replace:
                self.series_dict[name] = new_series
            else:
                print("ERROR: series allready exists. If you want to replace it call with replace = True")
        else:
            assert name not in self.series_names, 'shouldnt happen but _can_ be ignored'
            self.series_names.append(name)
            self.series_dict[name] = new_series

    def __repr__(self):
        return f"""<Collection {self.course}_{self.niveau} {len(self.series_names)} types>"""

class Database():

    version = "0.0.1"

    def get_info(self):


        info = {
            "version":Database.version,
            "courses":{}
        }
        for c_n in self.collection_names:
            print(c_n)
            col = self.collections[c_n]
            course = col.course
            niveau = col.niveau
            info_courses = info["courses"]

            if course not in info_courses:
                info_courses[course] = {}
            
            info_courses[course][niveau] = col.series_names

        return info

    def __init__(self,load = True):
        self.collection_names = []
        self.collections:Mapping[str,Collection] = {}

        if load:
            try:
                infofile = open('./education_data/info.json','r')
                self.info = json.load(infofile)
                infofile.close()
            except:
                self.info = self.get_info()

            course_info:Mapping[str,Mapping[str,list[str]]] = self.info['courses']

            for course_name,course in course_info.items():
                for nivea,s in course.items():
                    name = f"{course_name}_{nivea}"
                    self.collection_names.append(name)
                    self.collections[name] = (Collection.load(name))
        else:
            self.info = self.get_info()


    def save(self):

        infofile = open('./education_data/info.json','w')
        json.dump(self.get_info(),infofile,indent=4)
        infofile.close()

        for _,col in self.collections.items():
            col.save()


    def get_collection(self,course="math", niveau="C"):

        if course not in courses:raise KeyError("not a valid course.")
        if niveau not in niveaus:raise KeyError("not a valid niveau")

        name = f"{course}_{niveau}"
        if name in self.collections:
            return self.collections[name]

        coll = Collection(course,niveau)
        self.collections[name] = coll
        self.collection_names.append(name)
        return coll
    
    def __repr__(self):

        cols = "\n".join(self.collections)

        return f"""<Database collections:{cols}>"""
    
    def remove_collection(self,course,niveau):
        name = f"{course}_{niveau}"
        del self.collections[name]
        self.collection_names.remove(name)

    def clear(self):
        self.info = {
            "version":Database.version,
            "collections": []
        }
        self.collections = {}
        self.collection_names = self.info['collections']

db:Database = None        
try:
    db = Database()
except:
    print("couldnt find saved data")
    db = Database(load = False)

Question.STD = Question.standart
Question.MC = Question.multiple_choice

def randint(size): return random.randint(10**(size-1),10**size-1)
# %%