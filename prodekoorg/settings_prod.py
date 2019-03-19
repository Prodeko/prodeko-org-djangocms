"""
Django settings for production environment.

TODO: install this to apache https://tn123.org/mod_xsendfile/

Author: Webbitiimi
"""

FILER_SERVERS = {
    "private": {
        "main": {"ENGINE": "filer.server.backends.xsendfile.ApacheXSendfileServer"},
        "thumbnails": {
            "ENGINE": "filer.server.backends.xsendfile.ApacheXSendfileServer"
        },
    }
}
