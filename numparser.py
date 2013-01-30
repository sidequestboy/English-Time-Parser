##editing units, tens, scales will affect text2num
specialfractions = [
  "half", "third", "quarter", "fifth", "", "", "", "ninth"
]

units = [
  "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
  "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
  "sixteen", "seventeen", "eighteen", "nineteen"
  ]

tens = [
  "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", 
  "ninety", "", "eleventy"
  ]

scales = [
  "hundred", "thousand", "million", "billion", "trillion", "quadrillion", 
  "quintillion", "sexillion", "septillion", "octillion", "nonillion", 
  "decillion", "undecillion", "duodecillion", "tredecillion", 
  "quattuordecillion", "quindecillion", "sexdecillion", "septdecillion", 
  "octodecillion", "novemdecillion", "vigintillion", "unvigintillion", 
  "duovigintillion", "trevigintillion"]

unitfractions = [unit+"th" for unit in units if unit!="zero"]

tenfractions = [
  "" if tens[i]=="" else tens[i][:-1]+"ieth" for i in range(1,len(tens))
  ]

scalefractions = [scale+"th" for scale in scales]
unitplurals = [unit+"s" for unit in units]
tenplurals = [ten[:-1]+"ies" for ten in tens]
scaleplurals = [scale+"s" for scale in scales]
specialfractionplurals = ["halves"]+[specialfractions[i]+"s" for i in range(1,len(specialfractions))]


#structure stolen from http://stackoverflow.com/a/493788/1402511
def text2num(textnum, numwords={}, fractions={}):
    if not numwords:
      numwords["and"] = (None, None)
      numwords["of"] = (None, None)
      numwords["o"] = (0, 0) #same as "zero"
      numwords["o'"] = (0, 0)
      numwords["a"] = (0, 1) #same as "one"
      numwords["an"] = (0, 1) #same as "one"
      for idx, word in enumerate(units): numwords[word] = (0 if (idx<10) else 1, idx)
      for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales): numwords[word] = (idx * 3 or 2, 10 ** (idx * 3 or 2))
      for idx, word in enumerate(specialfractions): fractions[word] = (-1,float(1)/(idx+1))
      for idx, word in enumerate(unitfractions): fractions[word] = (-1,float(1)/(idx+1))
      for idx, word in enumerate(tenfractions): fractions[word] = (-1,float(1)/((idx+1)*10))
      for idx, word in enumerate(scalefractions): fractions[word] = (-1,float(1)/10**(idx * 3 or 2))


    phrase=""#starting empty
    prevscale = 0#climb starts immediately
    result = 0#result for number parsing
    climbed=[]
    climb=1#climb starts as unity
    sclimb=str(climb)#mirrors climb
    newclimb=True
    f=True #flag is True when previous entry was non-numword
    textnum=textnum.replace("-"," ") #treat "-" as " "

    for word in textnum.split():
      if word not in numwords and word not in fractions:
        print "NOT NUMWORD"
        if not f:#previous entry was numword - finish number parse, reset
          climbed.append(climb)
          result=sum(climbed)
          if phrase=="":
            phrase=(str(result))#add number
          else:
            phrase=phrase+" "+(str(result))
          prevscale = 0#initial settings
          climbed=[]
          climb=1
          newclimb=True
          sclimb=str(climb)
          f=True
        if phrase=="":
          phrase=(word)
        else:
          phrase=phrase+" "+word
      else:#numword or fraction
        if word in numwords:
          scale, num = numwords[word]
        elif f==True:
          scale, num = fractions[word]
        else:#fraction word not actually fraction then skip
          phrase=phrase+" "+(str(result))
          prevscale = 0#initial settings
          climbed=[]
          climb=1
          newclimb=True
          sclimb=str(climb)
          f=True
        print "num="+str(num)+" scale="+str(scale)

        f=False#signal for numword
        if scale == None: #catch "and", "of" - terminates climb and starts new climb
          if word=="and":#start new climb
            climbed.append(climb)
            prevscale = 0#initial settings for new climb
            climb=1
            newclimb=True
            sclimb=str(climb)
          elif word=="of":#continue current climb...
            prevscale = 0
            newclimb = False
          
        elif (prevscale == 0 or prevscale == 1) and (scale == prevscale or scale == 1): #one ten = 110
          if newclimb==True:
            print "newclimb"
            climb=num
            newclimb=False
          else:
            climb=int(sclimb+str(num)) 
          sclimb=str(climb)
          print "classifiers: climb="+sclimb+" climbed="+str(climbed)
        elif prevscale == 1 and scale == 0:#add to current climb
          newclimb = False
          climb += num
          sclimb = str(climb)
          print "add to classifier - climb="+sclimb+" climbed="+str(climbed)
        elif prevscale > scale:#fall
          climbed.append(climb)#add climb to climbed
          newclimb=True
          climb = num#start new climb with num
          sclimb = str(climb)
          print "fell - new climb="+sclimb+" climbed="+str(climbed)
          
        elif prevscale <= scale:#climbing
          print "climbing current num="+str(num)+" climb="+sclimb
          newclimb=False
          climb = climb * num#increase climb
          sclimb= str(climb)
          print "climbed climb="+sclimb+" climbed="+str(climbed)
        print "phrase="+phrase
        prevscale=scale
    if not f:#last word in whole phrase was numword
      print "finishing up... result="+str(result)+" climb="+str(climb)+" phrase="+phrase
      climbed.append(climb)
      result=sum(climbed)
      if phrase=="": phrase=str(result)
      else: phrase=phrase+" "+str(result)
    print phrase
    return phrase
"""
if __name__=="__main__":
  text2num("i will be ten in twenty minutes four hundred")
 """
 