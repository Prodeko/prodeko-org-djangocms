# Analytiikasta :bar_chart::chart_with_upwards_trend:

- **Päivitetty** 18.1.2019
- **Tekijä:** Timo Riski

Sivustolle on konfiguroitu [Google Analytics](https://analytics.google.com) ja [Google Tag Managerin](https://tagmanager.google.com) jotta voidaan seurata kuinka sivustoa käytetään.

## Setup

1. Luo uusi Google Analytics tili

<img src="images/analytics/ga-account-1.png" style="display: block;" width="500" alt="Luo uusi Google Analytics tili kuva 1" />
<img src="images/analytics/ga-account-2.png" style="display: block;" width="500" alt="Luo uusi Google Analytics tili kuva 2" />
<img src="images/analytics/ga-account-3.png" style="display: block;" width="500" alt="Luo uusi Google Analytics tili kuva 3" />

2. Luo uusi Google Tag Manager tili

<img src="images/analytics/gtm-account-1.png" style="display: block;" width="500" alt="Luo uusi Google Tag Manager tili kuva 1" />
<img src="images/analytics/gtm-account-2.png" style="display: block;" width="500" alt="Luo uusi Google Tag Manager tili kuva 2" />
<img src="images/analytics/gtm-account-3.png" style="display: block;" width="500" alt="Luo uusi Google Tag Manager tili kuva 3" />

3. Lisää `<body>` ja `<head>` elementteihin GTM

`<head>` elementin alkuun:

```html
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WV66B47');
  </script>
  <!-- End Google Tag Manager -->
```

`<body>` elementin alkuun:

```html
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WV66B47" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
```

4. Määritä tarvittavat tägit, triggerit ja muuttujat Google Tag Manageriin.

- Lisätietoja GTM toiminnasta on luettavissa [täältä](https://support.google.com/tagmanager/answer/6102821?hl=fi).

<img src="images/analytics/gtm-tags.png" style="display: block;" width="700" alt="GTM tägit" />

*Tägit*

<img src="images/analytics/gtm-triggers.png" style="display: block;" width="700" alt="GTM triggerit" />

*Triggerit*

<img src="images/analytics/gtm-triggers.png" style="display: block;" width="700" alt="GTM muuttujat" />

*Muuttujat*

5. Tämän jälkeen Google Analytics toimii!

<img src="images/analytics/ga.png" style="display: block;" width="700" alt="GA toimii!" />

## Mitä kaikkea voi seurata?

GTM:n kautta voi asentaa monenlaisia tagejä: sivuston katselukerrat, kuvan/linkin klikkaus, lomakkeen lähetys etc.

### Sivun näyttökertojen seuranta

Sivun näyttökertojen seurannan konfigurointi on helppoa. Tarvitaan ainoastaan yksi muuttuja, triggeri ja tägi.

- Muuttuja **Google Analytics** joka yhdistää Google Analyticsin ja Google Tag Managerin.
<img src="images/analytics/gtm-google-analytics-variable.png" style="display: block;" width="700" alt="Google Analytics muuttuja" />

- Määritettiin tag 'GA - Sivujen näyttökerrat' ('All pages' triggeri on valmiiksi määritetty)
<img src="images/analytics/gtm-pageviews.png" style="display: block;" width="700" alt="Google Analytics sivujen näyttökerrat" />

## Lomakkeen lähetyksen seuranta

Appien app_kulukorvaus ja app_apply_for_membership lomakkeet lähtevät AJAX requesteinä palvelimelle, eikä GTM:n normaali 'Lomakkeen lähetys' trigger toimi niiden kanssa.

<img src="images/analytics/gtm-trigger-formsubmission.png" style="display: block;" width="700" alt="Lomakkeen lähetys' trigger ei toimi" />

[Näiden ohjeiden](https://www.clickinsight.ca/blog/tracking-form-submissions-gtm) avulla määritettiin uudet custom eventit `formSubmitted` ja `formError` sekä uusi dataLayer muuttuja `formName` Google Tag Manageriin.

Tämän jälkeen määritettiin tarvittavat tägit. Kokonaisuudessaan setup näyttää tältä:

<img src="images/analytics/gtm-form-success-tag.png" style="display: block;" width="700" alt="GTM tägit" />
<img src="images/analytics/gtm-form-error-tag.png" style="display: block;" width="700" alt="GTM tägit" />

*Tägit*

<img src="images/analytics/gtm-form-success-trigger.png" style="display: block;" width="700" alt="GTM triggerit" />
<img src="images/analytics/gtm-form-error-trigger.png" style="display: block;" width="700" alt="GTM triggerit" />

*Triggerit*

<img src="images/analytics/gtm-datalayer-variable.png" style="display: block;" width="700" alt="GTM muuttujat" />

*Muuttujat*

Tämän lisäksi CSRF-validointia varten täytyy päivittää settings.py muuttuja `CSRF_TRUSTED_ORIGINS = '.google.com'`. Tämä johtuu siitä, että analytiikan tallentamiseksi lähtee GET-pyyntö Googlen palvelimelle, jolloin CSRF-token vanhenee.

Nyt javascriptillä voi lähettää dataLayeriin custom tapahtumia (esim. prodekoorg/app_kulukorvaus/static/js/kulukorvaus-custom.js):

<img src="images/analytics/gtm-datalayer-javascript.png" style="display: block;" width="500" alt="GTM tapahtumien lähetys javascriptillä" />

## Muuta

Google Analyticsiin on configuroitu linkitys Prodekon Google Ads accountin kanssa.

![Google Analytics & Google Ads linkitys](images/analytics/google-ads-linkitys.png)
