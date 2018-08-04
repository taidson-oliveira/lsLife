from bs4 import BeautifulSoup as bs
from selenium import webdriver
import subprocess
import time
ff = webdriver.Firefox()
pal = []
def pageNext():
    try:
        if ff.find_element_by_class_name('pageNext'):
            return True
        return False
    except:
        return False

def navegate(url=None):
    if url == None:
        url=input("Url: ")
    try:
        ff.get(url)
    except (BrokenPipeError, IOError):
        ff.get(url)

def get_page_html():
    try:
        return ff.page_source
    except (RemoteDisconnected, IOError):
        print('teste')
        return ff.page_source

def parser_html(html):
    return bs(html,'html.parser')

def get_tag_element(source,op=0):
    if op==0:
        tag_name= 'div'#input("tag: ")
        atriute= 'class'#input("atriuto: ")
        element= 'line'#input("elemento: ")
    else:
        tag_name= 'p'
        atriute= ''
        element= ''

    return source.find_all(tag_name,{atriute:element})

def get_list_txt(paragraph):
    ver = False
    lis = []
    # ini = input("paragráfo de início: ")
    # fim = input("paragráfo final: ")

    for p in paragraph:
        if init_par(p.text):
            ver = True
        if end_par(p.text):
            ver = False
        if ver:
            lis.append(p.text)
    return lis

def get_paragraph():
    return get_list_txt(get_tag_element(parser_html(get_page_html()),1))

def splint_list(list_p=[]):
    # tag<p> atriuto,elemento=None
    list_word = []
    for phrase in get_paragraph():
        word = phrase.split()
        list_word.append(word)
    return list_word

def get_links():
    # html.find_all('div',{'class':'line'})
    list_element = []
    links = []
    tag = get_tag_element(parser_html(get_page_html()),0)
    for element in tag:
        list_element.append(element.find_all('a',{'target':'_blank'}))
    for i,l in enumerate(list_element):
        if i%5 == 0:
            links.append(list_element[i][0]['href'])
    return links

def orgnize_list(list_p=[]):
    global pal
    for l in splint_list():
        for p in l:
            pal.append(p)

def exluir_repetidas():
    dic = {}
    for word in pal:
        if word.isalpha():
            dic[word] = 1
    return dic.keys()

def create_dist(caracter,lista=[]):
    for i in lista:
        if i[0] == caracter.upper() or i[0] == caracter.lower():
            print(i)
            subprocess.call('echo '+i+' >> lista_'+caracter.upper()+'.txt',shell=True)

def init_par(text):
    par_ini = ['ABSTRACT','Abstract','Resumen']
    for p in par_ini:
        if p.startswith(text):
            return True

def end_par(text):
    par_fim = ['REFERÊNCIAS','Referencias bibliográficas','Referencias','References','BIBLIOGRAFÍA']
    for p in par_fim:
        if p.startswith(text):
            return True

def google(p):
    navegate('https://translate.google.com/?hl=pt-Br')
    ff.find_element_by_tag_name('textarea').send_keys(p)
    time.sleep(10)
    try:
        sp = ff.find_element_by_id('result_box').text
    except:
        sp = ff.find_element_by_id('result_box').text
    return sp

url_p = "https://search.scielo.org/?q=Qu%C3%ADmica+org%C3%A2nica&lang=pt&count=15&from=1&output=site&sort=&format=summary&fb=&page=1&filter%5Bla%5D%5B%5D=pt&filter%5Bla%5D%5B%5D=en&q=Qu%C3%ADmica+industrial&lang=pt&page=1íde"
if __name__ == '__main__':
    all_links = []
    list_final = []
    navegate(url_p)
    while pageNext():
        for l in get_links():
            all_links.append(l)
        try:
            ff.find_element_by_class_name('pageNext').click()
        except (BrokenPipeError, IOError):
            ff.find_element_by_class_name('pageNext').click()

    for i,l in enumerate(all_links):
        navegate(l)
        orgnize_list()
        print(l,i,len(pal))

    list_final[:] = exluir_repetidas()
    dic = {}
    print('palavra -----> tradução ----> ordem')
    for w in list_final:
        tr = google(w)
        dic[w] = tr
        print(w,dic[w],len(dic))
