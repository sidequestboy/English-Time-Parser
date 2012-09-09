from datetime import datetime, timedelta, tzinfo, date, time
import sunrise
import re
import numparser
#include https://en.wikipedia.org/wiki/Number#Word_alternatives

#set timezone...
dateToday = date.today()
#get location for sunset, sunrise, etc.
#http://michelanders.blogspot.ca/2010/12/calulating-sunrise-and-sunset-in-python.html

def getsuntime(keyword):
  s = sunrise.sun(lat=49, long=3)
  if keyword=="sunset":
    time=s.sunset(when=datetime.now())
  elif keyword=="sunrise":
    time=s.sunrise(when=datetime.now())
  elif keyword=="solarnoon":
    time=s.solarnoon(when=datetime.now())
  return time

def tpd(t,delta):
  #method to add timedelta to time
  return (datetime.combine(date.today(), t)-delta).time()
def dpd(d,delta):
  #method to add timedelta to date
  return (datetime.combine(d, time())-delta).date()

worddictionary = {

  "pointers" : {
    "from": ("rel","ref","+-","+"),
    "before": ("rel","ref","-","+"),
    "to": ("rel","ref","-","+"),
    "until": ("rel","ref","-","+"),
    "after": ("rel","ref","+","+"),
    "in": ("ref","rel","+","+")
  }
  ,
  "dateTimes" : {
    "now": (datetime.now(),datetime.now()),
    "tonight": (datetime.combine(date.today(), getsuntime("sunset")), datetime.combine(date.today(), time(23,59,59)))
  }
  ,
  "daytimes" : {
    "afternoon": (getsuntime("solarnoon"),getsuntime("sunset")),
    "noon": (time(12,0,0), time(12,0,0), getsuntime("solarnoon"), getsuntime("solarnoon")),
    "midnight": (time(0,0,0), time(0,0,0)),
    #dawn & dusk vary relative to sunrise/sunset depending on latitude
    "dawn": (tpd(getsuntime("sunrise"), timedelta(seconds=-900)), getsuntime("sunrise")),
    "dusk": (getsuntime("sunset"), tpd(getsuntime("sunset"), timedelta(seconds=900))),
    "twilight": (tpd(getsuntime("sunrise"), timedelta(seconds=-900)), tpd(getsuntime("sunrise"), timedelta(seconds=-900)),
      tpd(getsuntime("sunset"), timedelta(seconds=900)), tpd(getsuntime("sunset"), timedelta(seconds=900))),
    "sunset": (getsuntime("sunset"), getsuntime("sunset")),
    "sundown": (getsuntime("sunset"), getsuntime("sunset")),
    "sunrise": (getsuntime("sunrise"), getsuntime("sunrise"))
  }
  ,
  "dates" : {
    "today": date.today(),
    "tomorrow": dpd(date.today(), timedelta(24*60*60))
  }
}

pluralsuffixes = {
  "s":"",
  "es":"",
  "ies":"y",
  "ves":"f",
  "i":"us"
}

def dictcheck(word,subdict=daytimes):
  """returns definition entry for singular word and plural boolean or None"""
  #try singular:
  for subdict in worddictionary:
    try:
      definition=worddictionary[subdict][word[:len(word)-len(suffix)]+pluralsuffixes[suffix]]
      plural=False
      return (definition, plural)
    except KeyError:
      pass
  for suffix in pluralsuffixes:
    if word[len(word)-len(suffix):]==suffix:
      plural=True
      for subdict in worddictionary:
        try:
          definition=worddictionary[subdict][word[:len(word)-len(suffix)]+pluralsuffixes[suffix]]
          return (definition, plural)
        except KeyError:
          pass
  return (None, None)

def insertchar(original, ch, pos):
  """inserts char at pos in original"""
  return original[:pos] + ch + original[pos:]

def parse(phrase):
  #convert all word numbers to number numbers
  phrase=numparser.text2num(phrase)
  
  #find all number numbers & surround with spaces
  regexp=re.compile("\d+")
  fi=regexp.finditer(phrase)
  i=0
  for f in fi:
    if f.start()!=0:
      phrase=insertchar(phrase," ",f.start()+i)
      i+=1
    if f.end()!=len(phrase):
      phrase=insertchar(phrase," ",f.end()+i)
      i+=1
  wlist = phrase.split()
  #convert to ints
  
  print wlist
  """for index in range(len(wlist)):
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

def timeFind(index, words):
  pass

if __name__ == "__main__":
  parse("in five sunsets")
