__author__ = 'Sony'
import re
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


def get_values():
    with open('nanai-vowels.csv', 'r', encoding='utf-8') as f:
        text = f.read()
    text = re.sub('(and|eak|nchb|eik|ltk|rab|ssb);', '', text)
    text = text.split()
    for i, line in enumerate(text):
        text[i] = line.split(';')
    text.pop(0)
    return text


def get_whatta_draw(origin_array):
    arr_m_I_d = []
    arr_m_I_n = []
    arr_f_I_d = []
    arr_f_I_n = []
    arr_m_i_d = []
    arr_m_i_n = []
    arr_f_i_d = []
    arr_f_i_n = []
    arr_m_e_d = []
    arr_m_e_n = []
    arr_f_e_d = []
    arr_f_e_n = []
    for line in origin_array:
        if line[0] == 'm':
            if line[1] == 'Dzhuen':
                if line[2] == 'I':
                    arr_m_I_d.append([line[3], line[4]])
                elif line[2] == 'i':
                    arr_m_i_d.append([line[3], line[4]])
                else:
                    arr_m_e_d.append([line[3], line[4]])
            else:
                if line[2] == 'I':
                    arr_m_I_n.append([line[3], line[4]])
                elif line[2] == 'i':
                    arr_m_i_n.append([line[3], line[4]])
                else:
                    arr_m_e_n.append([line[3], line[4]])
        else:
            if line[1] == 'Dzhuen':
                if line[2] == 'I':
                    arr_f_I_d.append([line[3], line[4]])
                elif line[2] == 'i':
                    arr_f_i_d.append([line[3], line[4]])
                else:
                    arr_f_e_d.append([line[3], line[4]])
            else:
                if line[2] == 'I':
                    arr_f_I_n.append([line[3], line[4]])
                elif line[2] == 'i':
                    arr_f_i_n.append([line[3], line[4]])
                else:
                    arr_f_e_n.append([line[3], line[4]])
    temp = [arr_m_I_n, arr_m_i_n, arr_m_e_n, arr_m_I_d, arr_m_i_d, arr_m_e_d, arr_f_I_n, arr_f_i_n, arr_f_e_n, arr_f_I_d, arr_f_i_d, arr_f_e_d]
    res_arr = []
    for vill in temp:
        t1 = 0
        t2 = 0
        for vowel in vill:
            t1 += float(vowel[0])
            t2 += float(vowel[1])
        res_arr.append([t1/len(vill), t2/len(vill)])
    return res_arr


def draw_smth(wh_draw):
    plt.scatter(wh_draw[0][0], wh_draw[0][1], c='b', label='I, m, Naikhin')
    plt.scatter(wh_draw[1][0], wh_draw[1][1], c='navy', marker='s', label='i, m, Naikhin')
    plt.scatter(wh_draw[2][0], wh_draw[2][0], c='royalblue', marker='^', label='e, m, Naikhin')
    plt.scatter(wh_draw[3][0], wh_draw[3][1], c='b', marker='1', label='I, m, Dzhuen')
    plt.scatter(wh_draw[4][0], wh_draw[4][1], c='navy', marker='2', label='i, m, Dzhuen')
    plt.scatter(wh_draw[5][0], wh_draw[5][0], c='royalblue', marker='3', label='e, m, Dzhuen')
    plt.scatter(wh_draw[6][0], wh_draw[6][1], c='plum', label='I, f, Naikhin')
    plt.scatter(wh_draw[7][0], wh_draw[7][1], c='salmon', marker='s', label='i, f, Naikhin')
    plt.scatter(wh_draw[8][0], wh_draw[8][0], c='red', marker='^', label='e, f, Naikhin')
    plt.scatter(wh_draw[9][0], wh_draw[9][1], c='plum', marker='1', label='I, f, Dzhuen')
    plt.scatter(wh_draw[10][0], wh_draw[10][1], c='salmon', marker='2', label='i, f, Dzhuen')
    plt.scatter(wh_draw[11][0], wh_draw[11][0], c='red', marker='3', label='e, f, Dzhuen')
    plt.title('Форманты')
    plt.ylabel('F2')
    plt.xlabel('F1')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    draw_smth(get_whatta_draw(get_values()))