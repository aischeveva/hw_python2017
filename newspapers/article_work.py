import os


def create_plain(article):
    head_str = '@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n\n'
    with open(article.path, 'w', encoding='utf-8') as fout:
           fout.write(head_str % (article.author, article.header, article.created, article.topic, article.source))
           fout.write(article.textN)


def create_mxml(article, t):
    xml_path = 'ohron' + os.sep + 'mystem-xml' + os.sep + article.year + os.sep + article.month
    with open(xml_path + os.sep + t + '.txt', 'w', encoding='utf-8') as fout:
        fout.write(article.textN)


def create_mplain(article, t):
    mplain_path = 'ohron' + os.sep + 'mystem-plain' + os.sep + article.year + os.sep + article.month
    with open(mplain_path + os.sep + t + '.txt', 'w', encoding='utf-8') as fout:
        fout.write(article.textN)


def mystem_xml(path, fin_dir):
    lst = os.listdir(path)
    n = len(lst)
    temp = 0
    #print(lst)
    for fl in lst:
        #print(fl)
        os.system(r"mystem.exe " + '-cnid --format xml ' + path + os.sep + fl + ' ' + fin_dir + os.sep + 'x' + fl)
        os.remove(fin_dir + os.sep + fl)
        temp += 1
        if temp == n:
            return


def mystem_plain(path, fin_dir):
    lst = os.listdir(path)
    n = len(lst)
    temp = 0
    for fl in lst:
        os.system(r"mystem.exe " + '-cid ' + path + os.sep + fl + ' ' + fin_dir + os.sep + 'p' + fl)
        os.remove(fin_dir + os.sep + fl)
        temp += 1
        if temp == n:
            return