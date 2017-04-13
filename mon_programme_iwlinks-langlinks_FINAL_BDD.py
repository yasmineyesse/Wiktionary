import json                     # encoder et de décoder des infos json
import os
import urllib.request           # Lire une page web
import webbrowser               # Ouvrir l'URL pour m'assurer : #webbrowser.open(mon_url)
import sqlite3        
               

# Mon programme en Python
# 1) Lister tous les fichiers d'un répertoire : verbes_francais

fichiers = os.listdir("C://Program Files (x86)/EasyPHP-12.1/www/my portable files/Wiktionnaire_Francais_FINAL/json_verbes")


## CREER BASE DE DONNEES
import sqlite3
conn = sqlite3.connect('dictionnaire2.db')
## CREER TABLE
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS dictionnaire2(
    id_title1 TEXT,
    title1 TEXT,
    title2 TEXT,
    title3 TEXT
    )
    """)
conn.commit()
    
print("Le dictionnaire ")
print("Mot source <==============> IWLINKS <===============> LANGLINKS")
nombre_fichiers = len(os.listdir('C://Program Files (x86)/EasyPHP-12.1/www/my portable files/Wiktionnaire_Francais_FINAL/json_verbes'))

for i in range(0,nombre_fichiers-1):
        fichier_json = open('C:/Program Files (x86)/EasyPHP-12.1/www/my portable files/Wiktionnaire_Francais_FINAL/json_verbes/donnees_francais_%s.json'% i, 'r', encoding='utf-8')
        #print(fichier_json)
                
        #2) Lire le fichier JSON sous Python et le parser
        with fichier_json as fichier:
           data = json.load(fichier)                    # load décode un fichier json
           
        # liste des URL
        liste = []
        liste_pageids = []
        # mettre tous les pageid dans pageid
        for datum in data['query']['categorymembers']:
            pageids_0 = datum['pageid']
            mon_url = "https://fr.wiktionary.org/w/api.php?action=query&prop=iwlinks|langlinks&iwprefix=en&llprop=url&lllang=en&utf8&format=json&pageids=%s" % (pageids_0)
            
            liste.append(mon_url)
            liste_pageids.append(pageids_0)
            # Afficher l'URL iwlinks + langlinks 
            #webbrowser.open(mon_url)
            
        # 6) Récupérer le mot traduit
        ### 1) Lien interne : Faire un test si iwlinks existe ?

        # Lire
       
        for i in liste:
                with urllib.request.urlopen(i) as url:
                        datas = json.loads(url.read().decode("utf8"))
                        for i in datas["query"]["pages"]:
                                try: # si i existe! 
                                    #print("la clé existe :)") 
                                    title1 = datas["query"]['pages'][i]["title"]
                                    #print(datas)
                                    pageid = str(datas["query"]['pages'][i]["pageid"])
                                    
                                    key = "langlinks"
                                    try:
                                        title3 = datas["query"]['pages'][i]["langlinks"][0]["url"]

                                        tab = title3.split('https://en.wiktionary.org/wiki/')
                                        title = tab[1]
                                        #print(title)
                    
                                        # PARTIE LANGLINKS

                                        url_langlinks = "https://en.wiktionary.org/w/api.php?action=query&prop=extracts&format=json&utf8&explaintext&titles=%s"% title
                                        #webbrowser.open(url_langlinks)
                                        #print(url_langlinks)
                                        with urllib.request.urlopen(url_langlinks) as url:
                                            data = json.loads(url.read().decode("utf8"))
                                            #print(datas)

                                            # PARSER EXTRACTS 
                                            
                                            for j in data["query"]['pages']:   ## Renommer l'indice
                                                    string = str(data["query"]['pages'][j]["extract"])
                                                    tab = string.split('=== Verb ===\n'+title1)
                                                    string1 = tab[1]
                                                    
                                                    tab1 = string1.split('\n')
                                                    title_lang = tab1[1]
                                        #print(title_lang)

                                    except:
                                        title3 = 'None'
                                        title_lang = 'None'
                                        #print("langlinks n'y est pas!")


                                   #key2 = "iwlinks"
                                    #try:
                                    #    title2 = datas["query"]['pages'][i]["iwlinks"][0]["*"]"""
                                   
                                   # stocker iwlinks dans une chaîne séparée par , 
                                    title2 = ''
                                    key2 = "iwlinks"
                                    try:
                                        liste = datas["query"]['pages'][i]["iwlinks"]
                                        for i in liste:
                                           #i = i+1
                                           a = i["*"] +','
                                           title2 += a
                                        #print(title2)
                                        #print('\n')


                                 
                                    except:
                                        title2 = 'None'
                                        #print("iwlinks n'y est pas!")


                                    
                                except KeyError:
                                    #print("la clé n'existe pas !!!!")
                                    pass
                                
                                print(title1+"<=============>"+title2+"<==================>"+title_lang)
                                # Insérer seulement les données traduites
                                if title2 != 'None' or title_lang != 'None':
                                    ## INSERER DONNEES
                                    c.execute(""" INSERT INTO dictionnaire2(id_title1, title1, title2, title3)
                                     VALUES(?,?,?,?)""", (pageid ,title1, title2, title_lang))
                                    conn.commit()
                                
conn.close()                           
                           
