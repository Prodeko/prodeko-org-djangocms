# app_toimarit Documentation

**Päivitetty:** 26.12.2018
**Tekijä:** Kalle Hiltunen

## Asennus
- Luo uusi sivu djangon admini-paneelissa
- Mene sivun lisäasetuksiin
- Valitse sovellukseksi (Application) joko Officials (toimarit) tai Board (hallituslaiset). Tämä määrittää näytettävän sisällön sivulla.
- Kohtaan application instance name voi valita käytännössä mitä tahansa, mutta toimari- ja hallitussivuilla on oltava eri arvo. Esimerkiksi arvot voivat olla app_toimarit_officials ja app_toimarit_board.
- Julkaise sivu

## Toimarien lisääminen

- Jaostot on lisättävä ensin manuaalisesti admin-paneelin kautta, mikäli niitä ei ole jo luotu
- CSV-tiedoston voi ladata admin --> Guild Officials/Toimihenkilöt --> Lataa CSV
- Vanhat toimarit eivät poistu CSV-tiedostoa ladatessa, joten tarvittaessa ne tulee poistaa ennen tiedoston lataamista
- Toimarien kuvat linkittyvät automaattisesti oikeisiin henkilöihin, kun ne ladataan kansioon prodekoorg/app_toimarit/static/images/toimari_photos
- Kuvien nimeämisen tulee noudattaa muotoa Etunimi_Sukunimi.jpg 
- Oletuskuvaa voi vaihtaa samasta kansiosta tiedostosta anonyymi_uniseksi_maskulinoitu.jpg

## Hallituksen jäsenten lisääminen

- Manuaalisesti admin-paneelin kautta
- Toimarien kuvat linkittyvät automaattisesti oikeisiin henkilöihin, kun ne ladataan kansioon prodekoorg/app_toimarit/static/images/hallitus_photos
- Kuvien nimeämisen tulee noudattaa muotoa Etunimi_Sukunimi.jpg 
- Oletuskuvaa voi vaihtaa samasta kansiosta tiedostosta placeholder.jpg

## Muut toiminnallisuudet

- Admin-paneelista kaikki toimarit voi ladata omalle koneelle CSV-tiedostona valitsemalla kaikki toimarit ja valitsemalla "Export selected as CSV" vasemmasta yläkulmasta.