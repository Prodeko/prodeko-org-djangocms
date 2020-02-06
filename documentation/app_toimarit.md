# app_toimarit :feelsgood::godmode::finnadie::trollface:

**Päivitetty:** 6.2.2020
**Tekijä:** Kalle Hiltunen, Timo Riski

## Asennus

- Luo uusi sivu djangon admini-paneelissa
- Mene sivun lisäasetuksiin
- Sivuja on neljää eri laatua: sivut vanhoille ja nykyisille toimareille ja sivut vanhoille ja uudelle hallitukselle. Sivun tyypin saat valittua valitsemalla lisäasetuksista sovellus valikosta haluamasi sivutyypin.
- Julkaise sivu

## Toimarien lisääminen

- CSV-tiedoston voi ladata admin --> Guild Officials/Toimihenkilöt --> Lataa CSV
- Tiedoston tulee olla muotoa etunimi;sukunimi;virka;jaosto;vuosi. Jos toimari täysin samoilla arvoilla on jo luotu, duplikaattia ei luoda.
- Toimarien kuvat linkittyvät automaattisesti oikeisiin henkilöihin, kun ne ladataan filerin kansioon Kuvat/Toimihenkilöt/[Vuosi]/Etunimi_Sukunimi.jpg.
- Huom! Kuvien nimessä ei saa olla ä tai ö kirjainta.
- Kuvan alkuperäisen tiedostonimen tulee noudattaa muotoa Etunimi_Sukunimi.[jpg|png|jpeg]
- Nykyisten toimarien oletuskuvana käytetään tiedostoa anonymous_prodeko.[jpg|png|jpeg], sen tulee löytyä filerista kansiosta Kuvat/

## Hallituksen jäsenten lisääminen

- CSV-tiedoston voi ladata admin --> Board members/Hallituksen jäsenet --> Lataa CSV
- Tiedoston tulee olla muotoa etunimi;sukunimi;virka suomeksi;virka englanniksi;vuosi;(mobilephone);(email);(telegram). Suluissa olevat kohdat ovat vapaavalintaisia, ne voi halutessaan jättää tyhjäksi. Jos hallituslainen täysin samoilla arvoilla on jo luotu, duplikaattia ei luoda.
- Hallituslaisten kuvat linkittyvät automaattisesti oikeisiin henkilöihin, kun ne ladataan filerin kansioon Kuvat/Hallitukset/[Vuosi]/Etunimi_Sukunimi.jpg.
- Huom! Kuvan nimessä ei saa olla ä tai ö kirjainta.
- Kuvan alkuperäisen tiedostonimen tulee noudattaa muotoa Etunimi_Sukunimi.[jpg|png|jpeg]
- Nykyisten toimarien oletuskuvana käytetään tiedostoa anonymous_prodeko.[jpg|png|jpeg], sen tulee löytyä filerista kansiosta Kuvat/

## Muut toiminnallisuudet

- Admin-paneelista kaikki toimarit/hallituslaiset voi ladata omalle koneelle CSV-tiedostona valitsemalla kaikki toimarit/hallituslaiset ja valitsemalla "Export selected as CSV" vasemmasta yläkulmasta.
