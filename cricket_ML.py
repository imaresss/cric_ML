import requests
from bs4 import BeautifulSoup
import urllib
import re
from nltk.corpus import wordnet
import pandas as p

df = p.DataFrame(columns =['Batsman_Name','Over','Bowler_Name','Batsman_country','Bowler_country','Score','Run_rate','Match_time','Type_of_pitch','Type_of_Bowler',
                            'Type_of_Batsman' ,'Bowling_area', 'Batting_area' , 'Wickets','Result'
                           ])



indian_player_bat = {'Dhawan':'Left_Hand_Batsman','Rohit':'Right_Hand_Batsman','Suresh Raina':'Left_Hand_Batsman',
'Kohli':'Right_Hand_Batsman','Manish Pandey':'Right_Hand_Batsman','Dhoni':'Right_Hand_Batsman','Hardik Pandya':'Right_Hand_Batsman',
                 'Bhuvneshwar':'Right_Hand_Batsman' , 'Jasprit Bumrah':'Right_Hand_Batsman','Kuldeep Yadav':'Left_Hand_Batsman',
                 'Yuzvendra Chahal':'Right_Hand_Batsman' ,'Mohammed Shami':'Right_Hand_Batsman', 'Rahane':'Right_Hand_Batsman','Kedar Jadhav':'Right_Hand_Batsman', 'Dinesh Karthik':'Right_Hand_Batsman',
                 'Shreyas Iyer':'Right_Hand_Batsman','Axar Patel':'Left_Hand_Batsman'
                 }
indian_player_bowl ={'Bhuvneshwar':'Right_arm_medium' , 'Bumrah':'Right_arm_medium' , 'Kuldeep Yadav':'Left_arm_chinaman', 'Chahal':'Right_arm_legbreak' ,
                     'Mohammed Shami':'Right_arm_medium', 'Shardul Thakur':'Right_arm_medium',
                    'Axar Patel':'Left_arm_orthodox' , 'Kedar Jadhav':'Right_arm_offbreak' , 'Hardik Pandya':'Right_arm_medium'
                    }

south_africa_player_bat = {'Zondo':'Right_Hand_Batsman','Shamsi':'Right_Hand_Batsman','Amla':'Right_Hand_Batsman' , 'de Kock':'Left_Hand_Batsman', 'du Plessis':'Right_Hand_Batsman' , 'Markram':'Right_Hand_Batsman' , 'Duminy':'Left_Hand_Batsman' , 'Miller':'Left_Hand_Batsman',
                        'Chris Morris':'Right_Hand_Batsman' , 'Phehlukwayo':'Left_Hand_Batsman' , 'Rabada':'Left_Hand_Batsman' , 'Morne Morkel':'Left_Hand_Batsman' , 'Tahir':'Right_Hand_Batsman'
                           }

south_africa_player_bowl ={'Zondo':'Right_arm_offbreak','Shamsi':'Left_arm_chinaman','Chris Morris':'Right_arm_medium' , 'Phehlukwayo':'Right_arm_medium'
                           , 'Rabada':'Right_arm_fast',  'Morkel':'Right_arm_fast' ,'Duminy':'Right_arm_offbreak' ,
                           'Tahir' :'Right_arm_legbreak', 'Lungi Ngidi':'Right_arm_fast'}


fielding_positions = ['deep point','deepish point' , 'mid-off' ,'deep square leg' ,'off-side'
                      , 'deep at cover' , 'cover','deep cover' ,'deep extra-cover', 'gully','square','long-off','long-on',
                      'extra-cover','to the bowler','silly point','slip','fine leg','short leg', 'defend' ,'off-side'
                      ,'third man'  ,'on-side',
                     'cover', 'fine leg' ,'deep at cover' ,'mid-wicket', 'deep point' ,
                     'mid-on' ,'sweeper cover' ,'long-on', 'deep square leg' ,'point' ,'long-off',
                     'deep shortward point', 'mid-wicket', 'deep extra-cover', 'extra-cover',
                     'shortcover' ,'deep shortward square', 'leave', 'short cover' ,'sweep',
                     'stumped', 'deep mid-wicket', 'silly point', 'outside-off' ]

types_of_delivery = ["leg-cutter","wrong'un","off-break",'leg-side','length ball','length delivery','on pads','back of a length','short and wide','leg-break'
                     ,'in-ducking','full toss','googly','short in length','flatter delivery','outside off stump','full-toss'
                     ,'yorker','quick delivery','length ball outside off','short of length','short ball','short outside off','inswinger','short',
                     'length ball off stump', 'short of a length off stump','length ball on stump' ,'short of a length' ,'flatter delivery',
                   'short of a length outside off', 'length ball outside off' ,'pitched up','length ball' ,'wide delivery' ,'fuller delivery' ,
                 'fuller delivery outside off', 'short' ,'bounce' ,'inswinger' ,'straighter delivery' ,'onto the stump' ,'flight delivery','full toss' ,
                     'slow delivery', 'toss up','tosses up', 'tossed up','googly' ,'turning away' ,'turning in', 'short and slow' ,'low delivery',
 'short and spining in' ,'spin', 'flatter delivery outside off',
 'short and outside off', 'tossed up outside off' ,'yorker','tossed up leg break' ,
 'length ball middle stump' ,'turning in ', 'shortand outside off',
 'toss up outside off', 'full toss outside off','outside off','off stump'
                     ]

#################################  PITCH REPORT  #######################################
#########  Might not be of any use ########################################
##url = "https://m.cricbuzz.com/cricket-commentary/19160/rsa-vs-ind-1st-odi-india-tour-of-south-africa-2017-18/36"
##response = requests.get(url)
##html = response.text
##soup = BeautifulSoup(html,"html.parser")
##
##the_text = soup
##you_pitch = str(the_text).split("What to expect:")[1].split("<br/>")[0]
##you_pitch = str.lower(you_pitch)
##print(you_pitch)
##
##if wordnet.synsets("solid")[0].lemmas()[0].name()or wordnet.synsets("moisture")[0].lemmas()[0].name() in you_pitch:
##    pitch_report = "Dead_pitches"
##elif wordnet.synsets("soft")[0].lemmas()[0].name()or wordnet.synsets("clay")[0].lemmas()[0].name() in you_pitch:
##    pitch_report = "Dusty_pitches"
##else:
##    pitch_report = "Grassy_pitche"
##print(pitch_report)

############################################################################
def check_after (bowling_area , text):
    if 'outside off' in text :
        return ' outside off'
    elif any(c in text for c in ('off stump','off')):
        return ' off stump'
    elif any(c in text for c in ('leg side' ,'on stump' ,'leg','leggie')):
        return ' on stump'
    
    else :return ''
    
def check_four_six(runs):

    if 'four' in runs :
        return int(4)
    elif 'six' in runs:
        return int(6)
    elif 'out' in runs:
        return int(-1)
    else:
        return 0


ans=0
out =0
conclude=0
for i in range(33,14,-1):
    
    url = "https://m.cricbuzz.com/cricket-commentary/19162/rsa-vs-ind-3rd-odi-india-tour-of-south-africa-2017-18/"+str(i)
    print(i)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")
    the_text = soup.find_all("p",class_="commtext")
    
##    print(str(the_text[0])[20:24])
##    all_ball= re.findall(r'\d\.\d' , str(the_text))
##    the_text = str.lower(str(the_text))
    
    for each in reversed(the_text):
        split =str(each).split('<p class="commtext">')[1]
        
        if split[0].isdigit():
            
            over =str(each)[20:24].strip()
            runs = str(each).split(over)[1].split(",")[1].split(',')[0].strip()
            bowler = str(each).split(over)[1].split(",")[0].split("to")[0].strip()
            batsman = str(each).split(over)[1].split(",")[0].split("to")[1].strip()
            batting_area =''
            bowling_area =''
            text = str(each).split(over)[1].strip()
            for bat_pos in fielding_positions:
                
                if bat_pos in text:
 
                    batting_area = bat_pos

                    break
            
            if any(c in text for c in ("short of a length","short of a good length", "back of a length","back of length","short of length")):
     
                bowling_area ='short of a length'
                bowling_area += check_after(bowling_area , text)
                
            elif  any(c in text for c in ("fuller", "full length","full")):
                bowling_area ='fuller delivery'
            elif any(c in text for c in ("good length", "length ball","length delivery")):
                bowling_area ='length ball'
                bowling_area += check_after(bowling_area , text)
            elif 'straight'in text:
                bowling_area ='straighter delivery'
                bowling_area += check_after(bowling_area , text)
            elif any(c in text for c in ("quicker","quick delivery","quick ball","flatter", "flat length")):
                bowling_area ='flatter delivery'
                bowling_area += check_after(bowling_area , text)
            elif any(c in text for c in ("tossed up","tosses up","toss up","tosses")):
                bowling_area ='toss up'
                bowling_area += check_after(bowling_area , text)
            elif any(c in text for c in ("flight","flighted")):
                bowling_area ='flight delivery'
                bowling_area += check_after(bowling_area , text)
            elif any(c in text for c in ("slow","slower" ,"slows")):
                bowling_area ='slow delivery'
                bowling_area += check_after(bowling_area , text)
               
            else:
                for bowl_pos in types_of_delivery:
                

                    if bowl_pos in str(each).split(over)[1].strip():
 
                        bowling_area = bowl_pos
                        break
            
##            print(runs)
            if '<b>' in runs:
                result = runs.split('<b>')[1].split('</b>')[0]
                result= str.lower(result)
                print(result)
                conclude = check_four_six(result)
                if conclude == -1:
                    out+=1
                else:
                    ans += conclude
            elif re.match(r'\d' , str(runs)):
                conclude = runs.split('run')[0].strip()
                
                ans+=int(conclude)
            else :
                conclude=0
                ans+=0
            rate = over.split(".")
            rate1 = int(rate[0])*6 + int(rate[1])
            run_rate = (ans/rate1)*6

                        
##            print(over, " and ",u)        
        

            df =df.append({'Batsman_Name': batsman ,'Over' : over , 'Bowler_Name': bowler , 'Batsman_country':"India" , 'Bowler_country':'South Africa',
                   'Score':ans , 'Run_rate':run_rate , 'Match_time': "Day" , 'Type_of_pitch':'Hard','Type_of_Bowler':south_africa_player_bowl[bowler],
                       'Type_of_Batsman':indian_player_bat[batsman] , 'Bowling_area':bowling_area, 'Batting_area':batting_area , 'Wickets':out , 'Result':conclude

                        
                },ignore_index =True)


save ="cricket_dataset_3rd_odi.csv"
df.to_csv(save)


