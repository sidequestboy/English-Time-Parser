from datetime import datetime, timedelta, tzinfo, date, time
import sunrise
import re

#set timezone...
dateToday = date.today()
#get location for sunset, sunrise, etc.
#http://michelanders.blogspot.ca/2010/12/calulating-sunrise-and-sunset-in-python.html
s = sun(lat=49, long=3)
sunriseTime=s.sunrise
sunsetTime=s.sunset
solarNoon=s.solarnoon

pointers = {
  "from": ("rel","ref","plusminus","plus"),
  "before": ("rel","ref","minus","plus"),
  "to": ("rel","ref","minus","plus"),
  "until": ("rel","ref","minus","plus"),
  "after": ("rel","ref","plus","plus"),
  "in": ("ref","rel","plus","plus")
}


dateTimes = {
  "now": (datetime.now(),datetime.now())
  "tonight": (datetime.combine(date.today(), sunsetTime), datetime.combine(date.today(), time(23,59,59)))

}
times = {
  "afternoon": (solarNoon,sunsetTime)
  "noon": (time(12,0,0), time(12,0,0), solarNoon, solarNoon)
  "midnight": (time(0,0,0), time(0,0,0))
  #dawn & dusk vary relative to sunrise/sunset depending on latitude
  "dawn": (sunriseTime-timedelta(seconds=900), sunriseTime)
  "dusk": (sunsetTime, sunsetTime+timedelta(seconds=900))
  "twilight": (sunriseTime-timedelta(seconds=900), sunriseTime-timedelta(seconds=900),
    sunsetTime+timedelta(seconds=900), sunsetTime+timedelta(seconds=900))
  "sunset": (sunsetTime, sunsetTime)
  "sundown": (sunsetTime, sunsetTime)
  "sunrise": (sunriseTime, sunriseTime)
}
dates = {
  "today": datetime.now(),
  "tomorrow": datetime.now()+timedelta(1),
  "yesterday": datetime.
}

def parse(phrase):
  wordsWithInts=[]
  words = phrase.split()
  #find all numbers
  wordsWithInts=text2int(phrase)
  for index in range(len(words)):
    #find all times
    wordsWithInts+=text2int(word)
  for index in range(len(wordsWithInts)):
    if type(wordsWithInts[i]) is int:
      #look to the right and left for pointers/units
      wordsWithInts[i-1]

  #assume implicit pointer (from now)

#stolen from http://stackoverflow.com/a/493788/1402511
def text2time(wlist):
  #find times of format 13:45, 1:45 pm, 2h30
  #patterns:
  divider=[":","h"]
  regexp1 = re.compile("\d{1,2}:\d{1,2}")
  regexp2 = re.compile("\d{1,2}h\d{1,2}")

  for i in range(len(wlist)):
    match[0]=regexp1.search(wlist[i])
    match[1]=regexp2.search(wlist[i])
    for j in range(len(match)):
      if type(match[j]) not None:
        oldWord=wlist[i]
        wlist[i]=oldWord[:match[j].start()]
        sepIndex=re.compile(divider[j]+"+").search(wlist[i]).start()
        wlist[i+1]=oldWord[match[j].end():]
        wlist[i+1:i+1]=
          time([wlist[i][0:sepIndex],wlist[i][sepIndex+1:]])


def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          return [result+current,word]
          #raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return [result + current]

def timeFind(index, words):
  pass

def stringToTimeDelta(time):
