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

- Käyttäjä: **webbitiimi@prodeko.rog**
- Salasana: **kananugetti**
