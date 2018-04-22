import urllib.request
import json
import config
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def download_posts():
    users = {}
    post_comm = {} #словарь по типу id поста : текст, комменты
    for i in range(0, 5):
        offset = i * 100
        req = urllib.request.Request('https://api.vk.com/method/'
                                     'wall.get?domain=evil_hand_made&extended=1&fields=city,bdate&count=100&v=5.74&offset=' + str(offset) +
                                     '&access_token=' + config.TOKEN) #ключи лежит в файле config.py, грузить на гит я его, конечно же, не буду
        with urllib.request.urlopen(req) as response:  # открываем соединение с сайтом
            html = response.read().decode('utf-8')
            arr = json.loads(html)
        for j in range(0, 100):
            post_comm[arr['response']['items'][j]['id']] = [arr['response']['items'][j]['text'],
                                                            arr['response']['items'][j]['comments']['count']] #потом в этот массив добавим коммы
            if 'signer_id' in arr['response']['items'][j]: #считаем пользователей постов, если не анон
                if arr['response']['items'][j]['signer_id'] in users: #если пользователь уже оставлял пост, добавим длину в массив, среднее посчитаем потом
                    users[arr['response']['items'][j]['signer_id']]['com_len'].append(len(arr['response']['items'][j]['text'].split()))
                else:
                    users[arr['response']['items'][j]['signer_id']] = {'com_len': [len(arr['response']['items'][j]['text'].split())]}
        #print(users)
        for j in range(0, len(arr['response']['profiles'])):
            if arr['response']['profiles'][j]['id'] != 60861648 and arr['response']['profiles'][j]['id'] in users:
                users[arr['response']['profiles'][j]['id']] = get_user_info(arr['response']['profiles'][j],
                                                                            users[arr['response']['profiles'][j]['id']])
    for user in users:
        if len(users[user]['com_len']) >= 1:
            temp = 0
            for post in users[user]['com_len']:
                temp += post
            users[user]['com_len'] = temp / len(users[user]['com_len'])
    return [post_comm, users]


def download_commenz(dic):
    users = {}
    for k in dic:
        temp = []
        if dic[k][1] > 100:
            of = int(dic[k][1]/100)
            for i in range(0, of):
                offset = 100 * i
                req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-60861648&post_id='
                                             + str(k) + '&count=100&extended=1&fields=bdate,city&v=5.74&offset=' + str(offset)
                                             + '&access_token=' + config.TOKEN)  # ключи лежит в файле config.py, грузить на гит я его, конечно же, не буду
                with urllib.request.urlopen(req) as response:  # открываем соединение с сайтом
                    html = response.read().decode('utf-8')
                    arr = json.loads(html)
                for j in range(0, len(arr['response']['items'])):
                    temp.append(arr['response']['items'][j]['text'])
                    #считаем пользователей комментов
                    if arr['response']['items'][j]['from_id'] != 60861648:
                        if arr['response']['items'][j]['from_id'] in users:  # если пользователь уже оставлял коммент, см как для постов
                            users[arr['response']['items'][j]['from_id']]['com_len'].append(len(arr['response']['items'][j]['text'].split()))
                        else:
                            users[arr['response']['items'][j]['from_id']] = {'com_len': [len(arr['response']['items'][j]['text'].split())]}
                for j in range(0, len(arr['response']['profiles'])):
                    if arr['response']['profiles'][j]['id'] > 0:
                        users[arr['response']['profiles'][j]['id']] = get_user_info(arr['response']['profiles'][j], users[arr['response']['profiles'][j]['id']])
        else:
            req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-60861648&post_id='
                                         + str(k) + '&count=' + str(dic[k][1]) + '&extended=1&fields=bdate,city&v=5.74&access_token=' + config.TOKEN)
            with urllib.request.urlopen(req) as response:  # открываем соединение с сайтом
                html = response.read().decode('utf-8')
                arr = json.loads(html)
            for j in range(0, len(arr['response']['items'])):
                temp.append(arr['response']['items'][j]['text'])
                #все еще считаем юзверей
                if arr['response']['items'][j]['from_id'] > 0:
                    if arr['response']['items'][j]['from_id'] in users:  # если пользователь уже оставлял пост, см выше
                        users[arr['response']['items'][j]['from_id']]['com_len'].append(len(arr['response']['items'][j]['text'].split()))
                    else:
                        users[arr['response']['items'][j]['from_id']] = {'com_len': [len(arr['response']['items'][j]['text'].split())]}
            for j in range(0, len(arr['response']['profiles'])):
                if arr['response']['profiles'][j]['id'] != 60861648:
                    users[arr['response']['profiles'][j]['id']] = get_user_info(arr['response']['profiles'][j],
                                                                                users[arr['response']['profiles'][j]['id']])
        dic[k].append(temp)
    for user in users:
        if len(users[user]['com_len']) >= 1:
            temp = 0
            for post in users[user]['com_len']:
                temp += post
            users[user]['com_len'] = temp / len(users[user]['com_len'])
    return [dic, users]


def write_file(dic):
    with open('results_vk.txt', 'w', encoding='utf-8') as fout:
        for k in dic:
            fout.write('Пост id {0}\n'.format(k))
            fout.write('\t{0}\n\n\tКомментарии\n'.format(dic[k][0]))
            for comment in dic[k][2]:
                fout.write('\t\t{0}\n'.format(comment))


def draw_post_comm(dic):
    ration = {}
    for k in dic:
        text_post = len(dic[k][0].split())
        text_comm = 0
        for comm in dic[k][2]:
            text_comm += len(comm.split())
        if len(dic[k][2]) != 0:
            text_comm = text_comm/len(dic[k][2])
        if text_post in ration: #если пост такой длины уже встречался, то считаем среднее между их средними коментами
            ration[text_post] = (ration[text_post] + text_comm)/2
        else:
            ration[text_post] = text_comm
    post_len = [post for post in ration]
    comm_len = [ration[post] for post in ration]
    plt.bar(post_len, comm_len)
    plt.title('Посты и комменты')
    plt.ylabel('Средняя длина коммента')
    plt.xlabel('Длина поста')
    plt.savefig('post_com.png')
    plt.show()


def get_user_info(prof, a):
    if 'city' in prof:
        if 'title' in prof['city']:
            a['city'] = prof['city']['title']
        else:
            a['city'] = prof['city']['id']
    else:
        a['city'] = 'undefined'
    if 'bdate' in prof:
        date = prof['bdate'].split('.')
        if len(date) == 3:
            a['age'] = 2018 - int(date[2])
        else:
            a['age'] = 'undefined'
    else:
        a['age'] = 'undefined'
    return a


def count_post_city(user_post):
    cities = {}
    for user in user_post:
        if 'city' in user_post[user]:
            if user_post[user]['city'] in cities:
                cities[user_post[user]['city']].append(user_post[user]['com_len'])
            else:
                cities[user_post[user]['city']] = [user_post[user]['com_len']]
    for city in cities:
        temp = 0
        for l in cities[city]:
            temp += l
        cities[city] = temp / len(cities[city])
    return cities


def count_age(user_post):
    ages = {}
    for user in user_post:
        if 'age' in user_post[user]:
            if user_post[user]['age'] in ages:
                ages[user_post[user]['age']].append(user_post[user]['com_len'])
            else:
                ages[user_post[user]['age']] = [user_post[user]['com_len']]
    for age in ages:
        temp = 0
        for l in ages[age]:
            temp += l
        ages[age] = temp / len(ages[age])
    return ages

def draw_it(posts, comms, savename):
    for post in posts: #объединим два словаря, чтобы информация по постам лежала и в комментах {город: [комменты, посты]}
        if post in comms:
            comms[post] = [comms[post] * (-1), posts[post]]
        else:
            comms[post] = [0, posts[post]]
    for comm in comms:
        if comm not in posts:
            comms[comm] = [comms[comm] * (-1), 0]
    data_fr = pd.DataFrame({'city': [city for city in comms], 'comment': [comms[city][0] for city in comms], 'post': [comms[city][1] for city in comms]})
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    # Plot the posts
    sns.set_color_codes("pastel")
    sns.barplot(x="city", y="post", data=data_fr, label="Посты", color="g")
    # Plot the comments
    sns.set_color_codes("muted")
    sns.barplot(x="city", y="comment", data=data_fr, label="Комменты", color="r")
    plt.xticks(rotation=90)
    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(ylabel="", xlabel="Средняя длина текста")
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(savename)
    plt.show()


if __name__ == '__main__':
    d = download_posts()
    dd = download_commenz(d[0])
    write_file(dd[0])
    draw_post_comm(dd[0])
    draw_it(count_post_city(d[1]), count_post_city(dd[1]), 'city.png')
    draw_it(count_age(d[1]), count_age(dd[1]), 'age.png')
