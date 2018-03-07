import requests
from bs4 import BeautifulSoup
import urllib
import re
from nltk.corpus import wordnet
import pandas as p

import urllib.request, json 
df = p.DataFrame(columns =['Batsman_Name','Over','Bowler_Name','Batsman_country','Bowler_country','Score','Run_rate','Match_time','Type_of_pitch','Type_of_Bowler',
                            'Type_of_Batsman' ,'Bowling_area', 'Batting_area' , 'Wickets','Result'
                           ])

fielding_positions = ['deep point','deepish point' , 'mid-off' ,'deep square leg' ,'off-side'
                      , 'deep at cover' , 'cover','deep cover' ,'deep extra-cover', 'gully','square','long-off','long-on',
                      'extra-cover','to the bowler','silly point','slip','fine leg','short leg', 'defend' ,'off-side'
                      ,'third man'  ,'on-side','long leg','deep mid-wicket',
                     'cover', 'fine leg' ,'deep at cover' ,'mid-wicket', 'deep point' ,
                     'mid-on' ,'sweeper cover' ,'long-on' ,'point' ,'long-off','long stop'
                     'deep shortward point', 'mid-wicket', 'deep extra-cover', 'extra-cover',
                     'shortcover' ,'deep shortward square', 'leave', 'short cover' ,'sweep',
                     'stumped',  'silly point', 'outside-off' ]

types_of_delivery = ["over-pitched","leg-cutter","wrong'un","off-break",'leg-side','length ball','length delivery','on pads','back of a length','short and wide','leg-break'
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
indian_player_bat = {'Dhawan':'Left_Hand_Batsman','Rohit':'Right_Hand_Batsman','Suresh Raina':'Left_Hand_Batsman',
'Kohli':'Right_Hand_Batsman','Manish Pandey':'Right_Hand_Batsman','Dhoni':'Right_Hand_Batsman','Hardik Pandya':'Right_Hand_Batsman',
                 'Bhuvneshwar':'Right_Hand_Batsman' , 'Jasprit Bumrah':'Right_Hand_Batsman','Kuldeep Yadav':'Left_Hand_Batsman',
                 'Yuzvendra Chahal':'Right_Hand_Batsman' ,'Mohammed Shami':'Right_Hand_Batsman', 'Rahane':'Right_Hand_Batsman','Kedar Jadhav':'Right_Hand_Batsman', 'Dinesh Karthik':'Right_Hand_Batsman',
                 'Shreyas Iyer':'Right_Hand_Batsman','Axar Patel':'Left_Hand_Batsman'
                 }
indian_player_bowl ={'Bhuvneshwar Kumar':'Right_arm_medium' , 'Jasprit Bumrah':'Right_arm_medium' , 'Kuldeep Yadav':'Left_arm_chinaman', 'Yuzvendra Chahal':'Right_arm_legbreak' ,
                     'Mohammed Shami':'Right_arm_medium', 'Shardul Thakur':'Right_arm_medium',
                    'Axar Patel':'Left_arm_orthodox' , 'Kedar Jadhav':'Right_arm_offbreak' , 'Hardik Pandya':'Right_arm_medium'
                    }

south_africa_player_bat = {'Khaya Zondo':'Right_Hand_Batsman','Tabraiz Shamsi':'Right_Hand_Batsman','Hashim Amla':'Right_Hand_Batsman' , 'Quinton de Kock':'Left_Hand_Batsman', 'Faf du Plessis':'Right_Hand_Batsman' , 'Aiden Markram':'Right_Hand_Batsman' , 'Jean-Paul Duminy':'Left_Hand_Batsman' , 'David Miller':'Left_Hand_Batsman',
                        'Chris Morris':'Right_Hand_Batsman' , 'Andile Phehlukwayo':'Left_Hand_Batsman' , 'Kagiso Rabada':'Left_Hand_Batsman' , 'Morne Morkel':'Left_Hand_Batsman' , 'Imran Tahir':'Right_Hand_Batsman'
                           }

south_africa_player_bowl ={'Zondo':'Right_arm_offbreak','Shamsi':'Left_arm_chinaman','Chris Morris':'Right_arm_medium' , 'Phehlukwayo':'Right_arm_medium'
                           , 'Rabada':'Right_arm_fast',  'Morkel':'Right_arm_fast' ,'Duminy':'Right_arm_offbreak' ,
                           'Tahir' :'Right_arm_legbreak', 'Lungi Ngidi':'Right_arm_fast'}

def check_after (bowling_area , text):
    if 'outside off' in text :
        return ' outside off'
    elif any(c in text for c in ('off stump','off')):
        return ' off stump'
    elif any(c in text for c in ('leg side' ,'on stump' ,'leg','leggie')):
        return ' on stump'
    
    else :return ''
    
batting_area =""
bowling_area=""
for i in range(1,9,1):
    ##1st odi link ################
    ##http://site.api.espn.com/apis/site/v2/sports/cricket/18065/playbyplay?contentorigin=espn&event=1122279&page=8&period=1&section=cricinfo
    with urllib.request.urlopen("http://site.api.espn.com/apis/site/v2/sports/cricket/18065/playbyplay?contentorigin=espn&event=1122280&page="+str(i)+"&period=1&section=cricinfo") as url:
        data = json.loads(url.read().decode())
        items = len(data["commentary"]["items"])

    for i in range(0,items,1):
        print(data["commentary"]["items"][i]["over"]["overs"])
        commentary = data["commentary"]["items"][i]["text"]
        for bat_pos in fielding_positions:
            if bat_pos in commentary:
                batting_area = bat_pos
                break

        if any(c in commentary for c in ("short of a length","short of a good length", "back of a length","back of length","short of length")):
 
            bowling_area ='short of a length'
            bowling_area += check_after(bowling_area , commentary)
            
        elif  any(c in commentary for c in ("fuller", "full length","full")):
            bowling_area ='fuller delivery'
        elif any(c in commentary for c in ("good length", "length ball","length delivery")):
            bowling_area ='length ball'
            bowling_area += check_after(bowling_area , commentary)
        elif 'straight'in commentary:
            bowling_area ='straighter delivery'
            bowling_area += check_after(bowling_area , commentary)
        elif any(c in commentary for c in ("quicker","quick delivery","quick ball","flatter", "flat length")):
            bowling_area ='flatter delivery'
            bowling_area += check_after(bowling_area , commentary)
        elif any(c in commentary for c in ("tossed up","tosses up","toss up","tosses")):
            bowling_area ='toss up'
            bowling_area += check_after(bowling_area , commentary)
        elif any(c in commentary for c in ("flight","flighted")):
            bowling_area ='flight delivery'
            bowling_area += check_after(bowling_area , commentary)
        elif any(c in commentary for c in ("slow","slower" ,"slows")):
            bowling_area ='slow delivery'
            bowling_area += check_after(bowling_area , commentary)                
        elif any(c in commentary for c in ("over-pitched","over-pitch")):
            bowling_area ='over-pitch'
            bowling_area += check_after(bowling_area , commentary)
            
        else:
            for bowl_pos in types_of_delivery:
                if bowl_pos in commentary:
                    bowling_area = bowl_pos
                    break
    
        
        batsman = data["commentary"]["items"][i]["batsman"]["athlete"]["name"]
        bowler = data["commentary"]["items"][i]["bowler"]["athlete"]["name"]
        ans = data["commentary"]["items"][i]["homeScore"]
        conclude = data["commentary"]["items"][i]["scoreValue"]
        if data["commentary"]["items"][i]["dismissal"]["dismissal"] == True:
            conclude = -1
        run_rate = data["commentary"]["items"][i]["innings"]["runRate"]
        over =data["commentary"]["items"][i]["over"]["overs"]
        wickets = data["commentary"]["items"][i]["innings"]["wickets"]
        df =df.append({'Batsman_Name': batsman ,'Over' : over , 'Bowler_Name': bowler , 'Batsman_country':"India" , 'Bowler_country':'South Africa',
                   'Score':ans , 'Run_rate':run_rate , 'Match_time': "Day" , 'Type_of_pitch':'Hard','Type_of_Bowler':indian_player_bowl[bowler],
                       'Type_of_Batsman':south_africa_player_bat[batsman] , 'Bowling_area':bowling_area, 'Batting_area':batting_area , 'Wickets':wickets , 'Result':conclude

                        
                },ignore_index =True)
                                                  
save ="cric_espn_dataset2nd_odi.csv"
df.to_csv(save)

