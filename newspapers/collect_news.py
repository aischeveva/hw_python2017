import urllib.request
import gazeta_class
import time
import os
import article_work


def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode()
    except:
        print('Error at', pageUrl)
        return
    return text


def html_array():
    u_link = 'https://hron.ru/news/read/'
    html_arr = []
    #53453
    for i in range(1, 1000):
        temp = gazeta_class.gazeta(download_page(u_link + str(i)))
        temp.source = u_link + str(i)
        html_arr.append(temp)
        #time.sleep(1)
    return html_arr

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_dirs(arr):
    t = 0
    for article in arr:
        path_plain = 'ohron' + os.sep + 'plain' + os.sep + article.year + os.sep + article.month
        path_xml = 'ohron' + os.sep + 'mystem-xml' + os.sep + article.year + os.sep + article.month
        path_pstem = 'ohron' + os.sep + 'mystem-plain' + os.sep + article.year + os.sep + article.month
        check_path(path_plain)
        check_path(path_xml)
        check_path(path_pstem)
        article.path = path_plain + os.sep + str(t) + '.txt'
        article_work.create_plain(article)
        article_work.create_mplain(article, str(t))
        article_work.create_mxml(article, str(t))
        t += 1


def write_xml():
    plain_path = 'ohron' + os.sep + 'plain'
    xml_path = 'ohron' + os.sep + 'mystem-xml'
    mystem_plain = 'ohron' + os.sep + 'mystem-plain'
    lstI = os.listdir(plain_path)
    for d1 in lstI:
        lstJ = os.listdir(plain_path + os.sep + d1)
        print(lstJ)
        for d2 in lstJ:
            print(d2)
            article_work.mystem_xml(xml_path + os.sep + d1 + os.sep + d2, xml_path + os.sep + d1 + os.sep + d2)
            article_work.mystem_plain(mystem_plain + os.sep + d1 + os.sep + d2, mystem_plain + os.sep + d1 + os.sep + d2)


def create_table(arr):
    with open('ohron' + os.sep + 'metadata.csv', 'w', encoding='utf-8') as meta_file:
        meta_file.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
        base_str = '%s\t%s\t \t \t%s\t%s\tпублицистика\t \t \t%s\t \tнейтральный\tн-возраст\tн-уровень\tгородская\t%s\tОрская хроника\t \t%s\tгазета\tРоссия\tОренбургская область\tru\n'
        for lne in arr:
            meta_file.write(base_str % (lne.path, lne.author, lne.header, lne.created, lne.topic, lne.source, lne.year))


def main():
    if not os.path.exists('ohron'):
        os.makedirs('ohron' + os.sep + 'plain')
        os.makedirs('ohron' + os.sep + 'mystem-xml')
        os.makedirs('ohron' + os.sep + 'mystem-plain')
    arr = html_array()
    create_table(arr)
    create_dirs(arr)
    write_xml()



if __name__ == '__main__':
    main()