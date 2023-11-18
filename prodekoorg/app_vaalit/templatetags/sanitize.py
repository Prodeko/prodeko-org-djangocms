import re
from django.template import Library
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup, Comment

register = Library()

@register.filter
@stringfilter
def sanitize(value):
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = 'a b blockquote br code dd del details div dl dt em h1 h2 h3 h4 h5 h6 hr i img ins kbd li ol p pre q rp rt ruby s samp span strike strong sub summary sup table tbody td tfoot th thead tr tt ul var'.split()
    validAttrs = 'href src width height'.split()
    soup = BeautifulSoup(value, features='lxml')
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        for attr, val in attrs.items():
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                tag.attrs[attr] = val

    return soup.renderContents().decode('utf8')
