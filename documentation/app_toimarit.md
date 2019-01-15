# app_toimarit :feelsgood::godmode::finnadie::trollface:

**P�ivitetty:** 26.12.2018
**Tekij�:** Kalle Hiltunen

## Asennus
- Luo uusi sivu djangon admini-paneelissa
- Mene sivun lis�asetuksiin
- Valitse sovellukseksi (Application) joko Officials (toimarit) tai Board (hallituslaiset). T�m� m��ritt�� n�ytett�v�n sis�ll�n sivulla.
- Kohtaan application instance name voi valita k�yt�nn�ss� mit� tahansa, mutta toimari- ja hallitussivuilla on oltava eri arvo. Esimerkiksi arvot voivat olla app_toimarit_officials ja app_toimarit_board.
- Julkaise sivu

## Toimarien lis��minen

- Jaostot on lis�tt�v� ensin manuaalisesti admin-paneelin kautta, mik�li niit� ei ole jo luotu
- CSV-tiedoston voi ladata admin --> Guild Officials/Toimihenkil�t --> Lataa CSV
- Vanhat toimarit eiv�t poistu CSV-tiedostoa ladatessa, joten tarvittaessa ne tulee poistaa ennen tiedoston lataamista
- Toimarien kuvat linkittyv�t automaattisesti oikeisiin henkil�ihin, kun ne ladataan kansioon prodekoorg/app_toimarit/static/images/toimari_photos
- Kuvien nime�misen tulee noudattaa muotoa Etunimi_Sukunimi.jpg 
- Oletuskuvaa voi vaihtaa samasta kansiosta tiedostosta anonyymi_uniseksi_maskulinoitu.jpg

## Hallituksen j�senten lis��minen

- Manuaalisesti admin-paneelin kautta
- Toimarien kuvat linkittyv�t automaattisesti oikeisiin henkil�ihin, kun ne ladataan kansioon prodekoorg/app_toimarit/static/images/hallitus_photos
- Kuvien nime�misen tulee noudattaa muotoa Etunimi_Sukunimi.jpg 
- Oletuskuvaa voi vaihtaa samasta kansiosta tiedostosta placeholder.jpg

## Muut toiminnallisuudet

- Admin-paneelista kaikki toimarit voi ladata omalle koneelle CSV-tiedostona valitsemalla kaikki toimarit ja valitsemalla "Export selected as CSV" vasemmasta yl�kulmasta.