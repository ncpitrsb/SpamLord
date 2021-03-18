import sys
import os
import re
import pprint


def process_file(name, f):
    res = []
    for line in f:
        #find phone number
        text1 = re.sub("[<].*?[>]", '', line)
        text1 = re.sub("[{].*", '', text1)
        text1 = re.sub(".*[}]", '', text1)
        text1 = re.sub("[(][0-9]{4}[)]", '', text1)
        text1 = re.sub("[(]","",text1)
        text1 = re.sub("[)][ ]?"," ",text1)
        text1 = re.sub("[ ]","-",text1)

        pattern_toFind_phone = '[(]?[0-9]{3}[)]?'+'[ ]?'+'[-]?[0-9]{3}'+'[-][0-9]{4}'
        list_phone_num = re.findall(pattern_toFind_phone, text1)

        # print(list_phone_num)
        if(len(list_phone_num)!=0):
            for phonenumber in list_phone_num:
                res.append((name, 'p', phonenumber))
        
        # find email 
        text2=line
        find_tuple = '''[(]['].*['][,]['].*['][)]'''
        x=re.findall(find_tuple,text2.lower())
        finished = []
        if len(x)==1:
            print(x)
            test = x[0].split(',')
            for i in test:
                i = re.sub("[(][']","",i)
                i = re.sub("[']","",i)
                i = re.sub("[)]","",i)
                finished.append(i)
        if len(finished)==2:
            text2 = finished[1]+"@"+finished[0]
        
        text2 = re.sub('[\<].*?[\>]',"",text2.lower())
        text2 = re.sub('.*[m][a][i][l][:][ ]?[t]?[o]?',"",text2) #*****mail delete text before "mail"
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
        #specific word (skip or replace)
        text2 = re.sub('[c][s][ ]\D+[ ]\D+',"cs.stanford.edu",text2) #replace
        text2 = re.sub("[s][e][r][v][e][r]","",text2) #skip (delete)

        pattern_toFind_email = '[a-z]*[.]?[a-z]+'+'[ ]?[@][ ]?'+'[a-z]*[ ]?[.]*[a-z]*[ ]?[.][a-z]{3}'
        list_email = re.findall(pattern_toFind_email, text2)

        if(len(list_email)!=0):
            for email in list_email:
                email = re.sub('[ ]',"",email)
                res.append((name, 'e', email))
    
    return res


def process_dir(data_path):
    """
    You should not need to edit this function, nor should you alter
    its interface as it will be called directly by the submit script
    """
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path, fname)
        f = open(path, 'r', encoding='latin-1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list


def get_gold(gold_path):
    """
    You should not need to edit this function.
    Given a path to a tsv file of gold e-mails and phone numbers
    this function returns a list of tuples of the canonical form:
    (filename, type, value)
    """
    # get gold answers
    gold_list = []
    f_gold = open(gold_path, 'r', encoding='utf8')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list


def score(guess_list, gold_list):
    """
    You should not need to edit this function.
    Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives.  Importantly, it
    converts all of the values to lower case before comparing
    """
    guess_list = [
        (fname, _type, value.lower())
        for (fname, _type, value)
        in guess_list
    ]
    gold_list = [
        (fname, _type, value.lower())
        for (fname, _type, value)
        in gold_list
    ]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    # print 'Guesses (%d): ' % len(guess_set)
    # pp.pprint(guess_set)
    # print 'Gold (%d): ' % len(gold_set)
    # pp.pprint(gold_set)
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('Summary: tp=%d, fp=%d, fn=%d' % (len(tp), len(fp), len(fn)))


def main(data_path, gold_path):
    """
    You should not need to edit this function.
    It takes in the string path to the data directory and the
    gold file
    """
    guess_list = process_dir(data_path)
    gold_list = get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])
