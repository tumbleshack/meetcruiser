#!/Users/Brandon/Documents/meetcruiser/venv/bin/python3

import re
import sys
import json
import codecs
import fitz  # http://pymupdf.readthedocs.io/en/latest/

#from EventHeat import *
#from Meet import *

#import firebase_admin
#from firebase_admin import credentials, firestore

"""
def fixtime(time):
    it = iter(time)
    newtime=""
    while True:
        char = next(it, None)
        if char is None:
            return(newtime)
        if ord(char) > 255:
            char=":"
        newtime=newtime+char
        print(char, ord(char))


def utfy_dict(dic):
    if isinstance(dic,unicode):
        return(dic.encode("utf-8"))
    elif isinstance(dic,dict):
        for key in dic:
            dic[key] = utfy_dict(dic[key])
        return(dic)
    elif isinstance(dic,list):
        new_l = []
        for e in dic:
            new_l.append(utfy_dict(e))
        return(new_l)
    else:
        return(dic)

def serialize(obj):

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


eventHeatList = []

event=[[0,0,0,0,0,0,0]]
prevDist="0"
prevStroke="None"
heat=[0] * 2
prevHeat=list(heat)

eventString=""
heatString=""

relay=False
lastHeat=False
combine=False

startNo=0

lane=0
prevLane=0

"""

heatSheet=sys.argv[1]
output=heatSheet.replace("pdf","json.txt")
pdf = fitz.open(heatSheet)

mode=""
for page_index in range(pdf.page_count):
    print(" ====================================================== page: ", page_index)
    page = pdf[page_index]
    heatSheetData = page.get_text('dict')

    for block in heatSheetData['blocks']:
        text_values=[]
        block_lines=len(block['lines'])
        for line in block['lines']:
            for span in line['spans']:
                text_values.append(span['text'])

        if block_lines == 1:
            if text_values[0].startswith('#'):
                mode="event"
                print("Event        >", text_values[0])
            elif text_values[0].startswith('Heat'):
                mode="heat "
                print("Heat           >", text_values[0])
            elif mode == "membr" or mode == "entry":
                print("Relay Swim  !1",mode,">", text_values)
            else:
                print("other 1    ",mode,">", text_values )

        elif block_lines == 4:
            mode="entry"
            print("Indv/Team   ",mode,">", text_values)
        elif block_lines == 2:
            mode="membr"
            print("Relay Swim    ",mode,">", text_values)
        else:
            print("other:      ",mode,">",block_lines,text_values)

        continue

"""
        try:
            print(block['lines'][2]['spans'][0]['text'])
            #if 'Jabbar' in block['lines'][2]['spans'][0]['text']:
            #    block['lines'].pop(2)
            #    print('yes!')
            #if 'Matthew' in block['lines'][2]['spans'][0]['text']:
            #    block['lines'].pop(2)
            #    print('yes!')
        except:
            print('no')

        print(len(block['lines']))
        print("lines: ",len(block['lines']))
        blockLines = (block['lines'])
        blockLineCount=len(blockLines)

        line = []
        for i in range(blockLineCount):
            line.append(block['lines'][i]['spans'][0]['text'])

        print("line:",line)
        print("line0:",line[0])

        if blockLineCount==5 and ("Team" in line[1] or "Seed Time" in line[4] ):
            print("CONTINUING")
            continue

        if blockLineCount==3 and "Heat Sheet" in line[0]:
            print("CONTINUING")
            continue

        print("still looping")
        name=""
        time=""
        club=""
        age=""
        lastTopic=""
        process=True

        print("blockLineCount",blockLineCount,line[0])
        if blockLineCount==1 and "#" in line[0] and "(" not in line[0] and "with" not in line[0]:
            line[0] = line[0].replace("yd"," Yard")
            print("Event line >"+line[0]+"<");

            try:
                print(event[0])
                prevDist = event[0][4]
                prevStroke = event[0][6]
                prevUnits = event[0][5]
            except:
                print("something fishy")
                print(sys.exc_info()[0])
                print(block)

            if 'Under' in line[0] or 'Over' in line[0]:
                print("over/under")
                event = re.findall('^#(\d+) (\w+) (\d+) & (Under|Over) (\d+) (Yard|LC Meter) (\w+) ?(\w+)?',line[0])
                try:
                    relay = event[0][7] == "Relay"
                except:
                    print("the error happened here")
                    print(sys.exc_info()[0])
                    print(block)
            else:
                event = re.findall('^#(\d+) (\w+) (\d+)-(\d+) (\d+) (Yard|LC Meter) (\w+) ?(\w+)?',line[0])
                try:
                    relay = event[0][7] == "Relay"
                except:
                    print("the error happened at this one")
                    print("Event:",event)
                    print(sys.exc_info()[0])
                    print("Block:",block)

            print(" ** event ** ", event[0], relay)

            lastTopic="Event"


        elif "Heat" in line[0]:

            if heatString != "":
                if combine:
                    print(" + ",end = "")
                    print(heatString, end="")
                else:
                    print("")
                    startNo+=1
                    print(startNo, heatString, end="")
                combine=False

            print(" entry ",name,time,club,lane)

            prevHeat = list(heat)
            if "of" in line[0]:
                heat = re.findall('Heat *(\d+) of (\d+)',line[0])
            else:
                heat = re.findall('Heat *(\d+) *\(#',line[0])
            lastHeat=True
            print(" ** heat ** ", heat)
            print(" heat ",heat[0][0])

            try:
                heatString = "#" + event[0][0] + ", heat "+heat[0][0]
                print('heatString='+heatString)
                evtHt = EventHeat(
                    event[0][0]
                    ,heat[0][0]
                    ,event[0][1]
                    ,event[0][2]+"-"+event[0][3]
                    ,event[0][4]
                    ,event[0][6]
                    ,relay
                )
                eventHeatList.append(evtHt)
            except:
                print("something going on")
                print(sys.exc_info()[0])
                print(block)

            lastTopic="Heat"

            print('line count:',len(line))

            if len(line) > 1:

                line.pop(0)

                print(line)
                if len(line) == 3:
                    new = []
                    new.append(line[0])
                    new.append(" ".join(line[1].split(" ",-2)[:2]))
                    new.append(" ".join(line[1].split(" ",-2)[2:]))
                    new.append(line[2])
                    line=new
                    print(line)
                    

                #if relay:
                #    print('Heat - relay')
                #    name = line[0]
                #    time = line[1]
                #    club = line[2]
                #    prevLane = lane
                #    lane = int(line[3])
                #    print(lane, name, club, time, age)
                #    evtHt.addEntry(lane, name, club, time, age)
                #else:
                print('Heat - not relay')
                club = line[2].split(' ')[1]
                time = line[3]
                age = line[2].split(' ')[0]
                name = line[1]
                prevLane = lane
                lane = int(line[0])
                print('Entry:', lane, name, club, time, age)
                time=fixtime(time)
                evtHt.addEntry(lane, name, club, time, age)

                if lastHeat:
                    print ("CHECK **: ", event[0][4], event[0][6], prevDist, prevStroke, lane, prevLane)
                    try:
                        if prevDist == event[0][4] and prevStroke == event[0][6] and lane == prevLane+1:
                            combine=True
                    except:
                        print("problems going down")
                        print(sys.exc_info()[0])
                        print(block)
                    lastHeat=False

                lastTopic="Entry"


        elif blockLineCount == 4 and relay: 
            #new: ['2', 'Whitewater Creek', 'A WWCS', '3:24.94']
            #old: ['B', 'NT', 'KHCA', '2']

            print('4 relay - here')
            name = line[2].split(' ')[0]
            time = line[3]
            club = line[2].split(' ')[1]
            prevLane = lane
            lane = int(line[0])
            print('Entry:', lane, name, club, time, age)
            time=fixtime(time)
            evtHt.addEntry(lane, name, club, time, age)

            if lastHeat:
                print ("CHECK **: ", event[0][4], event[0][6], prevDist, prevStroke, lane, prevLane)
                if prevDist == event[0][4] and prevStroke == event[0][6] and lane == prevLane+1:
                    combine=True
                lastHeat=False

            lastTopic="Entry"

        elif blockLineCount == 4 and not relay:
            #new ['1', 'Smith, Anna Kat', '6 WWCS', '1:11.07']#

            print('4 not relay - no, here')
            club = line[2].split(' ')[1]
            time = line[3]
            age = line[2].split(' ')[0]
            name = line[1]
            prevLane = lane
            lane = int(line[0])
            print('Entry:', lane, name, club, time, age)
            time=fixtime(time)
            evtHt.addEntry(lane, name, club, time, age)

            if lastHeat:
                print ("CHECK **: ", event[0][4], event[0][6], prevDist, prevStroke, lane, prevLane)
                try:
                    if prevDist == event[0][4] and prevStroke == event[0][6] and lane == prevLane+1:
                        combine=True
                except:
                    print("problems going down")
                    print(sys.exc_info()[0])
                    print(block)
                lastHeat=False

            lastTopic="Entry"

        else:
             process=False


#if combine:
#    print(" + ",end = "")
#else:
#    print("")

print(heatString)

pdf.close()

last=-1
starts=[]
startNo=0


for evtHt in eventHeatList:


    print(evtHt.event+": "+evtHt.heat, evtHt.firstLane(),evtHt.lastLane())

    if last+1 == evtHt.firstLane():
        starts[startNo-1].append(evtHt)
        print("Combine")

    else: 
        start=[]
        start.append(evtHt)
        starts.append(start)
        startNo+=1

    last = evtHt.lastLane()


meet = Meet("Whitewater at Kedron Hills")

for i, start in enumerate(starts):
    print("Start: ", i+1,"  ", end="")

    meet.newStart()
    #print(meet)

    max=0
    for event in start:
        max = (event.maxTime() if event.maxTime() > max else max)
    print("{:5.2f}".format(max))

    for event in start:
        print("    Event {} heat {}: {} {} {} Yard {} {:5.2f}; {}".format(
            event.event
            ,event.heat
            ,event.sex
            ,event.age
            ,event.yards
            ,event.stroke
            ,event.maxTime()
            ,("Relay" if event.relay else "")
        ))
        theHeat = meet.addHeat(event.event,event.heat,event.sex,event.age,event.yards,event.stroke,int(event.relay),event.maxTime())

        print("meet")
        #print(meet)

        print("type of theHeat")
        print(type(theHeat))

        print("theHeat")
        print(theHeat)

        for lane in sorted(event.entry.keys()):
            print("      {0:2}: {1:20} {2:8} {3:7} {4:5.2f}".format(
                lane
                ,event.entry[lane]['name']
                ,event.entry[lane]['club']
                ,event.entry[lane]['time']
                ,event.entry[lane]['timeSec']
            ))
            theHeat.addEntry(lane,event.entry[lane]['name'],event.entry[lane]['club'],event.entry[lane]['age'],event.entry[lane]['timeSec'])


print("Python Dictionary")
print(meet)
print(" ")

with open(output, 'w') as f1:
    json.dump(meet,f1, ensure_ascii=False,default=lambda x: x.__dict__)

#with open('data2.txt', 'wb') as f2:
#    json.dump(meet,codecs.getwriter('utf-8')(f2), ensure_ascii=False,default=lambda x: x.__dict__)

myjson = json.dumps(meet,ensure_ascii=False,default=lambda x: x.__dict__)
print("JSON string")
print(myjson)
print(" ")

m = json.loads(myjson).items()
print("Rebuilt Python Dictionary")
print(m)
print(" ")


#cred = credentials.Certificate("meet-status-firebase-adminsdk-gvb0j-edcdbe6c3b.json")
#app = firebase_admin.initialize_app(cred)

#db = firestore.client()
#db.collection(u'swim_test').document(u'whitewater2').set({u"opponent": u"Whitewater", u"starts": [{u"heats": [{u"eventNo": u"1", u"heatNo": u"1", u"sex": u"Girls", u"ageGroup": u"6-U", u"yards": u"100", u"stroke": u"Medley", u"relay": 1, u"estTime": 162.32999999999998}]}]})
#db.collection(u'swim_test').document(u'whitewater').set(myjson)
#!/usr/local/bin/python3


"""