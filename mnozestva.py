import urllib.request
import re
import html.parser    


def get_news():
    ref = ["https://faktom.ru/19867_uchenye__drevnie_zhenshhiny_imeli_silnye_ruki_wilson2034",
           "https://www.kp.ru/daily/26764/3796606/",
           "https://www.rusdialog.ru/news/128392_1512107149",
           "https://naked-science.ru/article/sci/doistoricheskie-zhenshchiny-prevzoshli",
           "https://riafan.ru/1002542-uchenye-vyyasnili-chem-drevnie-zhenshiny-byli-luchshe-sovremennykh"]
    a = []
    for r in ref:
        with urllib.request.urlopen(r) as page:
            text = page.read().decode()
        a.append(text)
    return a


def clear_it(a):
    import html
    r_fan = re.compile('<div class="single_block_content_txt onrelap js-mediator-article ">.+?</div>', flags=re.DOTALL)
    r_naked = re.compile('<div class="views-field views-field-php">.+?</div>', flags=re.DOTALL)
    r_fak = re.compile('<section class="news">.+?</section>', flags=re.DOTALL)
    r_kp = re.compile('<div class="text js-mediator-article" id="hypercontext">.+?</div>', flags=re.DOTALL)
    r_d = re.compile('<div class="news-text" itemprop="articleBody">.+?</div>', flags=re.DOTALL)
    a[0] = r_fak.findall(a[0])[0]
    a[1] = r_kp.findall(a[1])[0]
    a[2] = r_d.findall(a[2])[0]
    a[3] = r_naked.findall(a[3])[0]
    a[4] = r_fan.findall(a[4])[0]
    r_sc = re.compile('<.*?>', flags=re.DOTALL)
    r_sp = re.compile('\s{2,}', flags=re.DOTALL)
    for i, te in enumerate(a):
        a[i] = r_sc.sub('', te)
        a[i] = r_sp.sub('', a[i]) 
        a[i] = html.parser.HTMLParser().unescape(a[i])
        a[i] = a[i].split()
        a[i] = set(a[i])
    return(a)
    
def fin(a):
    rez = a[0] ^ a[1] ^ a[2] ^ a[3] ^ a[4]
    print(rez)

fin(clear_it(get_news()))
