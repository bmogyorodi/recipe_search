from sklearn import preprocessing
import json
import pickle
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from data.models import *
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from django.contrib.postgres.aggregates import ArrayAgg

class Cuisine_Classifier:
    def __init__(self,ingredientList,train_data):
        self.ingredientList=ingredientList
        self.train_data=train_data
        self.clf,self.le=self.BuildModel("cuisine_model.sav")
    def BuildModel(self,filename):
        if self.train_data.shape[1]!=len(self.ingredientList)+3: # +3 for id, cuisine and list of ingredients array
            self.train_data=self.IngredientsDataTransform(self.train_data)
        X=self.train_data.drop(['id','ingredients','cuisine'],axis=1)
        y=self.train_data['cuisine']
        print("Using label encoder...")
        le = preprocessing.LabelEncoder()
        le.fit(y)
        y=le.transform(y)
        print("Fitting classifier...")
        clf=LogisticRegression(solver='liblinear', multi_class='ovr')
        clf.fit(X,y)
        pickle.dump(clf, open(filename, 'wb'))
        print("Classifier model ready and saved!")
        return clf,le
    def ReturnClassProb(self,data,className):
        if className not in self.le.classes_:
            return "Error, Label Encoder doesn't recognize cuisine!"
        label_num=self.le.transform([className])[0]
        if data.shape[1]!=len(self.ingredientList)+2:
            data=self.IngredientsDataTransform(data)
        X=data.drop(['id','ingredients'],axis=1)        
        probs=self.clf.predict_proba(X)
        return data,probs[:,label_num]
    def IngredientsDataTransform(self,data):
        print("Adding ingredient attributes...")
        for i in self.ingredientList:
            data[i]=np.zeros(len(data))
        print("Filling out ingredients table...")
        for i in range(len(data)):
            for j in data['ingredients'][i]:
                if data.get(j) is not None:
                    data[j].iloc[i]=1
        return data
    def ReturnBestLabel(self,data):
        if data.shape[1]!=len(self.ingredientList)+2:   # +2 for id and ingredient array
            data=self.IngredientsDataTransform(data)
        X=data.drop(['id','ingredients'],axis=1)        
        probs=self.clf.predict(X)
        #probs=self.clf.predict_proba(X)
        return data,self.le.inverse_transform(probs)#[0]
    def ReturnAllProba(self,data):
        if data.shape[1]!=len(self.ingredientList)+2:   # +2 for id and ingredient array
            data=self.IngredientsDataTransform(data)
        X=data.drop(['id','ingredients'],axis=1)        
        probs=self.clf.predict_proba(X)
        return data,probs#[0]
    def GiveLabels(self,test_data,proba_array,threshold=0.51): #on default only label if the class is definitely most likely
        label_column={"cuisine":[]}
        for i in range(len(proba_array)):
            labels=[]
            for j in range(len(proba_array[i])):
                if proba_array[i][j]>threshold:
                    labels.append(self.le.inverse_transform([j])[0])
            label_column["cuisine"].append(labels)            
        return pd.concat([test_data[["id","ingredients"]], pd.DataFrame(data=label_column)], axis=1, join="inner")
    
class Test():
    def GetRecipes(self):
        recipes = Recipe.objects.annotate(ing_titles=ArrayAgg("ingredients__title"),tag_titles=ArrayAgg("tags__pk"))
        print("Hello2")
        data=list(recipes.values_list("pk", "ing_titles", "tag_titles"))
        print("Hello2")
        recipe_data={"id":[],"ingredients":[],"cuisine":[]}
        unlabeled_recipe={"id":[],"ingredients":[]}
        for recipe in data:
            if(recipe[2][0]!=None):
                recipe_data["id"].append(recipe[0])
                #recipe_data["ingredients"].append(filterList2(recipe[1],ingredientsList))
                recipe_data["ingredients"].append(recipe[1])
                recipe_data["cuisine"].append(recipe[2][0])
            else:
                unlabeled_recipe["id"].append(recipe[0])
                #unlabeled_recipe["ingredients"].append(filterList2(recipe[1],ingredientsList))
                unlabeled_recipe["ingredients"].append(recipe[1])
        
        recipe_df=pd.DataFrame(data=recipe_data)
        unlabeled_df=pd.DataFrame(data=unlabeled_recipe)
        train_data=recipe_df
        test_data=unlabeled_df
        counts=train_data["cuisine"].value_counts()
        important_classes=[]
        for index, value in counts.items():
            if value>=100:
                important_classes.append(index)
            print(f"Index : {index}, Value : {value}")
        recipe_data={"id":[],"ingredients":[],"cuisine":[]}
        unlabeled_recipe={"id":[],"ingredients":[]}
        for recipe in data:
            if(recipe[2][0]==None):
                unlabeled_recipe["id"].append(recipe[0])
                unlabeled_recipe["ingredients"].append(recipe[1])       
            elif recipe[2][0] in important_classes :
                recipe_data["id"].append(recipe[0])
                recipe_data["ingredients"].append(recipe[1])
                recipe_data["cuisine"].append(recipe[2][0])
        
        recipe_df=pd.DataFrame(data=recipe_data)
        unlabeled_df=pd.DataFrame(data=unlabeled_recipe)
        train_data=recipe_df
        test_data=unlabeled_df
        return train_data,test_data
    def GetIngredientList(self):
        ings = Ingredient.objects.annotate(count=models.Count("recipe"))
        data = [{"pk": d.pk, "title": d.title, "num_recipe": d.count} for d in ings]
        #print(data)
        ingredientsList=pd.DataFrame(data)
        ingredientsList=ingredientsList.loc[ingredientsList["num_recipe"]>=100]
        ingredientsList=ingredientsList["title"].array
        print(ingredientsList)
        return ingredientsList
    def Classification(self):
        labelled_recipe,unlabelled_recipe=self.GetRecipes()
        #shortener for testing remove two lines below to avoid shortening training and test data
        labelled_recipe=labelled_recipe[0:100]
        unlabelled_recipe=unlabelled_recipe[0:100]
        ingredientsList=self.GetIngredientList()
        model=Cuisine_Classifier(ingredientsList,labelled_recipe)
        testing,labels=model.ReturnAllProba(unlabelled_recipe)
        labelled_data=model.GiveLabels(testing,labels,threshold=0.51)
        counts=labelled_data["cuisine"].value_counts()
        for index, value in counts.items():
            if index==[]:
                labelled_percent=1-(value/testing.shape[0])
                print(labelled_percent)
        return labelled_data
    def SaveLabels(self):
        labelled_data=self.Classification()
        tags=Tag.objects.all()
        recipe=Recipe.objects.all()
        print(tags)
        for recipe in labelled_data.iterrows():
            recipe=recipe[1]
            print(recipe["cuisine"])
            if len(recipe["cuisine"])>0:
                Recipe.objects.get(id=recipe["id"]).tags.add(Tag.objects.get(id=recipe["cuisine"][0]))
    def NumLabelled(self):
        train_data,test_data=self.GetRecipes()
        print(train_data.shape[0])
        print(test_data.shape[0])
        

        