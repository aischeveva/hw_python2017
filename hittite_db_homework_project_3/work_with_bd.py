import sqlite3
import matplotlib.pyplot as plt

conn_org = sqlite3.connect('hittite.db')
conn_my = sqlite3.connect('hettsk.db')

c_org = conn_org.cursor()
c_my = conn_my.cursor()

## заполняем таблицу слов
def fill_words():
    temp_arr = []
    c_org.execute('SELECT * FROM wordforms')
    for i, row in enumerate(c_org.fetchall()):
        temp_arr.append([row[0], row[1], row[2]])
        temp_arr[i][2] = temp_arr[i][2].split('.')
        for k, j in enumerate(temp_arr[i][2]):
            if j.isupper() and k == 0:
                temp_arr[i][2][0] = ''
            elif j.isupper():
                temp_arr[i][2][0] += ''
            elif k != 0:
                temp_arr[i][2][0] += ' ' + j
        temp_arr[i][2] = temp_arr[i][2][0]
        c_my.execute('INSERT INTO words (Lemma, Wordform, Translate_w) VALUES (?, ?, ?)', temp_arr[i])
    conn_my.commit()


## заполняем таблицу глосс
def fill_glosses():
    with open('glossing_rules.txt', 'r', encoding='utf-8') as f:
        text = f.read().split('\n')
        for i, line in enumerate(text):
            text[i] = line.split(' — ')
            c_my.execute('INSERT INTO glosses (gloss, decode_gloss) VALUES (?, ?)', text[i])
    conn_my.commit()


## заполняем связь слово-глосса
def fill_word_glosses():
    c_org.execute('SELECT * FROM wordforms')
    temp_arr = []
    for i, row in enumerate(c_org.fetchall()):
        temp_arr.append([row[0], row[1], row[2]])
        temp_arr[i][2] = temp_arr[i][2].split('.')
        for gl in temp_arr[i][2]:
            if gl.isupper():
                temp_gl = (gl,)
                c_my.execute('SELECT id, gloss FROM glosses WHERE gloss=?', temp_gl)
                search_res = c_my.fetchone()
                print(gl)
                print(search_res)
                if search_res != None:
                    t = search_res[0]
                    c_my.execute('INSERT INTO word_glosses VALUES (?, ?)', [i + 1, t])
    conn_my.commit()


def count_gl():
    cases = ['NOM', 'GEN', 'LOC', 'DAT', 'DAT-LOC', 'INSTR', 'ACC', 'ABL']
    part_speech = ['ADJ', 'ADV', 'AUX',
                   'COMP', 'CONJ', 'CONN',
                   'DEM', 'INDEF', 'N', 'NUM',
                   'P', 'PART', 'PERS', 'POSS', 'PRON',
                   'PRV', 'PTCP', 'REL', 'Q', 'V', 'REFL']
    persons_numbers = ['SG', 'PL', '1PL', '1SG', '2SG', '2PL', '3SG', '3PL']
    tenses = ['PRT', 'PST', 'INF', 'MED', 'IMP']
    #rest = ['EMPH', 'ENCL', 'QUOT', 'NEG']
    c_my.execute('SELECT id_gloss FROM word_glosses')
    all_glosses = c_my.fetchall()
    d_c = {} #словарь падежей
    d_p = {} #словарь частей речи
    d_pn = {} #словарь чисел/лиц
    d_t = {} #словарь времен
    d_r = {} #словарь всего остального
    for row in all_glosses:
        temp_arr = (row[0],)
        c_my.execute('SELECT * FROM glosses WHERE id=?', temp_arr)
        temp = c_my.fetchone()[1]
        if temp in cases:
            if temp in d_c:
                d_c[temp] += 1
            else:
                d_c[temp] = 1
        elif temp in part_speech:
            if temp in d_p:
                d_p[temp] += 1
            else:
                d_p[temp] = 1
        elif temp in persons_numbers:
            if temp in d_pn:
                d_pn[temp] += 1
            else:
                d_pn[temp] = 1
        elif temp in tenses:
            if temp in d_t:
                d_t[temp] += 1
            else:
                d_t[temp] = 1
        else:
            if temp in d_r:
                d_r[temp] += 1
            else:
                d_r[temp] = 1
    return [d_c, d_p, d_pn, d_t, d_r]


def draw_gl(arr):
    x_cases = [k for k in arr[0]]
    x_parts = [i for i in arr[1]]
    x_persons = [i for i in arr[2]]
    x_tenses = [i for i in arr[3]]
    x_rest = [i for i in arr[4]]
    y_cases = [arr[0][i] for i in sorted(arr[0])]
    y_parts = [arr[1][i] for i in sorted(arr[1])]
    y_persons = [arr[2][i] for i in sorted(arr[2])]
    y_tenses = [arr[3][i] for i in sorted(arr[3])]
    y_rest = [arr[4][i] for i in sorted(arr[4])]
    egrid = (2, 3)
    ax1 = plt.subplot2grid(egrid, (0, 0))
    ax2 = plt.subplot2grid(egrid, (0, 1))
    ax3 = plt.subplot2grid(egrid, (0, 2))
    ax4 = plt.subplot2grid(egrid, (1, 0))
    ax5 = plt.subplot2grid(egrid, (1, 2))
    ax1.barh(x_cases, y_cases)
    ax2.barh(x_parts, y_parts)
    ax3.barh(x_persons, y_persons)
    ax4.barh(x_tenses, y_tenses)
    ax5.barh(x_rest, y_rest)
    plt.tight_layout()
    plt.title('Glosses comparison')
    plt.show()


#fill_words() # -- заполняем таблицу слов
#fill_glosses() # -- заполняем таблицу глосс
#fill_word_glosses() # -- устанавливаем связь между словами и глоссами
draw_gl(count_gl())
conn_org.close()
conn_my.close()
