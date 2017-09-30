import re


def clean(a):
    regClean = re.compile('<.*?>', flags=re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    a = regSpace.sub('', a)
    a = regClean.sub('', a)
    a = re.sub('&nbsp;', '', a)
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
    topic = clean(topic[0]).lower()
    return topic


def get_header(text):
    regHeader = re.compile('<h1 class="page-title">.*?</h1>', flags=re.DOTALL)
    header = regHeader.findall(text)
    header = clean(header[0])
    return header


def get_text(text):
    regText = re.compile('<div class="text">.*?</div>', flags=re.DOTALL)
    textA = regText.findall(text)
    textA = clean(textA[0])
    return textA


class gazeta:
    def __init__(self, text):
        self.author = get_author(text)
        self.header = get_header(text)
        self.year = get_created(text).split('.')[2]
        self.month = get_created(text).split('.')[1]
        self.topic = get_topic(text)
        self.textN = get_text(text)
