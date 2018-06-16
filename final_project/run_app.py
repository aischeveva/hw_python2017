from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def start_page():
    return render_template('main_page.html')


@app.route('/paranoid/1')
def paranoid1():
    return render_template('paranoid/1.html')

@app.route('/paranoid/2')
def paranoid2():
    return render_template('paranoid/2.html')

@app.route('/paranoid/3')
def paranoid3():
    return render_template('paranoid/3.html')

@app.route('/paranoid/4')
def paranoid4():
    return render_template('paranoid/4.html')

@app.route('/paranoid/5')
def paranoid5():
    return render_template('paranoid/5.html')

@app.route('/paranoid/6')
def paranoid6():
    return render_template('paranoid/6.html')

@app.route('/paranoid/7')
def paranoid7():
    return render_template('paranoid/7.html')

@app.route('/paranoid/8')
def paranoid8():
    return render_template('paranoid/8.html')

@app.route('/paranoid')
def paranoid9():
    return render_template('paranoid/all.html')


@app.route('/crikley/1')
def cr1():
    return render_template('crikley/1.html')

@app.route('/crikley/2')
def cr2():
    return render_template('crikley/2.html')

@app.route('/crikley/3')
def cr3():
    return render_template('crikley/3.html')

@app.route('/crikley')
def cr():
    return render_template('crikley/all.html')

@app.route('/robbery/1')
def rb1():
    return render_template('robbery/1.html')

@app.route('/robbery/2')
def rb2():
    return render_template('robbery/2.html')

@app.route('/robbery')
def rb():
    return render_template('robbery/all.html')

@app.route('/escape/1')
def e1():
    return render_template('escape/1.html')

@app.route('/escape')
def e():
    return render_template('escape/all.html')

@app.route('/hamarinn/1')
def h1():
    return render_template('hamarinn/1.html')

@app.route('/hamarinn/2')
def h2():
    return render_template('hamarinn/2.html')

@app.route('/hamarinn/3')
def h3():
    return render_template('hamarinn/3.html')

@app.route('/hamarinn/4')
def h4():
    return render_template('hamarinn/4.html')

@app.route('/hamarinn')
def h():
    return render_template('hamarinn/all.html')

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)