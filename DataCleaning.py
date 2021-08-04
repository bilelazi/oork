import requests
import pandas as pd
import mysql.connector
import re
import string
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jobscraper"
)

def clean_text_number1(text):
    text = text.lower()
    text = re.sub('\[.*?\]','',text)
    text = re.sub('[%s]' % re.escape(string.punctuation),'',text)
    text = re.sub('\w*\d\w*','',text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('/', ' ', text)
    text = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", " ", text)
    return text
number1 = lambda x: clean_text_number1(x)


def tokenization(txt):
    tokens = re.split('\W+',txt)
    return tokens
    
    
def remove_sw(txt_tokenized):
    txt_clean = [word for word in txt_tokenized if word not in stopwords]
    return txt_clean
    
def prity1(listdesc):

    string=''
    string = listdesc.description.replace('[' , '')
        
    string = string.replace(']' , '')
    string = string.replace("'" , '')
    string = string.replace(',' , '')

    return string
    
def prity2(listtitle):

    string=''
    string = listtitle.title.replace('[' , '')
        
    string = string.replace(']' , '')
    string = string.replace("'" , '')
    string = string.replace(',' , '')

    return string
    

add_stop_words = ['junior ', 'creativ ', 'techniques ', 'maghreb ', 'employee ', 'opportunity', 'informatiquetélécom ', 'formation ',
                  'avez', 'education', 'dexcellence ', 'centre ', 'sein', 'réaliser ', 'corrective','aagrebaouinetcomgroupco','abderahmane',
                 'abderrafii','abendhiebeticeuropecomnom','abendhiebeticeuropecomtel','abilities','ability','abroadstrong','absorber','abstraction',
                  'واختبار','مناظرةأعلنت','مناظرات','مشفوعة','لانتداب','للس','كك','experience','skills','work','software','solutions','knowledge','bonne',
                 'équipe','projets','ans','formation', 'tests', 'communication' , 'cv' , 'recherche' , 'dune' ,'postuler','technologies',
                  'support','clients' , 'expérience','abstracts', 'academic','academicians','académique','académiques','accelerate','accent','acceptance','acceptanceconstruire',
                  'acceptancefunctional','وتكون','من','فتح','غاية','شفاهيويمكن','ديسمبر','طب','centre', 'creativ', 'dexcellence', 'employee', 'informatiquetélécom', 'junior', 'maghreb',
                  'réaliser', 'techniques','ll', 'neuf', 'qu', 'quelqu', 've', 'abdelkader','able','accepted','acceptéscompétences','access',
                  'accessibility','accessiblesvous','accessoires','accompagne','accompagnement','الوطني','بالملف','بداية','بعد','بفحص','جانفي','خارجي','عن','عون',
                 'accompagner','accompagnez','accompagnons','accompagné','accompanying','accompliespossibilité','accomplir','accord','accordez','according',
                  'إلى','ات','اعلان','التسجيل','التونسي','الحديدي','الشركة','المناظرات','المناظرةالتسجيلcomment','يوم','accordinglyperform','accords','account','accountability','accountable',
                  'accountant','accountmanager','accounts','accro','accrueune','évolutiveprofil','évolutives','évolutivetests','évolutivité','évolué','évènements','êtes','œuvre','œuvreanalyser','œuvremettre',
                 'accueil','accueillir','accurate','accurately','accélerateur','achats','achievable','achieve','achievement','achour','évoluerez','évoluez','évolutif',
                  'évolution','évolutions','évolutionsrédaction','évolutionstests','évolutionsvous','évolutive','évolutivepar',
                 'acknowledged','acquaint','acquis','acquise','acquisition','acquérir','acrobat','act','acted','acteol','étudierexigences','étudié',
                  'évaluation','évaluer','évents','éventuellement','éventuels','évoluant','évoluer','évoluera',
                 'acteolemail','acteur','acteurrices','acteurs','actia','actian','actif','actifcomment','action','actionable','états','étendre','étoffer',
                  'étrangers','étrangerscoordonner','étroite','étude','études','étudiant','étudiants',
                 'actions','activant','active','activedirectory','actively','activement','activementvous','activistes','activiti','activities','équivalentminimum','équivalentune','établie','établies','établir','établissement','établissements','étage','étapes','état',
                  'activitiescustomize','activitiesthe','activity','activité','activités','actualisation','actualisé','actualiséesuivre','actuariat','actuarielles','équipes','équipesi','équipesrôledéveloppeurconsultant','équipestructuré','équipeveuillez','équipevotre',
                  'équipé','équivalent','équivalentdomaine','équivalente',
                  'actuariellesprofil','actuel','actuelle','actuellelea','actuellement','actuelles','actuellesecrire','actuellesspécification','actuels','actuelsassurer','équipemaîtrise','équipements','équipemissions','équipemissionsmettre','équipemotivation',
                  'équipenotre','équipenous','équipeprojet','équiperaisons','équiperigoureux',
                  'acumenthe','adactim','adagos','adapt','adaptablepossibilité','adaptation','adaptativeen','adapter','adaptez','adapting','épicerie','épurer','équipeavantages','équipedes','équipeesprit','équipeetre','équipefrançais','équipeil','équipeinvesti','équipele',
                  'adaptive','adapts','adapté','adaptée','adaptées','adaptés','add','added','addition','additional','émergents','émet','émission','énergie','énergies','énergiques','énergétique','énoncés','épanouir','épaulé',
                  'addixo','address','addressed','adecco','adjoint','adjust','admin','administrates','administrateur','administratif','électrique','électriques','électronique','élevé','élevées','élite','élément','éléments','émail','émergentedévelopper',
                  'administratifprofilformation','administration','administrationstrucutred','administrative','administratives','administrator','administrators','adobe','adonis','éditoriale','éditteur','également','égypt','élaborant','élaboration','élaborer','élaborez','élargi','électricité',
                 'adoption','adossée','adresse','adresser','ads','adsconnaissances','advanced','advancementsalesforce','advantage','écrits','écriture','écritures','écrità','écrivant','éditeur','éditeurs','édition','éditions','éditorial'
                 'advantagegeneral','advantageresponsibilities','adveez','advise','advisor','advisors','advocate','adwordsprescrire','adéquation','écosystèmes','écouter','écrire','écrit','écritcomment','écrite','écriteconviction','écrites','écritevous','écritlieu',
                  'advantagegeneral','adéquats','aetos','affaires','affairespersonnalité','affect','affectation','affecté','affectés','échéanciersexcellente','échéanciersparticipation','échéant','échéantpréparer','éclairé','école','écoles','économie','économique','éditorial',
                  'affiches','affiliation','affiliationmaîtrise','affirmé','afférents','africa','africains','afrique','aftercode','zéro','µservices','âgée','ème','échanger','échangercomment','échanges','échelle','échéances','échéanciers',
                  'age','agena','agence','agencies','agency','agent','agents','agile','agilebases','zaghouan','zarrouk','zeinebbouguerratuneleccomtnville','zend','zendesk','zi','zip','zmq','zone','zones',
                  'agileenvironnement','agileexigences','agileexpérience','agiles','agilescompétences','agilescrum','agilesvous','agilisation','agilité','youfrom','youinclude','youll','young','yourcegid','youre','youth','youths','youwhat','yrs',
                  'agrandir','agreed','agreements','agriculteurs','agricultural','agriculture','agronomes','agréable','agréablecomment','yasmine','year','years','yellow','yesweconnect','yosra','yosrabenabdallahfocuscorporationcomtel','yosrabenabdallahfocuscorporationcomville','yosramaloukitalancom','youan',
                  'agréablesalaire','agréableun','agréableune','agréableêtre','agréé','ahmedalweslatigmailcom','ahrconsulting','ahrconsultingemail','ahrefs','xpath','xquery','xrt','xsl','xtech','xtensus','xtoneo','yahoo','yarn','yarnpour',
                  'aid','aide','aider','aideront','aiding','aidons','aient','aigu','ailleurs','wsdl','wwwhydatiscom','wwwwhitecapetechcom','xapian','xd','xhtml','xml','xmlexperience','xmpp','xp',
                  'aim','aimant','aime','aiment','aimer','aimez','ain','airbus','aisance','writing','writingteam','written','writtencomment','writtennice','writtenskills','writtenteam','writtenverbal','writtenwe','ws',
                  'aisle','aislieu','ajout','ajouter','ajoutée','akouda','al','alain','worldclass','worlds','worldto','worldwide','worldwideemail','wp','wpf','write','writers',
                  'albeasworkplace','aleia','alentours','alerte','alerter','algorithmescode','works','workshop','workshopmeetup','workshops','workspace','workvalues','world','worldwide','worldwideemail']

stopwords = list(fr_stop) + list(en_stop) + list(add_stop_words)    
    
    
    
# # importing data from the DB
def jobsoffers():
    # # Cleaning Jora DF
    listjobs=[]
    mycursor= mydb.cursor()
    req=""" SELECT * from jobsoffers"""
    mycursor.execute(req)
    result=mycursor.fetchall()
    if(mycursor.rowcount > 0):
        for res in result:
            dict={
                'id':res[0],
                'link':res[1],
                'title':res[2],
                'description':res[3],
                'date':res[4],
                
            }
            listjobs.append(dict) 
    return listjobs            
def cleaningg():       
    df=pd.DataFrame(jobsoffers())
    df.drop({'date','link'},
      axis='columns', inplace=True)
    jobs=df
    clean_desc = pd.DataFrame(jobs.description.apply(number1))
    clean_title = pd.DataFrame(jobs.title.apply(number1))
    jobs['description']=clean_desc
    jobs['title']=clean_title
    jobs['desc_clean_tokenized'] = jobs['description'].apply(lambda x: tokenization(x.lower()))
    jobs['title_clean_tokenized'] = jobs['title'].apply(lambda x: tokenization(x.lower()))
    jobs['desc_no_sw'] = jobs['desc_clean_tokenized'].apply(lambda x: remove_sw(x))
    jobs['title_no_sw'] = jobs['title_clean_tokenized'].apply(lambda x: remove_sw(x))
    jobs['description'] = jobs['desc_no_sw']
    jobs['title'] = jobs['title_no_sw']
    jobs.drop({'desc_clean_tokenized','desc_no_sw','title_clean_tokenized','title_no_sw'} , axis='columns', inplace=True)
    jobs['description']=jobs['description'].apply(str)
    jobs['title']=jobs['title'].apply(str)
    jobs['description'] = jobs.apply(prity1 , axis=1)
    jobs['title'] = jobs.apply(prity2 , axis=1)
    list = jobs.values.tolist()
    mycursor= mydb.cursor()
    for l in list:
        req=""" update jobsoffers set title = %s, description = %s where id = %s"""
        val=(l[1],l[2],l[0])
        mycursor.execute(req, val)
        mydb.commit()


