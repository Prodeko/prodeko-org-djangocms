# Prodeko.org :tv::rainbow:

Tuotantotalouden kilta Prodekon Django pohjaiset nettisivut.

---

 Prodeko.org projekti käyttää Django versiota 1.11.11, sillä DjangoCMS ei ole vielä yhteensopiva version 2.0 kanssa.

### Vaatimukset

Yhtenäisen kehitysympäristöön käytämme Virtualboxia ja vagranttia. Virtuaalikoneen versio on Ubuntu 16.04.4 LTS (Xenial Xerus).

Lataa vagrant ja virtualbox:
- [vagrant](https://www.vagrantup.com/downloads.html)
- [virtualbox](https://www.virtualbox.org/wiki/Downloads)

### Vagrantin käyttö
```
$ vagrant up         # Virtuaalikoneen käynnistys (Vagrantfile & bootstrap.sh)
$ vagrant provision  # Ajaa bootstrap.sh tiedoston komennot virtuaalikoneen sisällä.
$ vagrant ssh        # SSH yhteys virtuaalikoneeseen
$ cd /vagrant        # Jaettu kansio
```

### Kehittäminen

Komento `vagrant up` käynnistää lokaalin serverin osoitteeseen localhost:9000 (sama kuin 127.0.0.1:9000). Lisäksi bootstrap.sh luo automaattisesti Django superuserin kirjautumista varten. Komento `vagrant provision` ajaa bootstrap.sh tiedoston komennot. 

Jos vagrantin sisällä oleva serveri pysähtyy jostain syystä, sen saa uudestaan päälle esimerkiksi seuraavilla komennoilla

```
$ vagrant ssh
$ python3 manage.py runserver 0.0.0.0:8000
```

- Käyttäjä: **webbitiimi@prodeko.org**
- Salasana: **kananugetti**

### Deployas palvelimelle

1. Virtualenv päälle `source venv/bin/activate`
2. Collectaa staattiset tiedostot `python3 manage.py collectstatic`
3. Käynnistä apache uudestaan `sudo service apache2 restart`
4. Tarkista näyttävätkö sivut toimivan [djangocms.prodeko.org](https://djangocms.prodeko.org)

Jos törmäät "ImportError: Couldn't import Django..." erroriin, vaihda käyttäjä roottiin ja tee kohdat 2. ja 3. uudestaan.

### Testaus

Testit saa ajettua komennolla `python3 manage.py test -v=2"`

Vain osan testeistä saa ajettua esimerkiksi näin: `python3 manage.py test -p=test_forms.py -v=2"`

Testien kirjoittamiseen voi katsoa mallia prodekoorg/app_kulukorvaus/tests/ kansiosta.

### Rakennuspalikat

* [Django](https://reactjs.org/) - Web development framework
* [Django CMS](https://www.django-cms.org/en/) - Sisällönhallintajärjestelmä Djangolle
  * [djangocms-bootstrap4](https://github.com/divio/djangocms-bootstrap4) - Bootstrap4 elementtien lisäys suoraan CMS:stä

### Rakenne
    .
    ├── ...
    ├── auth_prodeko                   # Autentikaatio
    │   └── ...  
    ├── lifelonglearning               # lifelonglearning.prodeko.org
    │   └── ...  
    ├── locale                         # Käännökset
    │   └── ...  
    ├── prodekoorg                     # Projektin pääkansio
    │   │── app_apply_for_membership   # Jäseneksi liittyminen -lomake
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
    │   │   └── scss
    │   │──templates          # Suurin osa .html tiedostoista - appeilla (app_kulukorvaus jne.) on omat templatensa ja staattiset tiedostonsa (js, scss, kuvat)
    │   │   └── ...  
    │   └── ...  
    ├── tiedotteet            # tiedotteet.prodeko.org verkkosivu
    │   └── ...  
    ├── README.md             # README
    ├── bootstrap.sh          # Vagrant konfiguraatio, jonka komennot käydään läpi `vagrant up` komennon seurauksesta
    └── ...

### Printtaaminen konsoliin
- Mikäli haluat printata jotain konsoliin, kommentoi `su - ubuntu -c "cd /vagrant && screen -S server -d -m python3 manage.py runserver 0.0.0.0:8000"` rivi pois bootstrap.sh tiedostosta ja aja `vagrant provision`. Vaihtoehtoisesti tapa runserver prosessi ajamalla virtuaalikoneen sisällä `sudo netstat -plten |grep python` ja `sudo kill $PID` ($PID tilalle laita netstatin kertoma prosessinumero).
- Suomenkielisten käännösten tekeminen onnistuu seuraavasti: 

### Kääntäminen eri kielille
1. importtaa ugettext_lazy: `from django.utils.translation import ugettext_lazy as _`. Käytä koodissa näin: _("First name")
2. `python3 manage.py makemessages -l fi`. locale/ kansioon .po tiedostoon muodostuu käännettävä sana, esimerkin tapauksessa "First name".
3. Käännä suomeksi .po tiedostossa ja aja `python3 manage.py compilemessages`. 

Jos törmäät "CommandError: Can't find msgfmt. Make sure you have GNU gettext tools 0.15 or newer installed." virheeseen, aja sudo `apt-get install gettext` vagrantissa.

.po tiedosto näyttää tältä: 

```
#: prodekoorg/app_apply_for_membership/models.py:37
msgid "First name"
msgstr "Etunimi"
```
### Jos scss ei meinaa toimia
Scss pitäisi compilaa silloin kun tiedosto tallennetaan ja sen aikaleima muuttuu. Tämä ei aina toimi. Workaround: poista tidostosta esim. yksi '{', jotta se on epäpätevä -> muodostuu error, jonka jälkeen compilaus toimii.

### Kehittäjät

* Timo Riski
* Santeri Kivinen
* Niko Kinnunen
* Kalle Hiltunen
* Leo Drosdek
