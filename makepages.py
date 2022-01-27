import os

import dominate
import markdown2

from dominate.tags import *
from dominate.util import raw

ROOT = 'https://1923.press'

def get_template(page_title, card_image, page_desc, include_lightbox=False):
    doc = html()
    with doc:
        doc.head = head()
        doc.body = body()

    with doc.head:
        meta(charset='utf-8')
        meta(content='width=device-width, initial-scale=1',
                name='viewport')
        title(page_title)
        meta(name='twitter:card', content='summary_large_image')
        meta(name='twitter:creator', content='@xor')
        meta(name='twitter:title', content=page_title)
        meta(property='og:title', content=page_title)
        meta(name='twitter:image', content=card_image)
        meta(property='og:image', content=card_image)
        meta(name='twitter:description', content=page_desc)
        meta(property='og:description', content=page_desc)

        link(rel='stylesheet', href=ROOT + '/styles/style.css')
        if include_lightbox:
            link(rel='stylesheet', href=ROOT + '/styles/lightbox.css')

    with doc.body:
        with div(id='header'):
            a(h1('1923: A Monthly Zine of Public Domain Treasures'), href=ROOT)
            nav = ul()
            nav.add(li(a('Issues', href=ROOT)))
            nav.add(li(a('About', href=ROOT + '/about')))

    return doc


def do_month(mon):
    month_dict = {'january':  '01',
                  'february': '02',
                  'march':    '03',
                  'april':    '04',
                  'may':      '05',
                  'june':     '06',
                  'july':     '07',
                  'august':   '08',
                  'september':'09',
                  'october':  '10',
                  'november': '11',
                  'december': '12'}

    os.chdir(mon)
    pt = mon.title() + ' | 1923: A Monthly Zine of Public Domain Treasures'    
    doc = get_template(pt, 
                       include_lightbox=True, 
                       card_image=ROOT+'/'+mon+'/cover-crop.jpg',
                       page_desc=f'The {mon} issue of 1923, a monthly zine of public domain treasures.')

    pdf_link = '1923_issue{}.pdf'.format(month_dict[mon])

    with doc.body:
        with div(id='body'):
            img(src='front-and-back-covers.jpg', cls='cover-image')
            fb = div(cls='main-content')
            with fb:
                with open('intro.markdown', 'r') as f:
                    intro = div(raw(markdown2.markdown(f.read())), cls='intro')
                    intro += a('Download this issue as pdf.',
                                href=pdf_link)
            with fb.add(div(cls='gallery')):
                for i in sorted(os.listdir('screenimgs')):
                    a(img(src='screenimgs/' + i, loading="lazy"),
                            href='screenimgs/' + i, data_lightbox="issue")

        script(src='../js/lightbox-plus-jquery.js')

    with open('index.html', 'w') as f:
        f.write('<!DOCTYPE html>\n\n' + doc.render())
            
    os.chdir('..')

def do_index(months):
    pt = '1923: A Monthly Zine of Public Domain Treasures'

    page_desc = '1923 is a year-long zine publication by Parker Higgins distributed on paper to 100 subscribers and online to the world. It was funded through a Kickstarter campaign in January 2019.'

    doc = get_template(pt,
                       card_image=ROOT+'/1923.png',
                       page_desc=page_desc)

    with doc.body:
        with div(id='body').add(ul(cls='issues')):
            for m in months:
                with li():
                    issue_link = a(href=m)
                    issue_link += img(src=m + '/cover-crop.jpg')
                    issue_link += m

    with open('index.html','w') as f:
        f.write('<!DOCTYPE html>\n\n' + doc.render())
            

def do_about():
    pt = 'About | 1923: A Monthly Zine of Public Domain Treasures'

    doc = get_template(pt, 
                       card_image=ROOT+'/about/1923-baby.png',
                       page_desc='About 1923, a year-long zine publication by Parker Higgins distributed on paper to 100 subscribers and online to the world.')

    about = doc.body.add(div(id='body')).add(div(cls='about-content'))

    with about:
        div(img(src='1923-baby.png'), cls='about-img')
        with div(cls='about-text'): 
            with open('about/about_text.markdown', 'r') as f:
                raw(markdown2.markdown(f.read()))

    with open('about/index.html','w') as f:
        f.write('<!DOCTYPE html>\n\n' + doc.render())

def main():
    months =  ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    for m in months:
        do_month(m)

    do_index(months)

    do_about()

if __name__ == '__main__':
    main()
