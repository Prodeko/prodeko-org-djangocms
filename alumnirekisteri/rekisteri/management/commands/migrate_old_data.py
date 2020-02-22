# import numpy as np
import json

from django.core.management.base import BaseCommand

from auth2.models import *
from rekisteri.models import *


class Command(BaseCommand):

    help = "Tulkkaa se vanha paskakasa"

    Education.audit_log.all().delete()
    Education.objects.all().delete()
    FamilyMember.audit_log.all().delete()
    FamilyMember.objects.all().delete()
    Honor.audit_log.all().delete()
    Honor.objects.all().delete()
    StudentOrganizationalActivity.audit_log.all().delete()
    StudentOrganizationalActivity.objects.all().delete()
    Email.audit_log.all().delete()
    Email.objects.all().delete()
    Phone.audit_log.all().delete()
    Phone.objects.all().delete()
    WorkExperience.audit_log.all().delete()
    WorkExperience.objects.all().delete()
    Interest.audit_log.all().delete()
    Interest.objects.all().delete()
    Language.audit_log.all().delete()
    Language.objects.all().delete()
    PositionOfTrust.audit_log.all().delete()
    PositionOfTrust.objects.all().delete()
    Person.objects.filter(user__is_admin=False).delete()
    User.objects.filter(is_admin=False).delete()

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        # Bring in data
        with open("old_data_files/users.json", encoding="utf8") as users_file:
            users = json.load(users_file)["data"]
        with open("old_data_files/perus.json", encoding="utf8") as persons_file:
            perus = json.load(persons_file)["data"]
        with open("old_data_files/edelt-op.json", encoding="utf8") as edelt_op_file:
            edelt_op = json.load(edelt_op_file)["data"]
        with open("old_data_files/akatkunn.json", encoding="utf8") as akatkunn_file:
            akatkunn = json.load(akatkunn_file)["data"]
        with open(
            "old_data_files/yo_kunnianosoitukset.json", encoding="utf8"
        ) as yo_kunn_file:
            yo_kunn = json.load(yo_kunn_file)["data"]
        with open(
            "old_data_files/jarjestotoiminta.json", encoding="utf8"
        ) as jarjestotoiminta_file:
            jarjestotoiminta = json.load(jarjestotoiminta_file)["data"]
        with open("old_data_files/lapset.json", encoding="utf8") as lapset_file:
            lapset = json.load(lapset_file)["data"]
        with open("old_data_files/puolisot.json", encoding="utf8") as puolisot_file:
            puolisot = json.load(puolisot_file)["data"]
        with open(
            "old_data_files/luottamustehtavat.json", encoding="utf8"
        ) as luottamustehtavat_file:
            ltehts = json.load(luottamustehtavat_file)["data"]
        with open("old_data_files/jatko-op.json", encoding="utf8") as jatko_op_file:
            jatkop = json.load(jatko_op_file)["data"]
        with open("old_data_files/sivutoimet.json", encoding="utf8") as sivutoimet_file:
            sivutoimet = json.load(sivutoimet_file)["data"]
        with open("old_data_files/vanhatyo.json", encoding="utf8") as vanhatyo_file:
            vanhatyo = json.load(vanhatyo_file)["data"]
        with open("old_data_files/vuorilinj.json", encoding="utf8") as vuorilinj_file:
            vuorilinj = json.load(vuorilinj_file)["data"]
        with open("old_data_files/tekniset-op.json", encoding="utf8") as teknop_file:
            teknop = json.load(teknop_file)["data"]

        user_id_dict = {}
        person_id_dict = {}
        user_email_dict = {}
        tekn_op_dict = {}

        without_email_users = 0
        without_email_perus = 0
        for user in users:
            email = user["email"].strip()

            if not user["email"].strip():
                email = user["username"] + "@" + "dummy.prodeko.org"

            if user["ID"] == 2189:  # sama henkilö kuin 2188
                user_id_dict[2189] = user_id_dict[2188]
                continue
            elif user["ID"] == 1183:
                continue
            elif user["ID"] == 2386:
                continue
            elif (
                user["ID"] == 797
                or user["ID"] == 2534
                or user["ID"] == 2535
                or user["ID"] == 2515
            ):
                continue

            emails = email.split(",")
            user_email_dict[user["ID"]] = emails

            u = User.objects.create_user(email=emails[0])

            user_id_dict[user["ID"]] = u
            """
            try:
            except django.db.utils.IntegrityError:
                u = User.objects.get(email=user['email'])

            user_id_dict[user['ID']] = user['email']
            #u.save()
            """

        # pprint(user_id_dict)
        for persu in perus:
            """
            if not "Sähköpostiosoite" in persu.keys() or not persu['Sähköpostiosoite'].strip():
                without_email_perus += 1
                if not persu['ID'] in user_id_dict.keys():
                    #print("käyttäjällä ei sähköpostia", persu['ID'])
                    continue
                else :
                    #print("used email from the users table for ", persu['ID'])
                    email = user_id_dict[persu['ID']].strip()
            else:
                email = persu['Sähköpostiosoite'].strip()

            #print(email)

            try:
                u = User.objects.create_user(email=email)
                u.save()
            except django.db.utils.IntegrityError:
                u = User.objects.get(email=email)

            """
            id_num = persu["ID"]

            if (
                id_num == 1183
            ):  # sama kuin 2360 mutta vanhempi entry, fiksaus loopin jälkeen
                continue
            elif id_num == 2386:  # sama kuin 1990, mutta tyhjä
                continue
            elif (
                id_num == 2257 or id_num == 2515
            ):  # täysin tyhjä entry, epäilyttävästi vesikiven maili = jotain säätöä, toinenkin tyhjä
                continue

            u = user_id_dict[id_num]

            u.first_name = persu["Etunimi"]
            u.last_name = persu["Sukunimi"]
            u.save()

            # print(u.first_name + ' ' + u.last_name)

            if id_num == 2189:  # sama henkilö
                p = person_id_dict[2188]
                id_num = 2188
            else:
                p = Person()
                p.user = u
                p.save()

            person_id_dict[persu["ID"]] = p

            p.user = u

            p.is_alumni = True

            if user_email_dict[id_num]:
                for mail in user_email_dict[id_num]:
                    # print(mail)
                    e = Email()
                    e.person = p
                    e.address = mail
                    e.save()

            if persu["Toinen nimi"]:
                if persu["Kolmas nimi"]:
                    p.middle_names = persu["Toinen nimi"] + " " + persu["Kolmas nimi"]
                else:
                    p.middle_names = persu["Toinen nimi"]

            if persu["Kutsumanimi"] and persu["Kutsumanimi"] != "NULL":
                p.preferred_name = persu["Kutsumanimi"]

            if persu["Omaa sukua"]:
                p.original_last_name = persu["Omaa sukua"]

            if persu["Syntymäpaikka"]:
                p.place_of_birth = persu["Syntymäpaikka"]

            if persu["Syntymäaika"] and persu["Syntymäaika"] != "0000-00-00":
                p.birthdate = persu["Syntymäaika"]

            if persu["Sukupuoli"]:
                if persu["Sukupuoli"] == "M":
                    p.gender = 0
                elif persu["Sukupuoli"] == "N" or persu["Sukupuoli"] == "F":
                    p.gender = 1
                else:
                    # print(persu['Sukupuoli'])
                    pass

            if persu["Siviilisääty"]:
                if persu["Siviilisääty"] == "Naimisissa":
                    p.marital_status = 0
                elif persu["Siviilisääty"] == "Naimaton":
                    p.marital_status = 1
                elif persu["Siviilisääty"] == "Avoliitossa":
                    p.marital_status = 2
                elif persu["Siviilisääty"] == "Rekisteröidyssä parisuhteessa":
                    p.marital_status = 3
                elif persu["Siviilisääty"] == "Leski":
                    p.marital_status = 4
                elif persu["Siviilisääty"] == "Eronnut":
                    p.marital_status = 5
                else:
                    print(persu["Siviilisääty"])

            if persu["Sotilasarvo"]:
                p.military_rank = persu["Sotilasarvo"]

            if persu["Ylentämisvuosi"]:
                p.promotion_year = persu["Ylentämisvuosi"]

            if persu["Katuosoite"]:
                p.address = persu["Katuosoite"]

            if persu["Postinumero"]:
                p.postal_code = persu["Postinumero"]

            if persu["Zip"]:
                p.postal_code = persu["Zip"]

            if persu["Paikkakunta"]:
                p.city = persu["Paikkakunta"]

            if persu["Maa"]:
                p.country = persu["Maa"]

            if persu["Osoitetiedot saa julkaista"]:
                if persu["Osoitetiedot saa julkaista"] == "K":
                    p.show_address_category = True

            if persu["Kotisivu"]:
                p.homepage = persu["Kotisivu"]

            if persu["Puhelinnumero"] and persu["Puhelinnumero"] != "NULL":
                num = ""
                if persu["Maasuuntanumero"] and persu["Maasuuntanumero"] != "NULL":
                    num = num + persu["Maasuuntanumero"]
                if persu["Suuntanumero"] and persu["Suuntanumero"] != "NULL":
                    num = num + persu["Suuntanumero"]
                num += persu["Puhelinnumero"]
                pn = Phone()
                pn.phone_number = num
                pn.number_type = "P"
                pn.person = p
                pn.save()

            if persu["Kakkospuhelin"] and persu["Kakkospuhelin"] != "NULL":
                num = ""
                if persu["Kakkosmaasuunta"] and persu["Kakkosmaasuunta"] != "NULL":
                    num = num + persu["Kakkosmaasuunta"]
                if persu["Kakkossuunta"] and persu["Kakkossuunta"] != "NULL":
                    num = num + persu["Kakkossuunta"]
                num += persu["Kakkospuhelin"]
                pn = Phone()
                pn.phone_number = num
                pn.number_type = "P"
                pn.person = p
                pn.save()

            if persu["Työpuhelinnumero"] and persu["Työpuhelinnumero"] != "NULL":
                num = ""
                if (
                    persu["Työmaasuuntanumero"]
                    and persu["Työmaasuuntanumero"] != "NULL"
                ):
                    num = num + persu["Työmaasuuntanumero"]
                if persu["Työsuuntanumero"] and persu["Työsuuntanumero"] != "NULL":
                    num = num + persu["Työsuuntanumero"]
                num += persu["Työpuhelinnumero"]
                pn = Phone()
                pn.phone_number = num
                pn.number_type = "W"
                pn.person = p
                pn.save()

            if persu["Vuosikurssi"]:
                p.class_of_year = persu["Vuosikurssi"]

            # Old data has some NULLs here, let's make this opt-out instead of opt-in. Pyry approved
            p.subscribe_alumnimail = True
            if persu["Sähköinen postituslista"]:
                if persu["Sähköinen postituslista"] == "E":
                    p.subscribe_alumnimail = False

            if "dummy" in p.user.email:
                p.subscribe_alumnimail = False

            if persu["Mentorointi"]:
                if persu["Mentorointi"] == "K":
                    p.mentoring = True

            if persu["Työnantaja"]:
                w = WorkExperience()
                w.person = p
                w.organisation = persu["Työnantaja"]
                if persu["Tehtävä"]:
                    w.position = persu["Tehtävä"]
                if persu["Työn aloitusvuosi"]:
                    w.start_year = persu["Työn aloitusvuosi"]

                if persu["Työpostiosoite"] or persu["Työalaosoite"]:
                    a = ""
                    if persu["Työpostiosoite"] and persu["Työpostiosoite"] != "NULL":
                        a = a + persu["Työpostiosoite"]
                    if persu["Työalaosoite"] and persu["Työpostiosoite"] != "NULL":
                        a = a + "\n" + persu["Työalaosoite"]
                    w.address = a

                if persu["Työzip"]:
                    w.postal_code = persu["Työzip"]

                if persu["Työpostinumero"]:
                    w.postal_code = persu["Työpostinumero"]

                if persu["Työpaikkakunta"]:
                    w.city = persu["Työpaikkakunta"]

                if persu["Työmaa"]:
                    w.country = persu["Työmaa"]
                w.save()

            if persu["Sukunimi (Avo)"] or persu["Etunimi (Avo)"]:
                f = FamilyMember()
                f.person = p
                if "Sukunimi (Avo)" in persu.keys():
                    f.last_name = persu["Sukunimi (Avo)"]
                if "Entinen sukunimi (Avo)" in persu.keys():
                    f.previous_last_name = persu["Entinen sukunimi (Avo)"]
                if "Etunimi (Avo)" in persu.keys():
                    f.first_name = persu["Etunimi (Avo)"]
                if "Ammatti (Avo)" in persu.keys():
                    f.profession = persu["Ammatti (Avo)"]
                # print(persu['Etunimi (Avo)'], persu['Sukunimi (Avo)'])
                f.member_type = 4
                f.save()

            if persu["Isä etunimi"] or persu["Isä sukunimi"]:
                f = FamilyMember()
                f.person = p
                if "Isä sukunimi" in persu.keys():
                    f.last_name = persu["Isä sukunimi"]
                if "Isä etunimi" in persu.keys():
                    f.first_name = persu["Isä etunimi"]
                if "Isä ammatti" in persu.keys():
                    f.profession = persu["Isä ammatti"]
                f.member_type = 1
                f.save()

            if persu["Äiti etunimi"] or persu["Äiti sukunimi"]:
                f = FamilyMember()
                f.person = p
                if "Äiti sukunimi" in persu.keys():
                    f.last_name = persu["Äiti sukunimi"]
                if "Äiti etunimi" in persu.keys():
                    f.first_name = persu["Äiti etunimi"]
                if "Äiti ammatti" in persu.keys():
                    f.profession = persu["Äiti ammatti"]
                f.member_type = 1
                f.save()

            if persu["Kielitaito"]:
                languages = persu["Kielitaito"].split(",")
                for language in languages:
                    l = Language()
                    l.person = p
                    l.language = language
                    l.save()

            if persu["Harrastukset"]:
                interests = persu["Harrastukset"].split(",")
                for interest in interests:
                    i = Interest()
                    i.person = p
                    i.title = interest
                    i.save()

            p.save()

        person_id_dict[1183] = person_id_dict[2360]
        person_id_dict[2360].previous_last_name = "Markkanen"
        person_id_dict[2360].save()
        # print(p.user.first_name + ' ' + p.user.last_name)
        person_id_dict[1183] = person_id_dict[2360]
        person_id_dict[2386] = person_id_dict[1190]
        person_id_dict[2360].previous_last_name = "Markkanen"
        person_id_dict[2360].save()
        # print(persu['Etunimi'])
        for tekn in teknop:
            if tekn["ID_perus"] == 2257:
                continue
            p = person_id_dict[tekn["ID_perus"]]
            e = Education()
            e.person = p
            if tekn["Oppilaitos"] and tekn["Oppilaitos"] != "NULL":
                e.school = tekn["Oppilaitos"]
            if tekn["Perustutkinto"] and tekn["Perustutkinto"] != "NULL":
                e.description = tekn["Perustutkinto"]
            if tekn["Koulutusohjelma"] and tekn["Koulutusohjelma"] != "NULL":
                e.field = tekn["Koulutusohjelma"]
            if tekn["Opintosuunta"] and tekn["Koulutusohjelma"] != "NULL":
                if tekn["Koulutusohjelma"] and tekn["Koulutusohjelma"] != "NULL":
                    e.field = e.field + ", " + tekn["Opintosuunta"]
                else:
                    e.field = tekn["Opintosuunta"]
            if tekn["I syventymiskohde"] and tekn["I syventymiskohde"] != "NULL":
                e.major = tekn["I syventymiskohde"]
            if tekn["II syventymiskohde"] and tekn["II syventymiskohde"] != "NULL":
                e.minor = tekn["II syventymiskohde"]
            if tekn["III syventymiskohde"] and tekn["III syventymiskohde"] != "NULL":
                e.minor += ", " + tekn["III syventymiskohde"]
            if tekn["IV syventymiskohde"] and tekn["IV syventymiskohde"] != "NULL":
                e.minor += ", " + tekn["IV syventymiskohde"]
            if tekn["V syventymiskohde"] and tekn["V syventymiskohde"] != "NULL":
                e.minor += ", " + tekn["V syventymiskohde"]
            if tekn["VI syventymiskohde"] and tekn["VI syventymiskohde"] != "NULL":
                e.minor += ", " + tekn["VI syventymiskohde"]

            if (
                tekn["Perustutkinto"] == "DI"
                or tekn["Perustutkinto"] == "Arkkit."
                or tekn["Perustutkinto"] == "TkK"
            ):
                e.degree_level = 3

            if tekn["Opinnot alkaneet"] and tekn["Opinnot alkaneet"] != "NULL":
                try:
                    e.start_year = int(tekn["Opinnot alkaneet"])
                except:
                    print("viallinen vuosi", tekn["Opinnot alkaneet"])
            if tekn["Valmistumisvuosi"] and tekn["Valmistumisvuosi"] != "NULL":
                try:
                    e.end_year = int(tekn["Valmistumisvuosi"])
                except:
                    pass

            e.save()

        for sivutoimi in sivutoimet:
            if not sivutoimi["ID_perus"] in person_id_dict.keys():
                continue
            w = WorkExperience()
            w.person = person_id_dict[sivutoimi["ID_perus"]]
            if sivutoimi["Aloitusvuosi"]:
                w.start_year = sivutoimi["Aloitusvuosi"]
            if sivutoimi["Lopetusvuosi"]:
                w.end_year = sivutoimi["Lopetusvuosi"]
            w.organisation = sivutoimi["Työnantaja"]
            w.position = sivutoimi["Tehtävä"]
            w.description = "(Sivutoimi)"

            w.save()

        for tyo in vanhatyo:
            if not tyo["ID_perus"] in person_id_dict.keys():
                continue
            w = WorkExperience()
            w.person = person_id_dict[tyo["ID_perus"]]
            if tyo["Aloitusvuosi"] and not tyo["Aloitusvuosi"] == "-":
                if "-" in tyo["Aloitusvuosi"]:
                    w.start_year = tyo["Aloitusvuosi"][:-1]
                else:
                    w.start_year = tyo["Aloitusvuosi"]
            if (
                tyo["Lopetusvuosi"]
                and not tyo["Lopetusvuosi"] == "-"
                and not tyo["Lopetusvuosi"] == "current"
            ):
                w.end_year = tyo["Lopetusvuosi"]
            w.organisation = tyo["Työnantaja"]
            w.position = tyo["Tehtävä"]

            w.save()

        for entop in edelt_op:
            e = Education()

            if not entop["ID_perus"]:
                continue
            else:
                if not entop["ID_perus"] in person_id_dict.keys():
                    continue
                p = person_id_dict[entop["ID_perus"]]
                e.person = p

            if (
                entop["Oppilaitos"]
                or entop["Tutkinto"]
                or entop["Koulutusohjelma _ Laitos"]
            ):
                if entop["Oppilaitos"]:
                    e.school = entop["Oppilaitos"]
                if entop["Tutkinto"]:
                    a = entop["Tutkinto"]
                    b = a.lower()
                    if (
                        "ylioppilas" in b
                        or "yo" in b
                        or "baccalaureat" == b
                        or "student" == b
                    ):
                        e.degree_level = 1
                        e.description = "Ylioppilastutkinto"
                    elif (
                        "high school" in b
                        or "hs diploma" in b
                        or "diploma" in b
                        or "avgå" in b
                        or "liiketa" in b
                        or "teknik" in b
                        or "opistoup" in b
                        or "abitur" == b
                        or "gcse" == b
                        or "leavin" in b
                        or "reife" in b
                        or "graduate" == b
                        or "automek" in b
                    ):
                        e.degree_level = 1
                        e.description = a
                    elif (
                        "insin" in b
                        or "ohjaaj" in b
                        or "kapteen" in b
                        or "Upseeri" == a
                        or "trade" in b
                        or "upseerin" in b
                        or "logist" in b
                    ):
                        e.degree_level = 2
                        e.description = a
                    elif "baccal" in b or "ib" in b:
                        e.degree_level = 1
                        e.description = "International Baccalaureate"
                    elif (
                        "maister" in b
                        or "magister" in b
                        or "master" in b
                        or "mba" in b
                        or "virkatut" in b
                        or "wirtschaft" in b
                        or "yleises" in b
                        or "service" in b
                        or "vordip" in b
                        or "arkkit" in b
                        or "industrial" in b
                        or "ktm" in b
                        or "fm" in b
                        or "nieur" in b
                    ):
                        e.degree_level = 3
                        e.description = a
                    elif "ekonomi" in b:
                        e.degree_level = 3
                        e.description = a
                    elif (
                        "kand" in b
                        or "bach" in b
                        or "cand" in b
                        or "civi" in b
                        or "erikoistu" in b
                    ):
                        e.degree_level = 2
                        e.description = a
                    elif "lice" in b or "lise" in b:
                        e.degree_level = 4
                        e.description = a
                    # else:
                    # print(a)
                if entop["Koulutusohjelma _ Laitos"]:
                    e.major = entop["Koulutusohjelma _ Laitos"]

            if (
                entop["Valmistumisvuosi"]
                or entop["Aloitusvuosi"]
                or entop["Tiedekunta _ Osasto"]
            ):
                if entop["Valmistumisvuosi"]:
                    e.end_year = entop["Valmistumisvuosi"]
                if entop["Aloitusvuosi"]:
                    e.start_year = entop["Aloitusvuosi"]
                if entop["Tiedekunta _ Osasto"]:
                    e.field = entop["Tiedekunta _ Osasto"]

            e.save()

        # print('KYRPÄ-----------------')

        for jatk in jatkop:
            e = Education()

            if not jatk["ID_perus"]:
                continue
            else:
                if not jatk["ID_perus"] in person_id_dict.keys():
                    continue
                p = person_id_dict[jatk["ID_perus"]]
                e.person = p

            if jatk["Oppilaitos"] or jatk["Tutkinto"] or jatk["Koulutusohjelma Laitos"]:
                if jatk["Oppilaitos"]:
                    e.school = jatk["Oppilaitos"]
                if jatk["Tutkinto"]:
                    a = jatk["Tutkinto"]
                    b = a.lower()
                    if "tekniikan tohtori" in b or "tkt" in b:
                        e.degree_level = 5
                        e.description = "Tekniikan tohtori"
                    elif (
                        "lise" in b
                        or "lice" in b
                        or "keuhkosai" in b
                        or "karexam" in b
                        or "licte" in b
                        or "ktl" in b
                        or "ll 1998" in b
                        or "tekn. lis" in b
                        or "psl" in b
                        or "tkl" in b
                        or "lääkär" in b
                    ):
                        e.degree_level = 4
                        e.description = a
                    elif (
                        "tohtori" in b
                        or "doct" in b
                        or "dr" in b
                        or "ktt" == b
                        or "ft" == b
                        or "ph.d" in b
                        or "d.sc" in b
                    ):
                        e.degree_level = 5
                        e.description = a
                    elif (
                        "maister" in b
                        or "master" in b
                        or "magister" in b
                        or "mba" in b
                        or "ekonomi" == b
                        or "ktm" in b
                        or "psm" in b
                        or "otm" == b
                        or "di" == b
                        or "graduate di" in b
                    ):
                        e.degree_level = 3
                        e.description = a
                    elif (
                        "esikunta" in b
                        or "fm" in b
                        or "vtm" in b
                        or "diploma in" in b
                        or "msc" in b
                        or "psm" in b
                    ):
                        e.degree_level = 3
                        e.description = a
                    elif (
                        "kand" in b
                        or "bach" in b
                        or "bsc" == b
                        or "insin" in b
                        or "trad" in b
                        or "bba" in b
                        or "ktk" in b
                        or "humk" in b
                        or "on" == b
                        or "oikeusnotaari" in b
                        or "vtk" in b
                    ):
                        e.degree_level = 2
                        e.description = a
                    elif "doce" in b or "dose" in b:
                        e.degree_level = 6
                        e.description = a
                    # else:
                    # print(a)
                if jatk["Koulutusohjelma Laitos"] == jatk["I Syventymiskohde"]:
                    e.major = jatk["Koulutusohjelma Laitos"]
                else:
                    if jatk["Koulutusohjelma Laitos"]:
                        e.major = jatk["Koulutusohjelma Laitos"]
                    if jatk["I Syventymiskohde"]:
                        e.major = jatk["I Syventymiskohde"]

            if (
                jatk["Valmistumisvuosi"]
                or jatk["Aloitusvuosi"]
                or jatk["Tiedekunta Osasto"]
            ):
                if jatk["Aloitusvuosi"] == "2000-2001":
                    e.start_year = 2000
                    e.end_year = 2001
                else:
                    if jatk["Valmistumisvuosi"]:
                        e.end_year = jatk["Valmistumisvuosi"]
                    if jatk["Aloitusvuosi"]:
                        e.start_year = jatk["Aloitusvuosi"]
                    if jatk["Tiedekunta Osasto"]:
                        e.field = jatk["Tiedekunta Osasto"]

            e.save()

        # print(without_email_perus, without_email_users)

        for kunn in akatkunn:
            if not kunn["ID_perus"] in person_id_dict.keys():
                continue
            h = Honor()
            h.person = person_id_dict[kunn["ID_perus"]]
            h.title = kunn["Kunnianosoitus"]
            h.organisation = kunn["Järjestö"]
            if kunn["Vuosi"] == "1996-":
                h.year = 1996
            elif kunn["Vuosi"] == "2003-2005":
                h.year = 2003
                h1 = Honor()
                h2 = Honor()
                h1.person = h.person
                h1.title = h.title
                h1.organisation = h.organisation
                h1.year = 2004
                h2.person = h.person
                h2.title = h.title
                h2.organisation = h.organisation
                h2.year = 2005
                h1.save()
                h2.save()
            elif kunn["Vuosi"]:
                h.year = kunn["Vuosi"]

            h.save()

        for kunn in yo_kunn:
            if not kunn["ID_perus"] in person_id_dict.keys():
                continue
            h = Honor()
            h.person = person_id_dict[kunn["ID_perus"]]
            h.title = kunn["Kunnianosoitus"]
            h.organisation = kunn["Jarjesto"]
            if kunn["Vuosi"]:
                h.year = kunn["Vuosi"]
            h.save()

        for v in vuorilinj:
            if not v["ID_perus"] in person_id_dict.keys():
                continue
            h = Honor()
            h.person = person_id_dict[v["ID_perus"]]
            if v["Vuosi"]:
                h.year = v["Vuosi"]

        for jtoim in jarjestotoiminta:
            s = StudentOrganizationalActivity()
            if not jtoim["ID_perus"] in person_id_dict.keys():
                continue
            s.person = person_id_dict[jtoim["ID_perus"]]
            s.organisation = jtoim["Järjestö"]
            s.position = jtoim["Tehtävä"]
            if jtoim["Aloitusvuosi"]:
                if "/" in jtoim["Aloitusvuosi"]:
                    s.start_year = jtoim["Aloitusvuosi"][:-1]
                    (s.start_year)
                else:
                    s.start_year = jtoim["Aloitusvuosi"]

            if jtoim["Lopetusvuosi"]:
                s.end_year = jtoim["Lopetusvuosi"]

            s.save()

        for lteht in ltehts:
            p = PositionOfTrust()
            if not lteht["ID_perus"] in person_id_dict.keys():
                continue
            p.person = person_id_dict[lteht["ID_perus"]]
            p.organisation = lteht["Organisaatio"]
            p.position = lteht["Tehtävä"]
            if lteht["Aloitusvuosi"].strip():
                if "-" in lteht["Aloitusvuosi"]:
                    p.start_year = lteht["Aloitusvuosi"][:-1]
                else:
                    p.start_year = lteht["Aloitusvuosi"]
            if lteht["Lopetusvuosi"].strip() and not "-" == lteht["Lopetusvuosi"]:
                p.end_year = lteht["Lopetusvuosi"]
            p.save()

        for puoliso in puolisot:
            f = FamilyMember()
            if not puoliso["ID_perus"] in person_id_dict.keys():
                continue
            f.person = person_id_dict[puoliso["ID_perus"]]
            if puoliso["Etunimi (P)"]:
                f.first_name = puoliso["Etunimi (P)"]
            if puoliso["Sukunimi (P)"]:
                f.last_name = puoliso["Sukunimi (P)"]
            if puoliso["Entinen sukunimi (P)"]:
                f.original_last_name = puoliso["Entinen sukunimi (P)"]
            if puoliso["Avioitumisvuosi"].strip():
                f.since = puoliso["Avioitumisvuosi"]
            if puoliso["Erovuosi"].strip():
                f.until = puoliso["Erovuosi"]
            f.member_type = 3

            f.save()

        for lapsi in lapset:
            f = FamilyMember()
            if not lapsi["ID_perus"] in person_id_dict.keys():
                continue
            f.person = person_id_dict[lapsi["ID_perus"]]
            if lapsi["Etunimi (L)"]:
                f.first_name = lapsi["Etunimi (L)"]
            if lapsi["Sukunimi (L)"]:
                f.last_name = lapsi["Sukunimi (L)"]
            if lapsi["Syntymävuosi"].strip():
                f.since = lapsi["Syntymävuosi"]
            f.member_type = 0

            f.save()
        """
        users = np.loadtxt('old_data_files/users_taulu.csv', delimiter=';', dtype='str')
        perus = np.loadtxt('old_data_files/perus_taulu.csv', delimiter=';', dtype='str')
        akatkunn = np.loadtxt('old_data_files/akatkunn_taulu.csv', delimiter=';', dtype='str')
        lapset = np.loadtxt('old_data_files/lapset_taulu.csv', delimiter=';', dtype='str')
        edelt_op = np.loadtxt('old_data_files/edelt-op_taulu.csv', delimiter=';', dtype='str')
        jatko_op = np.loadtxt('old_data_files/jatko-op_taulu.csv', delimiter=';', dtype='str')
        jarjestotoim = np.loadtxt('old_data_files/jarjestotoim_taulu.csv', delimiter=';', dtype='str')
        luottamusteht = np.loadtxt('old_data_files/luottamusteht_taulu.csv', delimiter=';', dtype='str')
        puolisot = np.loadtxt('old_data_files/puolisot_taulu.csv', delimiter=';', dtype='str')
        sivutoimet = np.loadtxt('old_data_files/sivutoimet_taulu.csv', delimiter=';', dtype='str')
        tekniset_op = np.loadtxt('old_data_files/tekniset-op_taulu.csv', delimiter=';', dtype='str')
        vanhatyo = np.genfromtxt('old_data_files/vanhatyo_taulu.csv', delimiter=';', dtype='str')
        vuorilinj = np.loadtxt('old_data_files/vuorilinj_taulu.csv', delimiter=';', dtype='str')
        yo_kunn = np.genfromtxt('old_data_files/yo_kunnianosoitukset_taulu.csv', delimiter=';', dtype='str')

        print(users[0])

        # Tee tähän dict noista tauluista, joista pitää id:llä hakea tavarat
        perus_dict = 0

        # Create objects without headers, update variable to contain just the data rows
        users_data = np.delete(users, (0), axis=0)
        perus_data = np.delete(perus, (0), axis=0)
        akatkunn_data = np.delete(akatkunn, (0), axis=0)
        lapset_data = np.delete(lapset, (0), axis=0)
        edelt_op_data = np.delete(edelt_op, (0), axis=0)
        jatko_op_data = np.delete(jatko_op, (0), axis=0)
        jarjestotoim_data = np.delete(jarjestotoim, (0), axis=0)
        luottamusteht_data = np.delete(luottamusteht, (0), axis=0)
        puolisot_data = np.delete(puolisot, (0), axis=0)
        sivutoimet_data = np.delete(sivutoimet, (0), axis=0)
        tekniset_op_data = np.delete(tekniset_op, (0), axis=0)
        vanhatyo_data = np.delete(vanhatyo, (0), axis=0)
        vuorilinj_data = np.delete(vuorilinj, (0), axis=0)
        yo_kunn_data = np.delete(yo_kunn, (0), axis=0)

        #print(users[:5])
        """

        """
        for useri in users:
            perus_object =
            u = User(email=useri[3], )
            #do shiz
            #save da shiz
            email = models.EmailField(
                verbose_name='email address',
                max_length=255,
                unique=True,
            )
            first_name = models.CharField(max_length=30, null=True)
            last_name = models.CharField(max_length=30, null=True)
            is_active = models.BooleanField(default=True)
            is_admin = models.BooleanField(default=False)
        """
