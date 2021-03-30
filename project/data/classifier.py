from sklearn import preprocessing
import json
import pickle
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import random
from data.models import *
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC, LinearSVC
from django.contrib.postgres.aggregates import ArrayAgg

class Cuisine_Classifier:
    def __init__(self,ingredientList,train_data,model=LogisticRegression(solver='liblinear', multi_class='ovr'),filename=""):
        self.ingredientList=ingredientList
        self.train_data=train_data
        self.clf,self.le=self.BuildModel("cuisine_model.sav",model,filename)
    def BuildModel(self,filename,model,readymodel):
        if readymodel=="":
            if self.train_data.shape[1]!=len(self.ingredientList)+3: # +3 for id, cuisine and list of ingredients array
                self.train_data=self.IngredientsDataTransform(self.train_data)
        X=self.train_data.drop(['id','ingredients','cuisine'],axis=1)
        y=self.train_data['cuisine']
        print("Using label encoder...")
        le = preprocessing.LabelEncoder()
        le.fit(y)
        y=le.transform(y)
        print("Fitting classifier...")
        clf=model
        if readymodel=="":
            #LogisticRegression(solver='liblinear', multi_class='ovr')
            clf.fit(X,y)
            pickle.dump(clf, open(filename, 'wb'))
            print("Classifier model ready and saved!")
        else:
            clf=pickle.load(open(readymodel, 'rb'))
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
        for i in data.index.values:#range(len(data)):
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
    
class Classifier():
    def __init__(self):
        pass
    def GetRecipes(self):
        print("Get Recipes")
        recipes = Recipe.objects.annotate(ing_titles=ArrayAgg("ingredients__title"),tag_titles=ArrayAgg("tags__pk"))
        data=list(recipes.values_list("pk", "ing_titles", "tag_titles"))
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
            #print(f"Index : {index}, Value : {value}")
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
    def GetTrain_Test_Split(self):
        recipes = Recipe.objects.annotate(ing_titles=ArrayAgg("ingredients__title"),tag_titles=ArrayAgg("tags__pk"))
        data=list(recipes.values_list("pk", "ing_titles", "tag_titles"))
        #data=data[0:1000]
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
            #print(f"Index : {index}, Value : {value}")
        recipe_data={"id":[],"ingredients":[],"cuisine":[]}
        test_data={"id":[],"ingredients":[],"cuisine":[]}
        unlabeled_recipe={"id":[],"ingredients":[]}
        for recipe in data:
            if(recipe[2][0]==None):
                unlabeled_recipe["id"].append(recipe[0])
                unlabeled_recipe["ingredients"].append(recipe[1])       
            elif recipe[2][0] in important_classes :
                if random.random()<.9:
                    recipe_data["id"].append(recipe[0])
                    recipe_data["ingredients"].append(recipe[1])
                    recipe_data["cuisine"].append(recipe[2][0])
                else:
                    test_data["id"].append(recipe[0])
                    test_data["ingredients"].append(recipe[1])
                    test_data["cuisine"].append(recipe[2][0])
        recipe_df=pd.DataFrame(data=recipe_data)
        test_df=pd.DataFrame(data=test_data)
        return recipe_df,test_df

    def GetIngredientList(self):
        print("Get Ingredients!")
        ings = Ingredient.objects.annotate(count=models.Count("recipe"))
        data = [{"pk": d.pk, "title": d.title, "num_recipe": d.count} for d in ings]
        ingredientsList=pd.DataFrame(data)
        ingredientsList=ingredientsList.loc[ingredientsList["num_recipe"]>=100] # change common ingredients from 100 to 1000
        ingredientsList=ingredientsList["title"].array
        return ingredientsList
    def Classification(self,filename="",threshold=0.51):
        print("Classification start!")
        labelled_recipe,unlabelled_recipe=self.GetRecipes()
        ingredientsList=self.GetIngredientList()
        model=Cuisine_Classifier(ingredientsList,labelled_recipe,filename=filename)
        testing,labels=model.ReturnAllProba(unlabelled_recipe)
        labelled_data=model.GiveLabels(testing,labels,threshold=threshold)
        counts=labelled_data["cuisine"].value_counts()
        for index, value in counts.items():
            if index==[]:
                labelled_percent=1-(value/testing.shape[0])
                print(labelled_percent)
        return labelled_data
    def SaveLabels(self,filename="",threshold=0.51):
        labelled_data=self.Classification(filename=filename,threshold=threshold)
        tags=Tag.objects.all()
        recipe=Recipe.objects.all()
        #print(tags)
        for recipe in labelled_data.iterrows():
            recipe=recipe[1]
            #print(recipe["cuisine"])
            if len(recipe["cuisine"])>0:
                Recipe.objects.get(id=recipe["id"]).tags.add(Tag.objects.get(id=recipe["cuisine"][0]))
    def PrintLabels(self,filename="",threshold=0.51):
        labelled_data=self.Classification(filename=filename,threshold=threshold)
        tags=Tag.objects.all()
        recipe=Recipe.objects.all()
        #print(tags)
        for recipe in labelled_data.iterrows():
            recipe=recipe[1]
            #print(recipe["cuisine"])
            if len(recipe["cuisine"])>0:
                print(Recipe.objects.get(id=recipe["id"]).title+" "+Tag.objects.get(id=recipe["cuisine"][0]).title)

    def NumLabelled(self):
        train_data,test_data=self.GetRecipes()
        print(train_data.shape[0])
        print(test_data.shape[0])
    def CrossValScore(self):
        train_data,test_data=self.GetRecipes()
        ingredientsList=self.GetIngredientList()
        model=Cuisine_Classifier(ingredientsList,train_data)
        kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
        cv_results = cross_val_score(LogisticRegression(solver='liblinear', multi_class='ovr'), model.train_data.drop(['id','ingredients','cuisine'],axis=1), model.train_data['cuisine'], cv=kfold, scoring='f1_weighted')
        print('Log regression accuracy: %f (%f)' % ( cv_results.mean(), cv_results.std()))
    def ClassificationReport(self, threshold=0.51):
        train_data,test_data=self.GetRecipes()
        ingredientsList=self.GetIngredientList()
        model=Cuisine_Classifier(ingredientsList,train_data)
        train,test=train_test_split(model.train_data,train_size=0.9,test_size=0.1,random_state=1, shuffle=True)
        clf=LogisticRegression(solver='liblinear', multi_class='ovr')
        X=train.drop(['id','ingredients','cuisine'],axis=1)
        y=train['cuisine']
        le = preprocessing.LabelEncoder()
        le.fit(y)
        y=le.transform(y)
        clf.fit(X,y)
        proba_array=clf.predict_proba(test.drop(['id','ingredients','cuisine'],axis=1))
        label_column={"tag":[]}
        for i in range(len(proba_array)):
            label=""
            for j in range(len(proba_array[i])):
                if proba_array[i][j]>threshold:
                    label=le.inverse_transform([j])[0]
            label_column["tag"].append(label)  
        final_test=pd.concat([test[["id","ingredients","cuisine"]], pd.DataFrame(data=label_column)], axis=1, join="inner")
        final_test=final_test.loc[final_test["tag"]!=""]
        print(final_test)
        correct=0
        sumrecord=0
        for i in range(len(final_test['cuisine'].values)):
            sumrecord+=1
            if final_test['cuisine'].values[i]==final_test["tag"].values[i]:
                correct+=1
        print("accuracy: "+str(correct/sumrecord))
    def TestAcc(self,threshold=0.51,model=LogisticRegression(solver='liblinear', multi_class='ovr')):
        train_data,test_data=self.GetRecipes()
        ingredientsList=self.GetIngredientList()
        train,test=self.GetTrain_Test_Split()
        model=Cuisine_Classifier(ingredientsList,train,model)
        print(test)
        testing,labels=model.ReturnAllProba(test.drop(['cuisine'],axis=1))
        pred=model.GiveLabels(testing,labels,threshold)
        print(pred['cuisine'].values)
        print(test['cuisine'].values)
        correct=0
        alltries=0
        for i in range(len(pred['cuisine'].values)):
            if len(pred['cuisine'].values[i])==1:
                alltries+=1
                if pred['cuisine'].values[i][0]==test['cuisine'].values[i]:
                    correct+=1
        resultstr="accuracy: "+str(correct/alltries)+" classified: "+str(100*alltries/len(pred['cuisine'].values))+"%"
        print(resultstr)
        return resultstr
    def ModelTesting(self):
        models = []
        #models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        thresholds=[0.45,0.50,0.51,.55,.60,.65,.70]
        with open('modeltest.txt', 'a') as modelFile:
            for model in models:
                modelFile.write("Model name: "+model[0]+"\n")
                for threshold in thresholds:
                    modelFile.write("threshold: "+str(threshold)+" "+self.TestAcc(threshold,model[1])+"\n")
    def SaveModel(self,model=LogisticRegression(solver='liblinear', multi_class='ovr')):
        labelled_recipe,unlabelled_recipe=self.GetRecipes()
        ingredientsList=self.GetIngredientList()
        model=Cuisine_Classifier(ingredientsList,labelled_recipe,model)
        print("Model created")
    def UseSavedModel(self,filename):
        labelled_recipe,unlabelled_recipe=self.GetRecipes()
        ingredientsList=self.GetIngredientList()
        model=Cuisine_Classifier(ingredientsList,labelled_recipe,filename=filename)
        return model



        

        