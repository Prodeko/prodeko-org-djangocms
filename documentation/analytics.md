# Analytiikasta :mailbox_with_mail::email:

- **Päivitetty** 18.1.2019
- **Tekijä:** Timo Riski

Sivustolle on konfiguroitu [Google Analytics](https://analytics.google.com) ja [Google Tag Managerin](https://tagmanager.google.com) jotta voidaan seurata kuinka sivustoa käytetään. 

## Setup

1. Luo uusi Google Analytics tili

![Luo uusi Google Analytics tili kuva 1](images/analytics/ga-account-1.png)
![Luo uusi Google Analytics tili kuva 2](images/analytics/ga-account-2.png)
![Luo uusi Google Analytics tili kuva 3](images/analytics/ga-account-3.png)

2. Luo uusi Google Tag Manager tili

![Luo uusi Google Tag Manager tili kuva 1](images/analytics/gtm-account-1.png)
![Luo uusi Google Tag Manager tili kuva 2](images/analytics/gtm-account-2.png)
![Luo uusi Google Tag Manager tili kuva 3](images/analytics/gtm-account-3.png)

3. Lisää `<body>` ja `<head>` elementteihin GTM

`<head>` elementin alkuun:
```
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
```
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WV66B47" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
```

4. Määritä tarvittavat tägit, triggerit ja muuttujat Google Tag Manageriin. 
- Lisätietoja GTM toiminnasta on luettavissa [täältä](https://support.google.com/tagmanager/answer/6102821?hl=fi).

![GTM tägit](images/analytics/gtm-tags.png)
*Tägit*
![GTM triggerit](images/analytics/gtm-triggers.png)
*Triggerit*
![GTM muuttujat](images/analytics/gtm-variables.png)
*Muuttujat*

5. Tämän jälkeen Google Analytics toimii!
![GA toimii!](images/analytics/ga.png)

## Mitä kaikkea voi seurata?

GTM:n kautta voi asentaa monenlaisia tagejä: sivuston katselukerrat, kuvan/linkin klikkaus, lomakkeen lähetys etc.

## Muuta

Google Analyticsiin on configuroitu linkitys Prodekon Google Ads accountin kanssa.

![Google Analytics & Google Ads linkitys](images/analytics/google-ads-linkitys.png)