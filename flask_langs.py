from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
app = Flask(__name__)


def op_lang():
    dic = {}
    with open('lang_codes.csv', 'r', encoding='utf-8') as fin:
        langs = fin.read().split('\n')
        for lang in langs:
            lang = lang.split(',')
            if len(lang) > 1:
                if lang[0] not in dic:
                    dic[lang[0]] = lang[1]
    return dic


@app.route('/')
def output_lang():
    dic_lang = op_lang()
    return render_template('index.html', languages=dic_lang)


@app.route('/codes/<ltrs>')
def choose_lang(ltrs):
    dic = {}
    with open('lang_codes.csv', 'r', encoding='utf-8') as fin:
        langs = fin.read().split('\n')
        for lang in langs:
            lang = lang.split(',')
            if len(lang) > 1:
                if lang[0] not in dic and lang[1].startswith(ltrs):
                    dic[lang[0]] = lang[1]
    return render_template('index.html', languages=dic)


@app.route('/not_found')
def not_found():
    return render_template('not_found.html')


@app.route('/lang/<code>')
def ret_lang(code, lang):
    dic_lang = op_lang()
    return render_template('chosen_lang.html', my_lang=lang, my_code=code)


@app.route('/form', methods=['GET'])
def give_form():
    return render_template('lang_form.html')


@app.route('/form', methods=['POST'])
def get_lang():
    dic_lang = op_lang()
    if request.args['language'] not in dic_lang:
        return redirect(url_for('not_found'))
    else:
        return redirect(url_for('ret_lang', code=dic_lang[request.args['text']], lang=request.args['text']))


if __name__ == '__main__':
    app.run()
