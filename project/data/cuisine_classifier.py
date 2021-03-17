from sklearn import preprocessing
import json
import pickle
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from data.models import Recipe
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
    

recipes = Recipe.objects.annotate(ing_titles=ArrayAgg("ingredients__title"), tag_titles=ArrayAgg("tags__title"))
recipes.values_list("pk", "ing_titles", "tag_titles")
print(recipes)