import json
import random
import os

from typing import List, Mapping

courses = ["math"]
niveaus = "ABCDEFGH"

class Database():

    version = "0.0.1"

    def __init__(self):

        try:
            infofile = open('./education_data/info.json','r')
            self.info = json.load(infofile)
            infofile.close()
        except:
            self.info = {
                "version":Database.version,
                "collections": []
                }
        self.collection_names:List[str] = self.info['collections']
        self.collections:Mapping[str,Collection] = {}
        for col in self.collection_names:
            self.collections[col] = Collection.load(col)

    def save(self):

        infofile = open('./education_data/info.json','w')
        json.dump(self.info,infofile,indent=4)
        infofile.close()

        for _,col in self.collections.items():
            col.save()


    def get_collection(self,course, niveau):

        if course not in courses:raise KeyError("not a valid course.")
        if niveau not in niveaus:raise KeyError("not a valid niveau")

        name = f"{course}_{niveau}"
        if name in self.collections:
            return self.collections[name]
        coll = Collection.new(course,niveau)
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



class Collection:

    def load(name):
        file = open('./education_data/'+name+'.json','r')
        data = json.load(file)
        file.close()

        file = open('./education_data/'+name+"_info.json",'r')
        info = json.load(file)
        file.close()

        return Collection(info,data)

    def save(self):
        name = f"{self.info['course']}_{self.info['niveau']}"

        file = open('./education_data/'+name+'.json','w')
        json.dump(self.questions,file,indent = 4)
        file.close()

        file = open('./education_data/'+name+"_info.json",'w')
        json.dump(self.info,file,indent = 4)
        file.close()


    def new(course, niveau):
        return Collection(info={
            "course":course,
            "niveau":niveau,
            "series":{},
            "next_rating":0,
        },questions=[])

    def __init__(self,info,questions):

        self.info = info
        self.questions = questions

    def remove_series(self,series_name):
        series_info = self.info['series'][series_name]
        rating_range = series_info['rating_range']
        min_rating = series_info['min_rating']

        min_idx = 0
        max_idx = 0
        for i,q in enumerate(self.questions):
            if q['series_name'] == series_name:
                max_idx = i
                if min_idx == 0:min_idx = i
        
        self.questions = self.questions[:min_idx] + self.questions[max_idx+1:]
        for q in self.questions:
            if q['rating'] > min_rating:
                q['rating'] -= rating_range
        del self.info['series'][series_name]

    def __getattr__(self, __name: str):
        info = object.__getattribute__(self,"info")
        if __name in info: return info[__name]
        raise AttributeError(__name+" not found")


    def add_many(self,qs,rating_increment, series_name):
        if series_name in self.info['series']:
            print (f"error: {series_name} series allready exists if u are trying to replace it call collection.remove_series(\"{series_name}\")")
            return 
        self.info['series'][series_name] = get_series_info(series_name,self.info['next_rating'],rating_increment)
        
        if len(qs) < rating_increment:
            raise ValueError("rating_increment needs to be as big as len of questions")

        rating_step = rating_increment/len(qs)
        rating = self.info['next_rating']

        for q in qs:
            q['series_name'] = series_name
            q['course'] = self.info['course']
            q['niveau'] = self.info['niveau']
            q['rating'] = rating
            rating += rating_step
            self.questions.append(q)

        self.info['next_rating'] += rating_increment

    def __repr__(self):
        return f"""<Collection {self.info['course']}_{self.info['niveau']} N{len(self.questions)} R{self.info["next_rating"]}>"""


def get_series_info(name,min_rating,rating_range):
    return {"name":name,
        "min_rating":min_rating,
        "rating_range":rating_range,}

def get_question (tit,sol:any,tit_params,tip,style=""):

    assert tit.count('{}') == tit.count('{') , "title wrong format if u want to include css do it in the style parameter"
    assert len ( tit_params) >= tit.count('{}'), 'params has not enough items to fill the title'


    # make sol a json rep of list of string or number solutions
    if type(sol) in [int,float]:
        sol = [sol]
    if type(sol) == str:
        sol:str = sol
        if not sol.find("[") == -1:
            sol = [sol]
    if type (sol) ==list:
        sol = json.dumps(sol)

    return {
        "title":tit.format(*tit_params)+style,
        "solution":sol,
        "tip":tip
    }


def option_question(title,correct_options:list[str],wrong_options:list[str],tip ,style = ""):

    title = f"<h3>{title}</h3><br>"
    options = correct_options + wrong_options
    options = random.sample(options,len(options))
    for option in options:
        title += f"<button>{option}</button>\n"
    
    correct_options = list(map(str, correct_options))

    return get_question(title,correct_options,[],tip,style)