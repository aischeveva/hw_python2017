
# coding: utf-8

# In[21]:

import json
import urllib.request
import time

user = 'whyisjake'
url = 'https://api.github.com/users/%s/repos' % user
users = ['elmiram', 'nevmenandr', 'shwars', 'JelteF', 'timgraham', 'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake']

response = urllib.request.urlopen(url)
text = response.read().decode('utf-8')
data = json.loads(text)

print(len(data))
lang_arr = {}
for i in data:
    #print('%s %s'%(i['name'], i['description']))
    if i['language'] not in lang_arr:
        lang_arr[i['language']] = 1
    else:
        lang_arr[i['language']] += 1
#print(lang_arr)

maxim = 0
max_us = ''
lang_arr1 = {}
for user in users:
    url = 'https://api.github.com/users/%s/repos' % user
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token 8ce69c608c02eb9a555161c2e4fe77632275cd05')
    result = urllib.request.urlopen(req)
    text = result.read().decode('utf-8')
    data = json.loads(text)
    if len(data) >= maxim:
        maxim = len(data)
        max_us = user
    for i in data:
        if i['language'] not in lang_arr1:
            lang_arr1[i['language']] = 1
        else:
            lang_arr1[i['language']] += 1
print(max_us)
print(lang_arr1)


# In[ ]:



