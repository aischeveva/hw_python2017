import urllib.request
import re
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import html
from pymystem3 import Mystem


app = Flask(__name__)


@app.route('/newsletters')
def news():
    req = urllib.request.Request('https://hron.ru')
    with urllib.request.urlopen(req) as f:
        text = f.read().decode('utf-8')
    text = html.unescape(text)
    text = re.sub('<script type="text/javascript" >.+?</noscript>', '', text, flags=re.DOTALL)
    text = re.sub('<script type="text/javascript">.+?</script>', '', text, flags=re.DOTALL)
    text = re.sub('<.*?>', '', text, flags=re.DOTALL)
    text = text.split()
    dorev = parse_dict()
    for i, word in enumerate(text):
        text[i] = word.strip('!?,;...').lower()
    text = ' '.join(text)
    m = Mystem()
    arr_stem = m.analyze(text)
    for i, word in enumerate(arr_stem):
        if 'analysis' in word:
            if len(word['analysis']) > 0:
                if 'lex' in word['analysis'][0]:
                    if word['analysis'][0]['lex'] in dorev and ('е' in word['analysis'][0]['lex'] or 'и' in word['analysis'][0]['lex'] or 'ф' in word['analysis'][0]['lex']):
                        for j, l in enumerate(dorev[word['analysis'][0]['lex']]):
                            if l == 'ѣ' or l == 'Ѳ' or l == 'ѳ' or l == 'ѵ':
                                arr_stem[i]['text'] = arr_stem[i]['text'][:j] + l + arr_stem[i]['text'][j+1:]
                if 'gr' in word['analysis'][0]:
                    if 'дат' in word['analysis'][0]['gr'] and word['text'].endswith('е'):
                        arr_stem[i]['text'] = arr_stem[i]['text'][:-1] + 'ѣ'
                    if i + 2 < len(arr_stem):
                        if 'A' in word['analysis'][0]['gr'] and (word['text'].endswith('ие') or word['text'].endswith('ые')) and ('жен' in arr_stem[i+2]['analysis'][0]['gr'] or 'сред' in arr_stem[i+2]['analysis'][0]['gr']):
                            arr_stem[i]['text'] = arr_stem[i]['text'][:-1] + 'я'
        arr_stem[i]['text'] = change_word(arr_stem[i]['text'], dorev)
    text_fout = ''
    freq = {}
    for word in arr_stem:
        if word['text'] != ' ':
            if word['text'] in freq:
                freq[word['text']] += 1
            else:
                freq[word['text']] = 1
        text_fout += word['text'] + ' '
    rez = []
    i = 0
    for word in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        if i == 10:
            break
        print(word)
        s = word[0] + ', ' + str(word[1])
        rez.append(s)
        i += 1
    return render_template('newsletters.html', text=text_fout, rez=rez)


@app.route('/test')
def test():
    check = ['1', '2', '2', '2', '2', '1', '1', '1', '1', '2']
    if request.args:
        temp_arr = []
        for i in range(1, 11):
            if request.args[str(i)] == check[i - 1]:
                temp_arr.append(1)
            else:
                temp_arr.append(0)
        '''
        temp = temp_arr[1]
        for t in range(8, 0, -1):
            temp_arr[t] = temp_arr[t + 1]
        temp_arr[9] = temp'''
        return render_template('test.html', rez=temp_arr)
    return render_template('test.html', rez=[])


@app.route('/', methods=['GET', 'POST'])
def main_page():
    weather = get_weather()
    if request.args:
        if 'word' in request.args:
            return render_template('main_page.html', print_word=change_word(request.args['word']), fact_temp=weather[0], fact_cond=weather[1], feel_like=weather[2])
        if 'news' in request.args:
            return redirect(url_for('news'))
        if 'test' in request.args:
            return redirect(url_for('test'))
    return render_template('main_page.html', print_word='', fact_temp=weather[0], fact_cond=weather[1], feel_like=weather[2])


def parse_dict():
    with open('dict.txt', 'r', encoding='utf-8') as fin:
        text = fin.read().split('\n')
    for i, line in enumerate(text):
        text[i] = line.split('\t')
        for j in text[i]:
            if j == '' or j == ' ':
                text[i].remove(j)
    d = {}
    for line in text:
        d[line[0]] = line[1].split(' ')[0].strip(',;')
    return d


def change_word(word, dorev_dict):
    if 'е' in word or 'и' in word or 'ф' in word or 'Ф' in word or 'И' in word or 'Е' in word:
        if word in dorev_dict:
            word = dorev_dict[word]
    word = re.sub('и(а|о|у|и|ы|е|ё|ю|я)', 'i\\1', word)
    word = re.sub('(бе|чере|чре)с', '\\1з', word)
    s = 'бвгджзклмнпрстфхцчшщ'
    if word != '':
        if word[-1] in s:
            word += 'ъ'
    return word


def get_weather():
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0; rv:11.0) like Gecko'
    req = urllib.request.Request('https://yandex.ru/pogoda/10463', headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    reg_temp = re.compile('<span class="fact__temp-val">.+?</span>', flags=re.DOTALL)
    reg_cond = re.compile('<span class="fact__condition">.+?</span>', flags=re.DOTALL)
    reg_feel = re.compile('<div class="fact__feels">.+?°</div>', flags=re.DOTALL)
    temp = reg_temp.findall(html)
    cond = reg_cond.findall(html)
    feel = reg_feel.findall(html)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    temp_fact = regTag.sub('', temp[0])
    temp_fact = regSpace.sub('', temp_fact)
    cond = regTag.sub('', cond[0])
    cond = regSpace.sub('', cond)
    feel = regTag.sub('', feel[0])
    feel = regSpace.sub('', feel)
    return temp_fact, cond, feel

if __name__ == '__main__':
    #parse_dict()
    app.run()