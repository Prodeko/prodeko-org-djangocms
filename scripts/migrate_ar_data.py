"""
Script to migrate alumnirekisteri data conform 
to prodeko-org-djangocms model hierarchy.

1. python3 manage.py dumpdata > alumnirekisteri_db.json
2. Backup database with mysqldump and manage.py dumpdata
3. DROP DATABASE prodekoorg
4. Run this script to generate .json files that are compatible with the database schema
5. python3 manage.py loaddata --exclude auth --exclude admin --exclude contenttypes --verbosity 3 ar_persons.json
6. python3 manage.py loaddata --exclude auth --exclude admin --exclude contenttypes --verbosity 3 ar_other.json
"""

import sys
import os
import django
import json
from django.contrib.auth import get_user_model

sys.path.append("prodekoorg")
os.environ["DJANGO_SETTINGS_MODULE"] = "prodekoorg.settings"
django.setup()


with open("alumnirekisteri_db.json") as f:
    d = json.load(f)

users = []
persons = []
other = []
for o in d:
    if o["model"] == "auth2.user":
        users.append(o)
    elif o["model"] == "rekisteri.person":
        persons.append(o)
    elif not o["model"] == "sessions.session":
        if (
            "fields" in o
            and "model" in o["fields"]
            and o["fields"]["model"].endswith("auditlogentry")
        ):
            pass
        if "model" in o and o["model"].endswith("auditlogentry"):
            pass
        else:
            other.append(o)

User = get_user_model()

new_persons = []

for u in users:
    first_name = u["fields"]["first_name"] if u["fields"]["first_name"] else ""
    last_name = u["fields"]["last_name"] if u["fields"]["last_name"] else ""
    try:
        user = User.objects.create_user(
            email=u["fields"]["email"],
            password=u["fields"]["password"],
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )
    except:
        print(f"Exeption!\n{last_name} - {first_name} \n")
    uid = u["pk"]
    for p in persons:
        if p["fields"]["user"] == uid:
            new_person = p.copy()
            new_person["fields"]["user"] = user.pk
            new_persons.append(new_person)


with open("ar_persons.json", "w") as f:
    json.dump(new_persons, f)

with open("ar_other.json", "w") as f:
    json.dump(other, f)
