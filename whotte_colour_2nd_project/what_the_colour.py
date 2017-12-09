from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json
from collections import OrderedDict
import os

app = Flask(__name__)
j_dict = {}


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.args:
        get_values(request.args)
        return redirect(url_for('thanks'))
    return render_template('start_page.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route('/json')
def push_json():
    return json.dumps(j_dict, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

@app.route('/stats')
def draw_stat():
    temp = count_stat()
    with open('statist.json', 'w', encoding='utf-8') as fout:
        json.dump(temp, fout, ensure_ascii=False, indent=4, sort_keys=True)
    return render_template('stats1.html', k=json.dumps(OrderedDict(sorted(temp.items())), ensure_ascii=False, indent=4, sort_keys=True))


@app.route('/search')
def search_smth():
    if request.args:
        global search_res
        search_res = search_this(request.args)
        return redirect(url_for('search_results'))
    return render_template('search_p.html')


@app.route('/results')
def search_results():
    return render_template('results.html', res=OrderedDict(sorted(search_res.items())))


def get_values(request):
    u_name = "user" + str(len(j_dict))
    temp_arr = []
    for i in range(1, 16):
        nm = "colour" + str(i)
        if nm in request:
            temp_arr.append(request[nm])
    if 'sex' in request and 'language' in request and 'age' in request and len(temp_arr) == 11:
        j_dict[u_name] = [request['sex'], request['language'], request['age'], temp_arr]
        with open('results.json', 'w', encoding='utf-8') as fout:
            json.dump(j_dict, fout, ensure_ascii=False, indent=4, sort_keys=True)

def search_this(request):
    temp_dic = {}
    if 'sex' in request and request['lang'] != ('Введите язык' or '') and 'age' in request:
        for k in j_dict:
            if j_dict[k][0] == request['sex'] and j_dict[k][1] == request['lang'] and j_dict[k][2] == request['age']:
                temp_dic[k] = j_dict[k]
    elif 'sex' in request and 'age' in request:
        for k in j_dict:
            if j_dict[k][0] == request['sex'] and j_dict[k][2] == request['age']:
                temp_dic[k] = j_dict[k]
    elif 'sex' in request and request['lang'] != ('Введите язык' or ''):
        for k in j_dict:
            if j_dict[k][0] == request['sex'] and j_dict[k][1] == request['lang']:
                temp_dic[k] = j_dict[k]
    elif 'age' in request and request['lang'] != ('Введите язык' or ''):
        for k in j_dict:
            if j_dict[k][1] == request['lang'] and j_dict[k][2] == request['age']:
                temp_dic[k] = j_dict[k]
    elif 'sex' in request:
        for k in j_dict:
            if j_dict[k][0] == request['sex']:
                temp_dic[k] = j_dict[k]
    elif 'age' in request:
        for k in j_dict:
            if j_dict[k][2] == request['age']:
                temp_dic[k] = j_dict[k]
    elif request['lang'] != ('Введите язык' or ''):
        for k in j_dict:
            if j_dict[k][1] == request['lang']:
                temp_dic[k] == j_dict[k]
    else:
        temp_dic['null'] = 'Вы не ввели параметров поиска!'
    return temp_dic


def count_stat():
    temp = {}
    for i in range(1, 6):
        temp[str(i)] = [0, 0, 0]
    for k in j_dict:
        for t in j_dict[k][3]:
            if t == 'синий':
                temp[j_dict[k][2]][0] += 1
            elif t == 'голубой':
                temp[j_dict[k][2]][1] += 1
            else:
                temp[j_dict[k][2]][2] += 1
    return temp

if __name__ == "__main__":
    try:
        with open('results.json', 'r', encoding='utf-8') as f:
            j_dict = json.load(f)
    except:
        j_dict = {}
    app.run()