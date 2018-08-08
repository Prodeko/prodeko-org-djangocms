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
$ vagrant up    # Virtuaalikoneen käynnistys (Vagrantfile & bootstrap.sh)
$ vagrant ssh   # SSH yhteys virtuaalikoneeseen
$ cd /vagrant   # Jaettu kansio
$ ls
```

### Kehittäminen

Komento `vagrant up` käynnistää lokaalin serverin osoitteeseen localhost:9000 (sama kuin 127.0.0.1:9000). Lisäksi bootstrap.sh luo automaattisesti Django superuserin kirjautumista varten.

Jos vagrantin sisällä oleva serveri pysähtyy jostain syystä, sen saa uudestaan päälle esimerkiksi seuraavilla komennoilla

```
$ vagrant ssh
$ python3 manage.py runserver 0.0.0.0:8000
```

- Käyttäjä: **webbitiimi@prodeko.org**
- Salasana: **kananugetti**


### Käyttöönotto

1. Virtualenv päälle `source venv/bin/activate`
2. Collectaa staattiset tiedostot `python3 manage.py collectstatic`
3. Käynnistä apache uudestaan `sudo service apache2 restart`

Jos törmäät "ImportError: Couldn't import Django..." erroriin, vaihda käyttäjä roottiin ja tee kohdat 2. ja 3. uudestaan.

## Rakennuspalikat

* [Django](https://reactjs.org/) - Web development framework
* [Django CMS](https://www.django-cms.org/en/) - Sisällönhallintajärjestelmä Djangolle
  * [djangocms-bootstrap4](https://github.com/divio/djangocms-bootstrap4) - Bootstrap4 elementtien lisäys suoraan CMS:stä

## Rakenne
    .
    ├── ...
    ├── auth_prodeko          # Autentikaatio
    │   └── ...  
    ├── prodekoorg            # Projektin pääkansio
    │   │── app_kulukorvaus   # Sähköinen kulukorvauslomake
    │   │   └── ...  
    │   │── app_poytakirjat   # Pöytäkirjojen automaattinen haku G Suiten Drivestä, enkryptointi ja
    │   │   └── ...  
    │   │── app_tiedostot     # Prodekon brändiin liittyviä tiedostoja
    │   │   └── ...  
    │   │── app_toimarit      # .csv toimarilistan uploadaus muodostaa automaattisesti templaten jossa on listattuna prodekon toimarit kuvineen
    │   │   └── ...  
    │   │── app_vaalit        # Vaaliplatform
    │   │   └── ...  
    │   │── media             # Django CMS kautta lähetetyt tiedostot kerääntyvät tänne
    │   │   └── ...  
    │   │── collected-static  # `python3 manage.py collectstatic` kerää tiedostot tänne
    │   │   └── ...  
    │   │── static            # Staattiset assetit
    │   │   ├── css
    │   │   ├── fonts
    │   │   ├── images
    │   │   └── js
    │   │──templates          # Suurin osa .html tiedostoista - appeilla (app_kulukorvaus jne.) on omat templatensa
    │   │   └── ...  
    │   └── ...  
    ├── tiedotteet            # tiedotteet.prodeko.org verkkosivu
    │   └── ...  
    ├── README.md             # README
    ├── bootstrap.sh.md       # Vagrant konfiguraatio, jonka komennot käydään läpi `vagrant up` komennon seurauksesta
    └── ...

## Kehittäjät

* Timo Riski
* Santeri Kivinen
* Niko Kinnunen
* Kalle Hiltunen
* Leo Drosdek
