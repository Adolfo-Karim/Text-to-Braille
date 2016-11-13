import string
def print2dList(l):
  for lo in l:
    print (lo,"\n")

alphabets_braille1={  "":"",
                      " ": "000000",
                      'a': "100000",
                      'b': "110000",
                      'c': "100100",
                      'd': "100110",
                      'e': "100010",
                      'f': "110100",
                      'g': "110110",
                      'h': "110010" ,
                      'i': "010100",
                      'j': "010110",
                      'k': "10100",
                      'l': "111000",
                      'm': "101100",
                      'n': "101110",
                      'o': "101010",
                      'p': "111100",
                      'q': "111110",
                      'r': "111010",
                      's': "011100",
                      't':  "011110",
                      'u': "101001",
                      'v': "111001",
                     'w': "010111",
                      'x': "101101",
                      'y': "101111",
                      'z': "101011"}

numbers_braille1= {   "0": "010110",
                      "1": "100000",
                      "2": "110000",
                      "3": "100100",
                      "4": "100110",
                      "5": "100010",
                      "6": "110100",
                      "7": "110110",
                      "8": "110010" ,
                      "9": "010100",
                      "0": "010110",}



num_initializer= "001111"

def convert_text_to_string(symbol):
    result=""
    if(symbol.isdigit()):
        result+=num_initializer+numbers_braille1[symbol]
    elif(symbol.isupper()):
      result="000001"+alphabets_braille1[symbol.lower()]
    elif(symbol=="."): 
      result="010011"
    elif(symbol==","): 
      result="010000"    
    elif(symbol=="?"): 
      result="jjjjjj"
    else:
      result=alphabets_braille1[symbol] 
    return result

def main(string):
  resultStr=""
  for c in string:
    resultStr+=convert_text_to_string(c)
  return resultStr

def filterText(text):
  text.replace("\n"," ")
  result=""
  for c in text:
    if c in (string.ascii_letters +string.digits+".,?"+" "):
      result+=c
  return result

#makes it into strings of 48
def convert_to_readable_form(primary_string):
    mainarray=[]
    for j in range(0,len(primary_string),48):
        arr=""
        for i in range (j,j+48):
            try:
             arr+=str(primary_string[i])
            except:
                break
        mainarray.append(arr)
    return mainarray

line="popo"
primary_string= main(   filterText(line)   )
main_string= convert_to_readable_form(primary_string)
#########################################################
def converter(main_string):
  mainArray=[]
  for string in main_string:
    result=[]    
    for i in range(0,len(string),3):
      res=string[i:i+3]
      result.append(res)
    for i in range(len(result),16):
      result.append("000")

    mainArray.append(result)
  for i in range(len(mainArray),4):
    mainArray.append(["000","000","000","000","000","000","000","000","000",\
                          "000","000","000","000","000","000","000"])
  return mainArray

final_string=converter(main_string)
