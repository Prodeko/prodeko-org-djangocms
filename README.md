# Prodeko.org :tv::rainbow:

Tuotantotalouden kilta Prodekon Django-pohjaiset nettisivut.

---

Prodeko.org projekti käyttää Django versiota 2.1.

### Vaatimukset

#### Docker

Lataa [docker](https://docs.docker.com/install/).

```
$ docker-compose up  # Kehitysympäristön käynnistys
```

### Kehittäminen

Kehitysympäristön käynnistys luo uuden Django käyttäjän:

- Käyttäjä: **webbitiimi@prodeko.org**
- Salasana: **kananugetti**

### Deployas palvelimelle

1. Virtualenv päälle `source venv/bin/activate`
2. Collectaa staattiset tiedostot `python3 manage.py collectstatic`
3. Käynnistä apache uudestaan `sudo service apache2 restart`
4. Tarkista näyttävätkö sivut toimivan [djangocms.prodeko.org](https://djangocms.prodeko.org)

Jos törmäät "ImportError: Couldn't import Django..." erroriin, vaihda käyttäjä roottiin (`sudo su`) ja tee kohdat 2. ja 3. uudestaan.

### Testaus

Testit saa ajettua komennolla `python3 manage.py test -v=2"`

Vain osan testeistä saa ajettua esimerkiksi näin: `python3 manage.py test -p=test_forms.py -v=2"`

Tietyn appin testit saa ajettua näin: `python3 manage.py test prodekoorg.app_kulukorvaus.tests -v=2`

Testien kirjoittamiseen voi katsoa mallia prodekoorg/app_kulukorvaus/tests/ kansiosta.

### Koodityyli

**Code compliance (PEP8)**

Konfiguraatiotiedosto [.pylintrc](./.pylintrc).

Aja pylint:

```shell
$ pylint --load-plugins pylint_django prodekoorg/
```

**Code formatting**

Konfiguraatiotiedosto [pyproject.toml](./pyproject.toml).

Aja black:

```shell
$ black .

All done! ✨ 🍰 ✨
48 files left unchanged.
```

### Rakennuspalikat

- [Django](https://reactjs.org/) - Web development framework
- [Django CMS](https://www.django-cms.org/en/) - Sisällönhallintajärjestelmä Djangolle
  - [djangocms-bootstrap4](https://github.com/divio/djangocms-bootstrap4) - Bootstrap4 elementtien lisäys suoraan CMS:stä

### Rakenne

    .
    ├── abisivut                       # abit.prodeko.org
    │   └── ...
    ├── alumnirekisteri                # martrikkeli.prodeko.org
    │   └── ...
    ├── auth_prodeko                   # Autentikaatio
    │   └── ...
    ├── documentation                  # Dokumentaatio
    │   └── ...
    ├── lifelonglearning               # lifelonglearning.prodeko.org
    │   └── ...
    ├── locale                         # Käännökset
    │   └── ...
    ├── prodekoorg                     # Projektin pääkansio
    │   │── app_apply_for_membership   # Jäseneksi liittyminen -lomake
    │   │   └── ...
    │   │── app_infoscreen             # REST api infoscreenille
    │   │   └── ...
    │   │── app_kulukorvaus            # Sähköinen kulukorvauslomake
    │   │   └── ...
    │   │── app_poytakirjat            # Pöytäkirjojen automaattinen haku G Suiten Drivestä ja lisäys DjangoCMS:ään
    │   │   └── ...
    │   │── app_tiedostot              # Prodekon brändiin liittyviä tiedostoja
    │   │   └── ...
    │   │── app_toimarit               # .csv toimarilistan uploadaus muodostaa automaattisesti templaten jossa on listattuna prodekon toimarit kuvineen
    │   │   └── ...
    │   │── app_vaalit                 # Vaaliplatform
    │   │   └── ...
    │   │── collected-static           # `python3 manage.py collectstatic` kerää tiedostot tänne
    │   │   └── ...
    │   │── media                      # Django CMS kautta lähetetyt tiedostot kerääntyvät tänne
    │   │   └── ...
    │   │── static                     # Staattiset tiedostot
    │   │   ├── fonts
    │   │   ├── images
    │   │   ├── js
    │   │   ├── misc                   # site.webmanifest
    │   │   └── scss                   # Bootstrap4 scss, muut scss tiedostot
    │   │──templates                   # Suurin osa .html tiedostoista - appeilla (app_kulukorvaus jne.)
    │   │   │                          # on omat templatensa ja staattiset tiedostonsa (js, scss, kuvat)
    │   │   └── ...
    │   └── ...
    ├── seminaari                      # Prodeko Seminaarin nettisivut
    │   └── ...
    ├── tiedotteet                     # tiedotteet.prodeko.org verkkosivu
    │   └── ...
    ├── README.md                      # README
    └── ...

### Kääntäminen eri kielille

1. importtaa ugettext*lazy: `from django.utils.translation import ugettext_lazy as *`. Käytä koodissa näin: \_("First name")
2. `python3 manage.py makemessages -l fi`. locale/ kansioon .po tiedostoon muodostuu käännettävä sana, esimerkin tapauksessa "First name".
3. Käännä suomeksi .po tiedostossa ja aja `python3 manage.py compilemessages`.

.po tiedosto näyttää tältä:

```
#: prodekoorg/app_apply_for_membership/models.py:37
msgid "First name"
msgstr "Etunimi"
```

### Jos scss ei meinaa toimia

Scss:n pitäisi automaattisesti compilata silloin kun tiedosto tallennetaan ja sen aikaleima muuttuu. Tämä ei aina toimi. Workaround: poista tidostosta esim. yksi '{', jotta se on epäpätevä -> muodostuu error, jonka jälkeen compilaus toimii kun '{' lisätään takaisin.

### Kehittäjät

- Timo Riski
- Santeri Kivinen
- Niko Kinnunen
- Kalle Hiltunen
- Leo Drosdek
