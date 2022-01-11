import json

all_users = []
with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for user in datos:
            all_users.append(user['nick_name'])

print(all_users)