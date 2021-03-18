import re

text2 = '''<a href="mailto:manning@cs.stanford.edu">&lt;manning@cs.stanford.edu&gt;</A> '''
find_tuple = '''[(]['].*['][,]['].*['][)]'''
x=re.findall(find_tuple,text2)
finished = []
if len(x)!=0:
    test = x[0].split(',')
    for i in test:
        i = re.sub("[(][']","",i)
        i = re.sub("[']","",i)
        i = re.sub("[)]","",i)
        finished.append(i)
if len(finished)!=0:
    text2 = finished[1]+"@"+finished[0]


text2 = re.sub('[\<].*?[\>]',"",text2.lower())
text2 = re.sub('.*[m][a][i][l][:][t]?[o]?',"",text2) #*****mail delete text before "mail"
text2 = re.sub('[(].*?["]',"",text2)
text2 = re.sub('[(].*?[;]',"",text2)
text2 = re.sub('.*?[(]',"",text2)
text2 = re.sub('[ ][w][h][e][r][e][ ]',"@",text2)
text2 = re.sub('[ ][d][o][m][ ]',".",text2)
text2 = re.sub('[%][0-9]*'," ",text2)
text2 = re.sub('[ ][a][t][ ]',"@",text2)
text2 = re.sub('[ ][d][o]?[t][ ]',".",text2)
text2 = re.sub('[;]',".",text2)
text2 = re.sub('[-]',"",text2) #d-l-w-h-@-s-t-a-n-f-o-r-d-.-e-d-u
text2 = re.sub('[&].*[0-9][.]',"@",text2)
text2 = re.sub('[&].*[.]',"",text2)
text2 = re.sub('[c][s][ ]\D+[ ]\D+',"cs.stanford.edu",text2)
text2 = re.sub("[s][e][r][v][e][r]","",text2)

print(text2)







pattern_toFind_email = '[a-z]*[.]?[a-z]+[ ]?[@][ ]?[a-z]*[ ]?[.]*[;]?[a-z]*[ ]?[;]?[.]?[a-z]{3}'

p=[]
earth = re.findall(pattern_toFind_email,text2)
print(earth)
for email in earth:
    email = re.sub('[ ]',"",email)
    p.append(email)
print(p)
# for i in earth:
#     text1 = re.sub(r"[ ]","",i)
#     print(text1)