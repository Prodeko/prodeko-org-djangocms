# Prodeko.org :tv::rainbow:

Tuotantotalouden kilta Prodekon Django CMS -pohjaiset nettisivut.

---

Prodeko.org projekti käyttää Django versiota 3.1.4

### Vaatimukset

#### Docker

1. Lataa [docker](https://docs.docker.com/install/)
2. Kopioi prodekoorg/settings/variables.sample.txt ja nimeä se variables.txt nimiseksi.
3. Täytä variables.txt tiedostoon puuttuvat muuttujat (kehitysympäristössä ei tarvitse)

Kehitysympäristöä varten tarvitset kirjastot `postgresql-devel` ja `uv`, jotka voi asentaa Ubuntulla (Debianilla) ja WSL:lla komennolla

```shell
$ sudo apt install libpq-dev
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Asenna lisäksi eslint, prettier, stylelint, pylint, jinjalint ja black ajamalla seuraavat komennot:

```shell
$ npm install
$ uv venv --python 3.12
$ uv sync
$ source .venv/bin/activate
```

Valinnainen: asenna git-hookit komennolla `uvx pre-commit install`, jolloin ruff ajetaan automaattisesti ennen committia.

Windowsilla on suositeltavaa ajaa nämä WSL:n sisällä.

### Kehittäminen

Aja docker-kontti ylös seuraavalla komennolla:

```shell
$ docker-compose up  # Kehitysympäristön käynnistys
```

Windowsilla on suositeltavaa ajaa tämä WSL:n sisällä.

Voit nyt siirtyä selaimellasi osoitteeseen <http://localhost:8000>.
Kehitysympäristön käynnistys luo sivustolle uuden Django-käyttäjän:

- Käyttäjä: **webbitiimi@prodeko.org**
- Salasana: **kananugetti**

### Uuden appin luonti

Esimerkiksi app_kiltiskamera luotiin seuraavasti:

```shell
mkdir prodekoorg/app_kiltiskamera
uv run  manage.py startapp app_kiltiskamera prodekoorg/app_kiltiskamera
```

Myös abisivut, auth_prodeko, seminaari ja tiedotteet ovat omia appejaan, vaikka ne eivät ole prodekoorg kansion sisällä.

### Deployaus palvelimelle

## Azure

Kun masteriin pusketaan tai mergetään tavaraan repoon määritetty Github Actions pipeline aktivoituu. Pipeline buildaa ja puskee automaattisesti kontin Azure Container Registryyn sekä deployaa kontin palvelimelle [infrastructure repon](https://github.com/Prodeko/infrastructure/tree/master/ansible) playbookin avulla.

Mikäli deployaus halutaan suorittaa manuaalisesti, onnistuu se seuraavilla komennoilla:

1. Kirjaudu Prodekon docker registryyn: `az acr login --name prodekoregistry`
2. Buildaa image: `docker build . -t prodekoregistry.azurecr.io/prodeko-org/prodeko-org`
3. Puske image registryyn: `docker push prodekoregistry.azurecr.io/prodeko-org/prodeko-org`
4. Aja infrastructure reposta: `ansible-playbook playbook.yml --extra-vars '@passwd.yml' --tags prodeko_org`

### Testaus

Windowsilla on suositeltavaa ajaa kaikki tämänkin osion komennot WSL:n sisällä.

- Käynnistä projekti komennolla `docker-compose up`
- Avaa uusi terminal window
- Testit saa ajettua komennolla `docker exec prodeko_org uv run pytest prodekoorg/`
- Testien kattavuus ja rinnakkaisajo `docker exec prodeko_org uv run pytest --cov -n auto prodekoorg/`
- **Tietyn appin testit saa ajettua näin: `docker exec prodeko_org uv run pytest prodekoorg/app_toimarit`**

### Koodityyli

Käytössä seuraavat työkalut:

- python: pylint + black
- html: curlylint
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

HTML-templatejen linttaamiseen käytetään [Curlylint](https://github.com/thibaudcolas/curlylint)

Aja jinjalint:

```shell
$ curlylint prodekoorg
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
    │   │── app_membership             # Jäseneksi liittyminen -lomake
    │   │   └── ...
    │   │── app_poytakirjat            # Pöytäkirjojen automaattinen haku G Suiten Drivestä ja lisäys DjangoCMS:ään
    │   │   └── ...
    │   │── app_proleko                # proleko.prodeko.org
    │   │   └── ...
    │   │── app_tiedostot              # Prodekon brändiin liittyviä tiedostoja
    │   │   └── ...
    │   │── app_toimarit               # Mahdollistaa vuoden toimihenkilöiden päivittämisen sivuille .csv-tiedoston avulla
    │   │   └── ...
    │   │── app_utils                  # Kolmannen osapuolen appien poistaminen administa, signaalit mediatiedostojen poistoon
    │   │   └── ...
    │   │── app_vaalit                 # Vaaliplatform
    │   │   └── ...
    │   │── collected-static           # Kerätyt staattiset tiedostot dev-asetuksilla. Komento `uv run manage.py collectstatic` kerää tiedostot tänne
    │   │   └── ...
    │   │── media                      # Palvelimelle lähetetyt tiedostot kerääntyvät tänne dev-asetuksilla
    │   │   └── ...
    │   │── settings                   # Django globaalit asetukset
    │   │   ├── base.py
    │   │   ├── dev.py
    │   │   └── prod.py
    │   │── static                     # Staattiset tiedostot
    │   │   ├── fonts
    │   │   ├── images
    │   │   ├── js
    │   │   ├── misc
    │   │   └── scss                   # Bootstrap4 scss, muut scss tiedostot
    │   │──templates                   # Suurin osa html-tiedostoista. Sovelluksilla (app_toimarit jne.)
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

1. importtaa gettext_lazy: `from django.utils.translation import gettext_lazy as *`. Käytä koodissa näin: \_("First name")
2. `uv run manage.py makemessages -l fi -i "node_modules/*" -i "venv/*"`. locale/ kansioon .po tiedostoon muodostuu käännettävä sana, esimerkin tapauksessa "First name".
3. Käännä suomeksi .po tiedostossa ja aja `uv run manage.py compilemessages -l fi -i "node_modules/*" -i "venv/*"`.
4. (Valinnainen) Javascript tiedostojen sisältämät käännöset saa muodostettua seuraavalla komennolla: `uv run manage.py makemessages -d djangojs -l fi -i tiedotteet -i "node_modules/*" -i "venv/*"`

.po tiedosto näyttää tältä:

```
#: prodekoorg/app_membership/models.py:37
msgid "First name"
msgstr "Etunimi"
```

### Jos scss ei meinaa toimia

Scss:n pitäisi automaattisesti compilata silloin kun tiedosto tallennetaan ja sen aikaleima muuttuu. Tämä ei aina toimi. Workaround: poista tiedostosta esim. yksi '{', jotta se on epäpätevä -> muodostuu error, jonka jälkeen kääntäminen toimii kun '{' lisätään takaisin.

Windows-käyttäjä: käynnistä docker-kontti WSL:n sisällä.

### Kehittäjät

- Timo Riski
- Santeri Kivinen
- Niko Kinnunen
- Kalle Hiltunen
- Leo Drosdek
