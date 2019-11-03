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

## Videoiden optimointi

Videot saa helposti muutettua .webm muotoon käyttämällä ffmpeg-työkalua: `brew install ffmpeg`.

Videon leikkaaminen:

```bash
ffmpeg -i abivideo.mov -ss 00:00:54 -to 00:01:27 -async 1 -c copy abivideo_cut.mov
```

Videon konvertoiminen:

```bash
ffmpeg -i abivideo_cut.mov -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus abivideo_webm.webm
```

Mustien palkkien poistaminen videon ylä- ja alareunasta:

```bash
# Cropdetect
$ ffmpeg -ss 20 -i abivideo_cut.mov -vframes 10 -vf cropdetect -f null -
...
[Parsed_cropdetect_0 @ 0x7fd18a905040] x1:0 x2:1919 y1:79 y2:999 w:1920 h:912 x:0 y:84 pts:200 t:0.083333 crop=1920:912:0:84
[Parsed_cropdetect_0 @ 0x7fd18a905040] x1:0 x2:1919 y1:79 y2:999 w:1920 h:912 x:0 y:84 pts:300 t:0.125000 crop=1920:912:0:84
[Parsed_cropdetect_0 @ 0x7fd18a905040] x1:0 x2:1919 y1:79 y2:999 w:1920 h:912 x:0 y:84 pts:400 t:0.166667 crop=1920:912:0:84
...
# Nähdään, että oikea rajaus on 1920:912:0:84
# Tarkastetaan rajaus ffplay:n avulla
$ ffplay -vf crop=1920:912:0:0 abivideo_cut.mov

# Rajaaminen (-an poistaa äänet)
$ ffmpeg -i abivideo_cut.mov -vf crop=1920:912:0:84 -c:a copy -an abivideo_crop.mov
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
