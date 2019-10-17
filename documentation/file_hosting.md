# Tiedostoista :open_file_folder::file_folder:

- **Päivitetty** 15.10.2019
- **Tekijä:** Timo Riski

Prodissa prodeko.org static- ja mediatiedostot hostataan Azure Storagessa. Storage blobeja on kaksi: static/ ja media/. Blobien edessä on CDN.

## Setup

1. Luo infrastruktuuri Azureen infrastructure/ kansion ohjeiden mukaan.
2. Määritä settings.py käyttämään `DEFAULT_FILE_STORAGE = "prodekoorg.custom_azure.AzureMediaStorage"` ja `STATICFILES_STORAGE = "prodekoorg.custom_azure.AzureStaticStorage"`.
3. Aja `python3 manage.py collectstatic`, jotta tiedostot kopioituvat Azureen.

## Filer-tiedostot

Asetuksen settings/prod.py FILER_STORAGES muuttuja osoittaa Azureen, devissä lokaaliin filesystemiin. Jos fileriin lähettää kuvatiedotoja, niistä muodostuu automaattisesti thumbnailit mediastorageen. Thumbnailit ovat optimoituja kuvia, jotta täysikokoisia ei lähetetä clientille.

## Kuvien optimointi

Kuvat on optimoitu käyttäen ImageMagick ja pngquant työkaluja. `brew install imagemagic && brew install pngquant`.

.jpg-kuvat (ImageMagick)

```
# Single file
convert prodeko-logo-text-blue.png -resize 700x200 test.png     # Create a new file
magick mogrify -resize 20% test.png                             # Overwrite existing file

# Multiple files
magick mogrify -resize 70% -path . *.png
```

.png-kuvat (pngquant)

```
# Single file
pngquant file.png

# Multiple files
for X in *.png; do pngquant "$X"; done                          # Create new files
for X in *.png; do pngquant "$X" --ext .png --force; done       # Overwrite existing files
```

## AzCopy

"AzCopy is a command-line utility that you can use to copy blobs or files to or from a storage account." AzCopyn saa ladattua [täältä](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10)

Komentoriviltä Azureen saa lähetettyä tiedostoja seuraavasti:

```
azcopy copy "media/filer/filer_public/*" "https://prodekostorage.blob.core.windows.net/media/filer/filer_public" --recursive
```

Ja poistettua seuraavasti:

```
azcopy rm "https://prodekostorage.blob.core.windows.net/media/filer_public_thumbnails/filer_public" --recursive=true
```

## Muuta

Mikäli modelissa käytetään FileFieldiä tai ImageFieldiä ja näihin liittyvä objekti poistetaan, kuvat/tiedostot eivät automaattisesti poistu Azuresta. Jotta turhia tiedostoja ei jää lojumaan Azureen, on modeleille määritettävä post_delete-hook. Esimerkkiä määritykseen voi katsoa prodekoorg/app_infoscreen/models.py tiedostosta:

```python
@receiver(post_delete, sender=Slide)
def slide_delete(sender, instance, **kwargs):
    instance.image.delete(False)
```
