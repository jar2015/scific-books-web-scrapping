# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:22:23 2019

@author: rodriguezjos
"""
#IMPORT LIBRARIES NEEDED
import requests
import pandas as pd
from bs4 import BeautifulSoup

#LIST OF PAGES IN WEBSITE
pages = [str(i) for i in range(1,13300)]

#CREATE LIST OF VARIABLES IN WEBSITE
author_name = []
book_name = []
details_desc = []

#LOOP TO SEARCH IN ALL THE PAGES
for page in pages:
    res = requests.get('https://www.bookrix.com/books;lang:all,page:'+ page + '.html')
    soup = BeautifulSoup(res.text)
    
    #CREATE A CONTAINER WHERE DATA IS
    books_container = soup.find_all('div', class_ = 'item-content')
    
    #LOOP TO SEARCH IN THE CONTAINER THE VARIABLES NEEDED
    for container in books_container:
        #SEARCH AND APPEND THE BOOK AUTHOR'S NAME
        name = container.find('a', class_ = 'item-author').text
        author_name.append(name)
        #SEARCH AND APPEND THE BOOK NAME
        book = container.find('a', class_ = 'word-break').text
        book_name.append(book)
        #SEARCH AND APPEND BOOK DETAILS
        details = container.find('ul', class_ = 'item-details').text
        details_desc.append(details)

#CREATE DATAFRAME WITH FIELDS CREATED BEOFRE
df_books = pd.DataFrame({'Author Name': author_name,
'Book Name': book_name,
'details': details_desc
})

#SPLIT DETAILS FIELD IN MORE COLUMNS
new = df_books['details'].str.split('\n', n=7, expand= True)
df_books["Categorie"]= new[1] 
df_books["Language"]= new[2] 
df_books["Words"]= new[3]
df_books["Age"]= new[4]
df_books["Views"]= new[5]
df_books["Favorite"]= new[6] 

#DELETE DETAILS FIELD BECAUSE IT WAS SPLITTED 
df_books.drop(columns =['details'], inplace = True) 

#REMOVE WORDS IN COLUMNS
df_books["Words"] = df_books["Words"].str.replace(' Words','')
df_books["Age"] = df_books["Age"].str.replace('Ages ','')

#REMOVE DUPLICATES IN CASE THEY EXIST
df_books.drop_duplicates(subset ="First Name", keep = False, inplace = True) 

#CREATED A CSV FILE USING DATAFRAME CREATED
df_books.to_csv(r'C:\Users\rodriguezjos\OneDrive - VMware, Inc\VMwareCorp\Desktop\Master Data Sciences\3- II Semestre 2019\Tipologia y cliclo de vida de los datos\PRAC 1\Books_dataset_vf.csv', index=False)

libros = pd.read_csv('C:\Users\rodriguezjos\OneDrive - VMware, Inc\VMwareCorp\Desktop\Master Data Sciences\3- II Semestre 2019\Tipologia y cliclo de vida de los datos\PRAC 1\Books.csv')