from datetime import datetime, timedelta, tzinfo, date, time
import sunrise
import re
#include https://en.wikipedia.org/wiki/Number#Word_alternatives

#set timezone...
dateToday = date.today()
#get location for sunset, sunrise, etc.
#http://michelanders.blogspot.ca/2010/12/calulating-sunrise-and-sunset-in-python.html
s = sunrise.sun(lat=49, long=3)
sunriseTime=s.sunrise(when=datetime.now())
sunsetTime=s.sunset(when=datetime.now())
solarNoon=s.solarnoon(when=datetime.now())

def timeplusdelta(t,delta):
  #method to add timedelta to time
  return (datetime.combine(date.today(), t)-delta).time()

pointers = {
  "from": ("rel","ref","plusminus","plus"),
  "before": ("rel","ref","minus","plus"),
  "to": ("rel","ref","minus","plus"),
  "until": ("rel","ref","minus","plus"),
  "after": ("rel","ref","plus","plus"),
  "in": ("ref","rel","plus","plus")
}


dateTimes = {
  "now": (datetime.now(),datetime.now()),
  "tonight": (datetime.combine(date.today(), sunsetTime), datetime.combine(date.today(), time(23,59,59)))
}
times = {
  "afternoon": (solarNoon,sunsetTime),
  "noon": (time(12,0,0), time(12,0,0), solarNoon, solarNoon),
  "midnight": (time(0,0,0), time(0,0,0)),
  #dawn & dusk vary relative to sunrise/sunset depending on latitude
  "dawn": (timeplusdelta(sunriseTime, timedelta(seconds=-900)), sunriseTime),
  "dusk": (sunsetTime, timeplusdelta(sunsetTime, timedelta(seconds=900))),
  "twilight": (timeplusdelta(sunriseTime, timedelta(seconds=-900)), timeplusdelta(sunriseTime, timedelta(seconds=-900)),
    timeplusdelta(sunsetTime, timedelta(seconds=900)), timeplusdelta(sunsetTime, timedelta(seconds=900))),
  "sunset": (sunsetTime, sunsetTime),
  "sundown": (sunsetTime, sunsetTime),
  "sunrise": (sunriseTime, sunriseTime)
}
dates = {
  "today": datetime.now(),
  "tomorrow": datetime.now()+timedelta(1)
}



def parse(phrase):
  wlist=[]
  words = phrase.split()
  #find all numbers
  wlist=text2num(phrase)
  print wlist
  """for index in range(len(words)):
    #find all times
    wlist+=text2num(word)
  for index in range(len(wlist)):
    if type(wlist[i]) is int:
      #look to the right and left for pointers/units
      wlist[i-1]
  """
  #assume implicit pointer (from now)

#stolen from http://stackoverflow.com/a/493788/1402511
"""
def text2time(wlist):
  #find times of format 13:45, 1:45 pm, 2h30
  #patterns:
  divider=[":","h"]
  regexp1 = re.compile("\d{1,2}:\d{2}")
  regexp2 = re.compile("\d{1,2}h\d{2}")
  regexp3 = re.compile("o'?clock")

  for i in range(len(wlist)):
    match[0]=regexp1.search(wlist[i])
    match[1]=regexp2.search(wlist[i])
    for j in range(len(match)):
      if type(match[j]) not None:
        oldWord=wlist[i]
        wlist[i]=oldWord[:match[j].start()]
        sepIndex=re.compile(divider[j]+"+").search(wlist[i]).start()
        wlist[i+1]=oldWord[match[j].end():]
        minutes=int(wlist[i][sepIndex+1:])
        extraHours=minutes/60
        hours=int(wlist[i][0:sepIndex])+extraHours #rollover hours
        extraDays=hours/24 #rollover days
        wlist[i+1:i+1]=
          time(int(wlist[i][0:sepIndex])%24,int(wlist[i][sepIndex+1:])%60) #convert to int to time
    oclkMatch=regexp3.search(wlist[i])
    if type(oclkMatch) not None:
      #look at number before and "and" after
      try:
        if type(wlist[i-1]) is int:
          if wlist[i-1]>23 or <0:
            extraDays=wlist[i-1]/24
            wlist[i-1]=wlist[i-1]%24
          else:
            extraDays=0
          if wlist[i+1]
        else:
          try:
            raise Exception("input error what o'clock?")
          except Exception as inst:
            print type(inst)
            print inst.args

      except IndexError:
        try:
          raise Exception("input error what o'clock?")
        except Exception as inst:
          print type(inst)
          print inst.args
      

  return (wlist,extraDays)
"""
def strnum2int(textnum):
  #converts all lone numbers to ints
  for i in range(len(textnum)):
    try:
      textnum[i]=int(textnum[i])
    except ValueError:
      pass
  return textnum

#stolen from http://stackoverflow.com/a/493788/1402511
def text2num(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = [
        "hundred", "thousand", "million", "billion", "trillion", "quadrillion", 
        "quintillion", "sexillion", "septillion", "octillion", "nonillion", "decillion",
        "undecillion", "duodecillion", "tredecillion", "quattuordecillion", "quindecillion", 
        "sexdecillion", "septdecillion", "octodecillion", "novemdecillion", "vigintillion", 
        "unvigintillion", "duovigintillion", "trevigintillion"]

      numwords["and"] = (-1, -1)
      numwords["o"] = (0, 0) #same as "zero"
      numwords["o'"] = (0, 0)
      numwords["a"] = (0, 1) #same as "one"
      for idx, word in enumerate(units):    numwords[word] = (0 if (idx<10) else 1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (idx * 3 or 2, 10 ** (idx * 3 or 2))

    prevscale = 0
    result = 0
    climb=1
    sclimb=""
    textnum=textnum.replace("-"," ") #treat "-" as " "
    for word in textnum.split():
        if word not in numwords:
          return result + climb
        scale, num = numwords[word]
        if scale<0: #filter "and"
          scale=prevscale
        elif (prevscale == 0 or 1) and (scale == 0 or 1): #one ten = 110
          climb = int(str(sclimb) + str(num))
          sclimb=str(climb)
        elif prevscale > scale:
          result += climb
          climb = num

        elif prevscale <= scale:
          climb = climb * num
        prevscale=scale
    return result + climb

def timeFind(index, words):
  pass

if __name__ == "__main__":
  parse("one-twenty")
