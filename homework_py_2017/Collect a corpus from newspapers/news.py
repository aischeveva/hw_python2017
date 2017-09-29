import re
import time
import urllib.request
import os


def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode()
    except:
        print('Error at', pageUrl)
        return
    return text


def html_array():
    uLink = 'https://hron.ru/news/read/'
    htmlArr = []
    #53453
    for i in range(1, 11):
        htmlArr.append([download_page(uLink + str(i)), uLink + str(i)])
        time.sleep(2)
    return htmlArr


def create_table(arr):
    with open('metadata.csv', 'w', encoding='utf-8') as metaFile:
        metaFile.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
        baseStr = '%s\t%s\t \t \t%s\t%s\tпублицистика\t \t \t%s\t \tнейтральный\tн-возраст\tн-уровень\tгородская\t%s\tОрские хроники\t \t%s\tгазета\tРоссия\tОренбургская область\tru\n'
        path = ''
        author = ''
        header = ''
        created = ''
        topic = ''
        source = ''
        publ_year = ''
        for lne in arr:
            author = get_author(lne[0])
            header = get_header(lne[0])
            created = get_created(lne[0])
            topic = get_topic(lne[0])
            source = lne[1]
            metaFile.write(baseStr % (path, author, header, created, topic, source, publ_year))

def clean(a):
    regClean = re.compile('<.*?>', flags=re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    a = regSpace.sub('', a)
    a = regClean.sub('', a)
    return a


def get_author(text):
    regAuthor = re.compile('<li class="detail author">.+?</li>', flags=re.DOTALL)
    author = regAuthor.findall(text)
    if len(author) == 0:
        return 'Noname'
    else:
        author = clean(author[0])
        return author


def get_created(text):
    regCreated = re.compile('<li class="detail date">.*?</li>', flags=re.DOTALL)
    created = regCreated.findall(text)
    created = clean(created[0])
    created = re.sub('-', '.', created)
    return created


def get_topic(text):
    regTopic = re.compile('<li class="detail category">.*?</li>', flags=re.DOTALL)
    topic = regTopic.findall(text)
    topic = clean(topic[0])
    return topic


def get_header(text):
    regHeader = re.compile('<h1 class="page-title">.*?</h1>', flags=re.DOTALL)
    header = regHeader.findall(text)
    header = clean(header[0])
    return header


def main():
    create_table(html_array())


if __name__ == '__main__':
    main()