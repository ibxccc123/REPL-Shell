#!/util/bin/python
import sys
import os.path

checker = 0
checker1 = 0

def stackShow(list):
	list.reverse()
	for s in list:
	    print(s)
	list.reverse()

def pushString(word,list,str):
	global checker
	temp = word
	index = str.find(word)
	indextemp = index + len(word)
	if temp.endswith('"'):
	    list.append(temp)
	else:
            for character in str[indextemp:]:
              if character == '"':
                temp += character
                break
              else:
                temp += character 
            list.append(temp)
            checker = temp.count(' ')

def closureString(word,list,stri,closurestack):
	global checker1
	index = stri.find(word)
	index += 2
	x = 1
	contents = ""
	for character in stri[index:]:
	  if character != '}':
            contents += character
            if character == '{':
              x += 1
	  else:
            x -= 1
            if x != 0:
              contents += character
            else:
              break
	closurestack.append(contents)
	checker1 = contents.count(' ') + 1;
	list.append(":closure:")

def closureStringBind(x,closurestack):
	x = x.strip('{} ')            
	closurestack.append(x)
	
def convertlocal(x):
	local = ""
	for character in x[1:]:
          if character != ',':
            local += character		
          else:
            break
	return local	

def convertnotonlylocal(x):
	index = x.find(',')
	index = index + 1
	notonlylocal = ""
	for character in x[index:]:
          if character != '>':
            notonlylocal += character		
          else:
            break
	return notonlylocal

def checkWord(word,list,dict,closuredict,stri,closurestack,parentdict):
	global checker
	global checker1

	if checker != 0:
	    list.pop()
	    checker = checker - 1	

	elif checker1 != 0:
	    list.pop()
	    checker1 = checker1 - 1

	elif word[0] == '"':
	    list.pop()
	    pushString(word,list,stri)

	elif word[0] == '{':
	    list.pop()
	    closureString(word,list,stri,closurestack)	   

	elif word == "apply":
	    list.pop()	
	    if len(list) == 0:
              list.append(":error:")
	    else:
              x = list.pop()
              X = x
              if x[0] == '<' and x[-1] == '>':
                x = convertnotonlylocal(x) 
              if x != ":closure:":
                list.append(X)
                list.append(":error:")
              elif len(closurestack) == 0:
                list.append(X)
                list.append(":error:")
              else:
                name = closurestack.pop()
                tempdict = {}
                for y in name.split():
                  list.append(y)
                  checkWord(y,list,tempdict,closuredict,name,closurestack,parentdict)

	elif word == "quit":
	    sys.exit(0)

	elif word == "bind":
	    list.pop()
	    if len(list) < 2:
              list.append(":error:")
	    else:
              first = list.pop()
              second = list.pop()
              First = first
              Second = second
              first = str(first)
              second = str(second)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first) 
              if second[0] == '<' and second[-1] == '>':
                second = convertlocal(second)
              if second in dict.keys() or second in closuredict.keys():
                list.append(Second)
                list.append(First)
                list.append(":error:")
              elif not second[0].isalpha():
                list.append(Second)
                list.append(First)
                list.append(":error:")
              elif first == ":closure:":
                x = closurestack.pop()
                y = ''.join(('{ ',x,'}'))
                closuredict.update({second:y})	     
                list.append(":closure:")
                closurestack.append(x)
                a = ''.join(('<',second,',',x,'>'))
                parentdict.append(a)
              else:
                dict.update({second:first})
                list.append(first)
                x = ''.join(('<',second,',',first,'>'))
                parentdict.append(x)

	elif word == "load":
	    list.pop()	   
	    if len(list) == 0:
              list.append(":error:")
	    else:
              name = list.pop()
              Name = name 
              name = str(name)
              if name[0] == '<' and name[-1] == '>':
                name = convertnotonlylocal(name) 
              name = name.strip('"')            
              if os.path.exists(name):
                with open(name, "r") as file:
                  stri = file.read()      
                  tempclosurestack = []
                  tempdict = {}
                  tempclosuredict = {}
                  tempparentdict = []
                  for fileword in stri.split():
                    list.append(fileword)
                    checkWord(fileword,list,tempdict,tempclosuredict,stri,tempclosurestack,tempparentdict)
                  list.append(":true:")
              else:
                list.append(":error:")

	elif word == "equal":
	    list.pop()
	    if len(list) < 2:
              list.append(":error:")
	    else:
              first = list.pop()
              second = list.pop()
              First = first
              Second = second
              first = str(first)
              second = str(second)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first)
              if second[0] == '<' and second[-1] == '>':
                second = convertnotonlylocal(second)
              if first == ":closure:" or second == ":closure:":
                list.append(Second)
                list.append(First)
                list.append(":error:")
              else:          
                if first == second:
                  list.append(":true:")
                else:
                  list.append(":false:")  

	elif word == "lessThan":
	    list.pop()
	    if len(list) < 2:
              list.append(":error:")
	    else:
              num1 = list.pop()
              num2 = list.pop()
              Num1 = num1
              Num2 = num2
              num1 = str(num1)
              num2 = str(num2)
              if num1[0] == '<' and num1[-1] == '>':
                num1 = convertnotonlylocal(num1)
              if num2[0] == '<' and num2[-1] == '>':
                num2 = convertnotonlylocal(num2)
              if (not num1.isdigit() and not(num1[0] in "-" and num1[1:].isdigit())) or (not num2.isdigit() and not(num2[0] in "-" and num2[1:].isdigit())):
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              else:          
                if int(num2) < int(num1):
                  list.append(":true:")
                else:
                  list.append(":false:")  

	elif word == "and":
	    list.pop()
	    if len(list) < 2:
              list.append(":error:")
	    else:
              first = list.pop()    
              second = list.pop()
              First = first
              Second = second
              first = str(first)
              second = str(second)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first)
              if second[0] == '<' and second[-1] == '>':
                second = convertnotonlylocal(second)
              if (first != ":true:" and first != ":false:") or (second != ":true:" and second != ":false:"):
                list.append(Second)
                list.append(First)
                list.append(":error:")
              else:
                if first == ":true:" and second == ":true:":
                  list.append(":true:")
                else:
                  list.append(":false:")
                    
	elif word == "if":
	    list.pop()
	    if len(list) < 3:
              list.append(":error:")
	    else:
              first = list.pop()    
              second = list.pop()
              third = list.pop()
              First = first
              Second = second
              Third = third
              first = str(first)
              second = str(second)
              third = str(third)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first)
              if second[0] == '<' and second[-1] == '>':
                second = convertnotonlylocal(second)
              if third[0] == '<' and third[-1] == '>':
                third = convertnotonlylocal(third)
              if first != ":true:" and first != ":false:":
                list.append(Third)
                list.append(Second)
                list.append(First)
                list.append(":error:")
              elif second == ":closure:" and third == ":closure:":
                if first == ":true:":
                  closurestack.pop()
                  list.append(Third)
                else:
                  x = closurestack.pop()
                  closurestack.pop()
                  closurestack.append(x)
                  list.append(Second)
              else:
                if first == ":true:":
                  list.append(Third)
                else:
                  list.append(Second)
                    
	elif word == "or":
	    list.pop()
	    if len(list) < 2:
              list.append(":error:")
	    else:
              first = list.pop()    
              second = list.pop()
              First = first
              Second = second
              first = str(first)
              second = str(second)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first)
              if second[0] == '<' and second[-1] == '>':
                second = convertnotonlylocal(second)
              if (first != ":true:" and first != ":false:") or (second != ":true:" and second != ":false:"):
                list.append(Second)
                list.append(First)
                list.append(":error:")
              else:
                if first == ":false:" and second == ":false:":
                  list.append(":false:")
                else:
                  list.append(":true:")


	elif word == "not":
	    list.pop()
	    if len(list) == 0:
              list.append(":error:")
	    else:
              first = list.pop()
              First = first
              first = str(first)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first)
              if first != ":true:" and first != ":false:":
                list.append(First)
                list.append(":error:")
              else:
                if first == ":true:":
                  list.append(":false:")
                else:
                  list.append(":true:")
                           

	elif word == "-0":
           list.pop()
           list.append("0")
 
	elif word == "pop":
	    list.pop()
	    if len(list) == 0:
              list.append(":error:")
	    else:
              x = list.pop()
              if x == ":closure:":
                closurestack.pop()

	elif word == "exch":
	    list.pop()
	    if len(list) < 2:
              list.append(":error:")
	    else:
              first = list.pop()
              second = list.pop()
              First = first
              Second = second
              first = str(first)
              second = str(second)
              if first[0] == '<' and first[-1] == '>':
                first = convertnotonlylocal(first)
              if second[0] == '<' and second[-1] == '>':
                second = convertnotonlylocal(second)
              if first == ":closure:" and second == ":closure:":
                x = closurestack.pop()  
                y = closurestack.pop()
                closurestack.append(x)
                closurestack.append(y)
                list.append(First)
                list.append(Second)
              else:
                list.append(First)
                list.append(Second)

	elif word == "neg":
            list.pop()
            if len(list) < 1:
              list.append(":error:")
            else:
              num = list.pop()
              num = str(num)
              Num = num
              if num[0] == '<' and num[-1] == '>':
                num = convertnotonlylocal(num)
              if not num.isdigit() and not(num[0] in "-" and num[1:].isdigit()):
                list.append(Num)
                list.append(":error:")
              else:
                num = int(num) * -1 
                list.append(num)

	elif word == "add":
            list.pop()
            if len(list) < 2:
              list.append(":error:")
            else:
              num1 = list.pop()
              num2 = list.pop()
              Num1 = num1
              Num2 = num2
              num1 = str(num1)
              num2 = str(num2)
              if num1[0] == '<' and num1[-1] == '>':
                num1 = convertnotonlylocal(num1)
              if num2[0] == '<' and num2[-1] == '>':
                num2 = convertnotonlylocal(num2)
              if (not num1.isdigit() and not(num1[0] in "-" and num1[1:].isdigit())) or (not num2.isdigit() and not(num2[0] in "-" and num2[1:].isdigit())):
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              else:
                num1 = int(num1)
                num2 = int(num2)
                sum = num1 + num2
                list.append(sum)

	elif word == "sub":
            list.pop()
            if len(list) <2:
              list.append(":error:")
            else:
              num1 = list.pop()
              num2 = list.pop()
              Num1 = num1
              Num2 = num2
              num1 = str(num1)
              num2 = str(num2)
              if num1[0] == '<' and num1[-1] == '>':
                num1 = convertnotonlylocal(num1)
              if num2[0] == '<' and num2[-1] == '>':
                num2 = convertnotonlylocal(num2)
              if (not num1.isdigit() and not(num1[0] in "-" and num1[1:].isdigit())) or (not num2.isdigit() and not(num2[0] in "-" and num2[1:].isdigit())):
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              else:
                num1 = int(num1)
                num2 = int(num2)
                sum = num2 - num1
                list.append(sum)

	elif word == "mul":
            list.pop()
            if len(list) < 2:
              list.append(":error:")
            else:
              num1 = list.pop()
              num2 = list.pop()
              Num1 = num1
              Num2 = num2
              num1 = str(num1)
              num2 = str(num2)
              if num1[0] == '<' and num1[-1] == '>':
                num1 = convertnotonlylocal(num1)
              if num2[0] == '<' and num2[-1] == '>':
                num2 = convertnotonlylocal(num2)
              if (not num1.isdigit() and not(num1[0] in "-" and num1[1:].isdigit())) or (not num2.isdigit() and not(num2[0] in "-" and num2[1:].isdigit())):
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              else:
                num1 = int(num1)
                num2 = int(num2)
                sum = num1 * num2
                list.append(sum)
 
	elif word == "div":
            list.pop()
            if len(list) < 2:
              list.append(":error:")
            else:
              num1 = list.pop()
              num2 = list.pop()
              Num1 = num1
              Num2 = num2
              num1 = str(num1)
              num2 = str(num2)
              if num1[0] == '<' and num1[-1] == '>':
                num1 = convertnotonlylocal(num1)
              if num2[0] == '<' and num2[-1] == '>':
                num2 = convertnotonlylocal(num2)
              if (not num1.isdigit() and not(num1[0] in "-" and num1[1:].isdigit())) or (not num2.isdigit() and not(num2[0] in "-" and num2[1:].isdigit())):
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              elif int(num1) == 0:
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              else:
                num1 = int(num1)
                num2 = int(num2)
                sum = num2 // num1
                if (num2 > 0) and (num1 < 0):
                  check = sum * num1
                  if check > num2:
                    sum = sum + 1
                elif (num2 < 0) and (num1 < 0):
                  check = sum * num1
                  if check > num2:
                    sum = sum + 1     
                list.append(sum)

	elif word == "rem":
            list.pop()
            if len(list) < 2:
              list.append(":error:")
            else:
              num1 = list.pop()
              num2 = list.pop()
              Num1 = num1
              Num2 = num2
              num1 = str(num1)
              num2 = str(num2)
              if num1[0] == '<' and num1[-1] == '>':
                num1 = convertnotonlylocal(num1)
              if num2[0] == '<' and num2[-1] == '>':
                num2 = convertnotonlylocal(num2)
              if (not num1.isdigit() and not(num1[0] in "-" and num1[1:].isdigit())) or (not num2.isdigit() and not(num2[0] in "-" and num2[1:].isdigit())):
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              elif int(num1) == 0:
                list.append(Num2)
                list.append(Num1)
                list.append(":error:")
              else:
                num1 = int(num1)
                num2 = int(num2)
                sum = num2 % num1
                if (num2 > 0) and (num1 < 0):
                  temp = num2 // num1
                  check = temp * num1
                  if check > num2:
                    temp = temp + 1
                    sum = num2 - (num1*temp)
                elif (num2 < 0) and (num1 < 0):
                  sum = num2 // num1
                  check = sum * num1
                  if check > num2:
                    sum = sum + 1     
                    sum = num2 - (num1*sum)
                list.append(sum)

	else:
	    if word in dict.keys():
              list.pop()
              x = ''.join(('<',dict[word],',',dict[word],'>'))
              list.append(x)
	    elif word in closuredict.keys():
              list.pop()
              closureStringBind(closuredict[word],closurestack)
              list.append("<:closure:,:closure:>")           
	    elif word[0].isalpha():
              x = 0
              z = 0
              while x < len(parentdict):
                y = parentdict[x]
                local = ""
                for character in y[1:]:
                  if character != ',':
                    local += character
                  else:
                    break
                if local == word: 
                  list.pop()
                  list.append(y)
                  z = 1
                  break
                else:
                  x += 1
              if z == 0:
                list.pop()
                word = ''.join(('<',word,',',word,'>'))
                list.append(word)
	    elif not word[0].isalpha() and (not word.isdigit() and not(word[0] in "-" and word[1:].isdigit())):
              list.pop()
              list.append(":error:")

def repl():	
	stack = []	
	dict = {}
	closurestack = []
	closuredict = {}
	checker = 0
	parentdict = []
	while True:
	    str = input("repl>")
	    for word in str.split():
                stack.append(word)
                checkWord(word,stack,dict,closuredict,str,closurestack,parentdict)
	    stackShow(stack)

def main():
       repl()
main()

