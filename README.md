# Prodeko.org :tv::rainbow:

Tuotantotalouden kilta Prodekon Django CMS -pohjaiset nettisivut.

---

Prodeko.org projekti käyttää Django versiota 2.2.10.

### Vaatimukset

#### Docker

1. Lataa [docker](https://docs.docker.com/install/)
2. Kopioi prodekoorg/settings/variables.sample.txt ja nimeä se variables.txt nimiseksi
3. Täytä variables.txt tiedostoon puuttuvat muuttujat

```
$ docker-compose up  # Kehitysympäristön käynnistys
```

Asenna lisäksi eslint, prettier, stylelint, pylint, jinjalint ja black ajamalla seuraavat komennot:

```
$ npm install
$ python3 -m venv venv
$ pip3 install -r requirements-dev.txt
```

### Kehittäminen

Kehitysympäristön käynnistys luo uuden Django käyttäjän:

- Käyttäjä: **webbitiimi@prodeko.org**
- Salasana: **kananugetti**

### Uuden appin luonti

Esimerkiksi app_kiltiskamera luotiin seuraavasti:

```
mkdir prodekoorg/app_kiltiskamera
python3 manage.py startapp app_kiltiskamera prodekoorg/app_kiltiskamera
```

Myös abisivut, auth_prodeko, seminaari ja tiedotteet ovat omia appejaan, vaikka ne eivät ole prodekoorg kansion sisällä.

### Deployas palvelimelle

Azuressa hostataan media ja static tiedostot. Lisäksi käytössä on Azuren CDN.

1. Virtualenv päälle `source venv/bin/activate`
2. Aja `bash deploy.sh` projektin juuressa
3. Käynnistä apache uudestaan `sudo service apache2 restart`
4. Tarkista näyttävätkö sivut toimivan oikein [prodeko.org](https://prodeko.org)

Jos törmäät "ImportError: Couldn't import Django..." erroriin, vaihda käyttäjä roottiin (`sudo su`) ja tee kohdat 2. ja 3. uudestaan.

### Testaus

- Testit saa ajettua komennolla `python3 manage.py test -v=2"`
- Vain osan testeistä saa ajettua esimerkiksi näin: `python3 manage.py test -p=test_forms.py -v=2"`
- Tietyn appin testit saa ajettua näin: `python3 manage.py test prodekoorg.app_kulukorvaus.tests -v=2 --keepdb --parallel` (--keepdb säilyttää tietokannan testiajojen välissä)
- Testien kirjoittamiseen voi katsoa mallia prodekoorg/app_kulukorvaus/tests/ kansiosta

### Koodityyli

Käytössä seuraavat työkalut:

- python: pylint + black
- html: jinjalint
- javascript: eslint + prettier
- css: stylelint + prettier

#### Python

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

#### HTML

HTML-templatejen linttaamiseen käytetään [Jinjalint](https://github.com/motet-a/jinjalint)

Aja jinjalint:

```shell
$ jinjalint prodekoorg/templates
```

#### Javascript & CSS

Muista asentaa tarvittavat packaget komennolla `npm i`.

**Javascript**

Konfiguraatiotiedosto [.eslintrc.js](./.eslintrc.js). Lisäksi käytössä on Prettier-integraatio [.prettierrc](./..prettierrc).

```shell
$ npm run lint:eslint      # Näytä virheet
$ npm run lint:eslint-fix  # Korjaa virheet
```

**CSS**

Konfiguraatiotiedosto [.stylelintrc](./.stylelintrc). Lisäksi käytössä on Prettier-integraatio [.prettierrc](./..prettierrc).

```shell
$ npm run lint:css      # Näytä virheet
$ npm run lint:css-fix  # Korjaa virheet
```

### Rakennuspalikat

- [Django](https://www.djangoproject.com/) - Web development framework
- [React](https://reactjs.org/) - Web development framework
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
    │   │── app_contact                # Yhteydenottolomake
    │   │   └── ...
    │   │── app_infoscreen             # REST api infoscreenille
    │   │   └── ...
    │   │── app_kiltiskamera           # Kiltiskamera
    │   │   └── ...
    │   │── app_kulukorvaus            # Sähköinen kulukorvauslomake
    │   │   └── ...
    │   │── app_membership             # Jäseneksi liittyminen -lomake
    │   │   └── ...
    │   │── app_poytakirjat            # Pöytäkirjojen automaattinen haku G Suiten Drivestä ja lisäys DjangoCMS:ään
    │   │   └── ...
    │   │── app_tiedostot              # Prodekon brändiin liittyviä tiedostoja
    │   │   └── ...
    │   │── app_toimarit               # Mahdollistaa vuoden toimihenkilöiden päivittämisen sivuille .csv-tiedoston avulla
    │   │   └── ...
    │   │── app_utils                  # Kolmannen osapuolen appien poistaminen administa, signaalit mediatiedostojen poistoon
    │   │   └── ...
    │   │── app_vaalit                 # Vaaliplatform
    │   │   └── ...
    │   │── collected-static           # Kerätyt staattiset tiedostot dev-asetuksilla. Komento `python3 manage.py collectstatic` kerää tiedostot tänne
    │   │   └── ...
    │   │── media                      # Palvelimelle lähetetyt tiedostot kerääntyvät tänne dev-asetuksilla
    │   │   └── ...
    │   │── settings                   # Django globaalit asetukset
    │   │   ├── base.py
    │   │   ├── dev.py
    │   │   ├── prod.py
    │   │── static                     # Staattiset tiedostot
    │   │   ├── fonts
    │   │   ├── images
    │   │   ├── js
    │   │   ├── misc
    │   │   └── scss                   # Bootstrap4 scss, muut scss tiedostot
    │   │──templates                   # Suurin osa html-tiedostoista. Sovelluksilla (app_kulukorvaus jne.)
    │   │   │                          # on omat templatensa ja staattiset tiedostonsa (js, scss, kuvat)
    │   │   └── ...
    │   └── ...
    ├── scripts                        # Python skriptejä
    │   └── ...
    ├── seminaari                      # seminaari.prodeko.org
    │   └── ...
    ├── tiedotteet                     # tiedotteet.prodeko.org
    │   │── backend                    # Tiedotteet django backend
    │   │   └── ...
    │   │── frontend                   # Tiedotteet React frontend
    │   │   └── ...
    ├── README.md                      # README
    └── ...

### Kääntäminen eri kielille

1. importtaa ugettext_lazy: `from django.utils.translation import ugettext_lazy as *`. Käytä koodissa näin: \_("First name")
2. `python3 manage.py makemessages -l fi -i "node_modules/*" -i "venv/*"`. locale/ kansioon .po tiedostoon muodostuu käännettävä sana, esimerkin tapauksessa "First name".
3. Käännä suomeksi .po tiedostossa ja aja `python3 manage.py compilemessages -l fi -i "node_modules/*" -i "venv/*"`.
4. (Valinnainen) Javascript tiedostojen sisältämät käännöset saa muodostettua seuraavalla komennolla: `python3 manage.py makemessages -d djangojs -l fi -i tiedotteet -i "node_modules/*" -i "venv/*"`

.po tiedosto näyttää tältä:

```
#: prodekoorg/app_membership/models.py:37
msgid "First name"
msgstr "Etunimi"
```

### Jos scss ei meinaa toimia

Scss:n pitäisi automaattisesti compilata silloin kun tiedosto tallennetaan ja sen aikaleima muuttuu. Tämä ei aina toimi. Workaround: poista tiedostosta esim. yksi '{', jotta se on epäpätevä -> muodostuu error, jonka jälkeen kääntäminen toimii kun '{' lisätään takaisin.

### Kehittäjät

- Timo Riski
- Santeri Kivinen
- Niko Kinnunen
- Kalle Hiltunen
- Leo Drosdek
