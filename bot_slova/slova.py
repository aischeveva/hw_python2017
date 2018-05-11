from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem
import random

morph = MorphAnalyzer()
m_stem = Mystem()

def split_sent(sentence):
    sent = sentence.split()
    ana = []
    for i, word in enumerate(sent):
        sent[i] = word.strip(',!.?:;')
        ana.append(morph.parse(sent[i])[0].tag)
    print(ana)
    return ana


def create_sent(sent):
    new_s = ''
    for word in sent:
        if 'NOUN' in word:
            if 'femn' in word:
                if 'anim' in word:
                    with open('fem_anim.txt', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
                else:
                    with open('fem_inan.txt', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
            else:
                if 'anim' in word:
                    with open('masc_anim.txt', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
                else:
                    with open('masc_inan.txt', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
        elif 'VERB' in word or 'INFN' in word:
            if 'tran' in word:
                if 'perf' in word:
                    with open('tran_perf', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
                else:
                    with open('tran_imp', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
            else:
                if 'perf' in word:
                    with open('intr_perf', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
                else:
                    with open('intr_imp', 'r', encoding='utf-8') as f:
                        new_w = f.read().split()
        else:
            if word.POS != None:
                with open(word.POS.lower() + '.txt', 'a', encoding='utf-8') as f:
                    new_w = f.read().split()
        new_word = random.choice(new_w)
        infl = set()
        print(word)
        if 'VERB' in word:
            if word.tense != None:
                infl.add(word.tense)
            if word.voice != None:
                infl.add(word.voice)
            if word.number != None:
                infl.add(word.number)
            if word.gender != None:
                infl.add(word.gender)
            if word.person != None:
                infl.add(word.person)
            if word.mood != None:
                infl.add(word.mood)
        print(infl)
        new_word = morph.parse(new_word)[0].inflect(infl)
        print(new_word)
        new_s += str(new_word.word) + ' '
    print(new_s)


def get_ready():
    with open('sour.txt', 'r', encoding='utf-8') as f:
        temp = f.read().split('\n')
    words = []
    for line in temp:
        word  = line.split('\t')[1]
        w = morph.parse(word)[0]
        #print(w.word, w.tag.POS)
        if 'NOUN' in w.tag:
            if 'femn' in w.tag:
                if 'anim' in w.tag:
                    with open('fem_anim.txt', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
                else:
                    with open('fem_inan.txt', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
            else:
                if 'anim' in w.tag:
                    with open('masc_anim.txt', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
                    print()
                else:
                    with open('masc_inan.txt', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
        elif 'VERB' in w.tag or 'INFN' in w.tag:
            if 'tran' in w.tag:
                if 'perf' in w.tag:
                    with open('tran_perf', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
                else:
                    with open('tran_imp', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
            else:
                if 'perf' in w.tag:
                    with open('intr_perf', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
                else:
                    with open('intr_imp', 'a', encoding='utf-8') as f:
                        f.write(w.normal_form + '\n')
        else:
            if w.tag.POS == None:
                with open('num.txt', 'a', encoding='utf-8') as f:
                    f.write(w.normal_form + '\n')
            else:
                with open(w.tag.POS.lower() + '.txt', 'a', encoding='utf-8') as f:
                    f.write(w.normal_form + '\n')


a = split_sent('купи пирог')
create_sent(a)
#get_ready()
#print(morph.parse('мыла'))
#print(m_stem.analyze('мама мыла раму'))