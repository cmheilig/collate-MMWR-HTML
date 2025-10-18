#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract MMWR HTML from zipped JSON object
Extract HTML for 56 selected full reports
Extract and trim core HTML for each report
Collate trimmed, revised core HTML into a single HTML file
"""

#%% Set up environment

import zipfile
import json
import re
from tqdm import tqdm
from bs4 import BeautifulSoup
from collections import Counter
from copy import copy

json_zip_path = (
    'https://github.com/cmheilig/harvest-cdc-journals/blob/main/json-outputs/html/mmwr_art_en_html_json.zip')
selectee_construction_folder = (
    '/Users/cmheilig/Documents/professional/chad-essays-on-data/bookdown/'
    'data-in-mmwr/mmwr-selectees/')

#%% Parse JSON and subset to 56 selectees

# Load JSON object from zip archive as a dictionary of HTML strings
with zipfile.ZipFile(json_zip_path, 'r') as _zip_in:
    with _zip_in.open('mmwr_art_en_html.json') as _f_in:
        mmwr_art_en_html = json.load(_f_in)
# del json_zip_path

# List of 56 full reports selected for review
selectees = ['mm6802a1', 'mm6806a2', 'mm6817a3', 'mm6827a2', 'mm6834a3', 'mm6841e3', 'mm6844a1', 'mm6848a1', 'mm6903a1', 'mm6906a3', 'mm6911a5', 'mm6916e1', 'mm6920e2', 'mm6923e4', 'mm6924e1', 'mm6925a1', 'mm6927a4', 'mm6928e3', 'mm6930e1', 'mm6932a1', 'mm6932e5', 'mm6935a2', 'mm6935e2', 'mm6936a5', 'mm6939e2', 'mm6943e3', 'mm6944e3', 'mm6947e2', 'mm6949a2', 'mm695152a3', 'mm7001a4', 'mm7004e3', 'mm7006e2', 'mm7010e3', 'mm7010e4', 'mm7011e3', 'mm7013e3', 'mm7018e1', 'mm7021e1', 'mm7023e2', 'mm7024e1', 'mm7031e1', 'mm7032e3', 'mm7034e5', 'mm7037e1', 'mm7039e3', 'mm7041a2', 'mm7043e2', 'mm7047e1', 'mm705152a2', 'mm705152a3', 'mm7104e1', 'mm7110e1', 'mm7114e1', 'mm7121a2', 'mm7121e1']

# Regular expression to match report identifiers
mm_re = re.compile(r'(mm\d{4,6}[ae]\d{1,2})(?![_-])')

# Dictionary containing HTML for only the 56 selectees
selectee_html = {
    mm_re.search(k).group(): v
    for k, v in mmwr_art_en_html.items()
    if mm_re.search(k) and (mm_re.search(k).group() in selectees)}
# selectees == list(selectee_html) # True
# del mmwr_art_en_html

selectee_soup = {
    k: BeautifulSoup(v, 'lxml')
    for k, v in tqdm(selectee_html.items())}
# 56/56 [00:01<00:00, 55.71it/s]

#%% Explore parsed HTML to prepare to trim and modify

# Exactly 1 occurrence of <div class="content-fullwidth"> in mm6802a1
len(selectee_soup['mm6802a1'].find_all(attrs={'class': 'content-fullwidth'}))

# Exactly 1 occurrence of <div class="content-fullwidth">, <h1> in each selectee
Counter([len(soup.find_all(attrs={'class': 'content-fullwidth'})) 
         for soup in selectee_soup.values()]) # Counter({1: 56})
Counter([len(soup.find_all(name='h1')) 
         for soup in selectee_soup.values()]) # Counter({1: 56})

# 1 or 2 occurrences of <a href="mailto"> in each selectee
Counter([len(soup.find_all(name='a', href=re.compile('mailto:.+'))) 
         for soup in selectee_soup.values()]) # Counter({1: 54, 2: 2})

# Subelements to remove from parse trees, 1 each per selectee
Counter([len(soup.find_all(attrs={'class': 'tp-related-pages'})) 
         for soup in selectee_soup.values()]) # Counter({1: 56})
Counter([len(soup.find_all(attrs={'class': 'no-syndicate'})) 
         for soup in selectee_soup.values()]) # Counter({1: 56})
Counter([len(soup.find_all(attrs={'class': 'pull-left'})) 
         for soup in selectee_soup.values()]) # Counter({1: 56})

# Consistent attributes in <div class="content-fullwidth"> and its parent element
Counter([
    (str(soup.find(attrs={'class': 'content-fullwidth'}).parent.attrs) +
     str(soup.find(attrs={'class': 'content-fullwidth'}).attrs))
    for soup in selectee_soup.values()])
Counter({"{'class': ['row']}{'class': ['col', 'content', 'content-fullwidth']}": 56})

#%% Function to extract and trim core HTML for each report

def extract_report(rep_id):
    "Given soup for selected report, return trimmed HTML string"
    # Extract element of interest; copy is faster than re-parsing
    soup_x = copy(selectee_soup[rep_id].find(attrs={'class': 'content-fullwidth'}).parent)
    soup_x.find(attrs={'class': 'tp-related-pages'}).decompose()
    soup_x.find(attrs={'class': 'no-syndicate'}).decompose()
    soup_x.find(attrs={'class': 'pull-left'}).decompose()

    # Replace 'Top' with '(Top of page | Top of report)'
    top_top_soup = BeautifulSoup(
        f'<p class="text-right">[&nbsp;<a href="#">Top of page</a> | '
        f'<a href="#_{rep_id}">Top of {rep_id}</a>&nbsp;]</p>',
        'lxml')
    # '<p class="text-right"><a href="#">Top</a></p>'
    for pTag in soup_x.find_all(name='p', class_="text-right"):
        pTag.replace_with(copy(top_top_soup).p) # kludge

    # <a: modify a elements
    for aTag in soup_x.find_all(name='a'):
        # <a aria-controls=
        if (aTag.get('aria-controls') and 
            re.match(r'nav-group-\w{5}', aTag.get('aria-controls'))):
                aTag['aria-controls'] += f'_{rep_id}'
        # <a href=
        if aTag.get('href'):
            # mailto, tel
            if aTag['href'].startswith(('mailto:', 'tel:')):
                    aTag.unwrap()
            # remove selected anchor values
            elif aTag['href'] in {'#headerSearch', '#share-new'}:
                print('#headerSearch, #share-new')
                aTag['href'] = ''
            # remove social media references
            elif re.search(
                '((api\\.addthis|facebook|instagram|linkedin|pinterest|snapchat|twitter|youtube)\\.com|tools\\.cdc.gov)', 
                aTag['href'], flags=re.X):
                aTag['href'] = ''
            # add report ID to selected anchors: unique values when collated
            elif re.match(
                r'\#([BFT][123]_(up|down)|nav-group-\w{5}|References|'
                r'content|contribAff|discussion|suggestedcitation)',
                aTag['href']):
                aTag['href'] += f'_{rep_id}'
            # change relative pdf href to local reference
            elif rep_id in aTag['href']:
                aTag['href'] = re.sub(
                    rf'/mmwr/.*?/({rep_id}.*?\.pdf).*', r'pdfs/\1', aTag['href'])
            # change other relative reference to absolute URL
            elif aTag['href'].startswith('/mmwr/volumes'):
                aTag['href'] = 'https://www.cdc.gov' + aTag['href']
        # <a id=: modify a:id elements
        if aTag.get('id'):
            if re.match(
                r'(Acknowledgment|[BFT][123]_(up|down)|'
                r'contribAff|discussion|suggestedcitation|References)',
                aTag['id']):
                aTag['id'] += f'_{rep_id}'
        # <a title=: modify a:title elements
        if aTag.get('title') and aTag['title'].startswith('Acknowledgment'):
            aTag['title'] +=  f'_{rep_id}'
    # <img src=: modify img:src elements
    for aTag in soup_x.find_all(name='img'):
            # change relative gif href to local reference
            if rep_id in aTag['src']:
                aTag['src'] = re.sub(
                    rf'/mmwr/.*?/({rep_id}.*?\.gif).*', r'gifs/\1', aTag['src'])
            # change other relative image source values to absolute URL
            elif aTag['src'].startswith('/mmwr/volumes'):
                aTag['src'] = 'https://www.cdc.gov' + aTag['href']
            # change arrow_up.gif reference to local reference
            elif aTag['src'] == '//www.cdc.gov/images/arrow_up.gif':
                aTag['src'] = 'gifs/arrow_up.gif'
                # move arrow_up to end of figure element, consiste with tables
                figTag = aTag.parent.parent # h5 element containing figure
                imgTag = figTag.img.parent.extract()
                figTag.strong.insert_after(imgTag)
    # <p id=: modify p:id elements
    for aTag in soup_x.find_all(name='p', id='suggestedcitation'):
        aTag['id'] +=  f'_{rep_id}'
    # <h1: modify h1 element
    assert len(soup_x.find_all(name='h1')) == 1
    # put report identifier in h1 title and insert report-specific anchor
    soup_x.find(name='h1').string += f' [{rep_id}]'
    soup_x.find(name='h1').insert(0,
        BeautifulSoup(f'<a id="_{rep_id}"></a>', 'lxml').find('a'))
    # insert class="clear" to force opening paragraph not to wrap previous element
    first_para = soup_x.find(string='Related Materials').find_next('div', class_='w-100')
    first_para['class'] += ['clear']
    # <hr: remove horizontal rules
    assert len(soup_x.find_all(name='hr')) == 1
    soup_x.find(name='hr').decompose()
    html = re.sub('</div><br/>', '</div><!--br/-->', str(soup_x))

    return html # str(soup_x)

selectee_html_x = {rep_id: extract_report(rep_id) for rep_id in tqdm(selectees)}
# 56/56 [00:00<00:00, 87.38it/s]

#%% Collate trimmed, revised core HTML into a single HTML file
#   with preconstructed head, table of contents, and tail

with open(selectee_construction_folder +
          'mmwr-selectees-compiled.html', 'w') as _f_out:
    # preconstructed head contains <head>, overall title,
    with open(selectee_construction_folder +
              'mmwr-selectees-head.html', 'r') as _f_in:
        _f_out.write(_f_in.read())
    # preconstructed table of contents
    with open(selectee_construction_folder +
              'mmwr-selectees-toc.html', 'r') as _f_in:
        _f_out.write(_f_in.read())
    # trimmed, revised core HTML for each of the 56 selectees
    for _rep_id in selectees:
        _f_out.write('\n<hr style="border-top:1px solid"/>\n')
        _f_out.write(selectee_html_x[_rep_id])
    # preconstructed tail to close </body>
    with open(selectee_construction_folder +
              'mmwr-selectees-tail.html', 'r') as _f_in:
        _f_out.write(_f_in.read())

#%% Extra code: write selectees back out
with open('/Users/cmheilig/Temp/_move-or-delete/selectee_html.json', 'w') as _f_out:
    json.dump(selectee_html, _f_out)

with open('/Users/cmheilig/Temp/_move-or-delete/mm6802a1.html', 'w') as _f_out:
    _f_out.write(selectee_html['mm6802a1'])
with open('/Users/cmheilig/Temp/_move-or-delete/mm7121e1.html', 'w') as _f_out:
    _f_out.write(selectee_html['mm7121e1'])
