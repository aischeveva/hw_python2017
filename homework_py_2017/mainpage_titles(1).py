import urllib.request
import re

def get_titles():
    req = urllib.request.Request('https://hron.ru/')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        regTitleMain = re.compile('<a class="tape-title.*?" .*?>', flags=re.DOTALL)
        regTitleLate = re.compile('<li class="clearfix".*?</a>', flags=re.DOTALL)
        titles_late = regTitleLate.findall(html)
        titles_main = regTitleMain.findall(html)
        clean_titles_main = []
        clean_titles_late = []
        regCleanLate1 = re.compile('<.*?>', flags=re.DOTALL)
        regCleanLate2 = re.compile('\s{2,}', flags=re.DOTALL)
        regCleanMain = re.compile('.+?title="(.*?)">', flags=re.DOTALL)
        for title in titles_main:
            clean_t = regCleanMain.sub('\g<1>', title)
            clean_titles_main.append(clean_t)
        for title in titles_late:
            clean_t = regCleanLate1.sub('', title)
            clean_t1 = regCleanLate2.sub('', clean_t)
            clean_titles_late.append(clean_t1)
        with open('titles.txt', 'w', encoding='utf-8') as fout:
            fout.write('Главные новости:\n')
            for title in clean_titles_main:
                fout.write('%s\n' %title)
            fout.write('Последние новости:\n')
            for title in clean_titles_late:
                fout.write('%s\n' %title)


def main():
    get_titles()


if __name__ == '__main__':
    main()