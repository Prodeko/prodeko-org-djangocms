# Alumnirekisteri :person_with_blond_hair::older_man::construction_worker:

[Rekisteriseloste](rekister/static/Rekisteriseloste.pdf).

### Ohjeita projektin ajamiseen lokaalisti:

```
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ python manage.py shell
>>> from rekisteri.initialise import *
>>> create_admin_profile()
```

`vagrant destroy` tuhoaa nykyisen ympäristön, jonka jälkeen yllä olevat komennot voi ajaa uudestaan jos jokin meni pieleen.

Kirjaudu sisään matrikkeliin käyttäjällä admin@admin.fi / salasana.
