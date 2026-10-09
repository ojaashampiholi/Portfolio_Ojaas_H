from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, os, xml.etree.ElementTree as ET
root=Path('dist')
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.h1=0;self.links=[];self.meta={};self.canonical='';self.schemas=[];self.script=False;self.buffer='';self.title='';self.in_title=False;self.ids=set();self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.in_title=True
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag=='link' and a.get('rel')=='canonical':self.canonical=a['href']
  if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
  if tag=='script':
   assert a.get('type')=='application/ld+json','Unexpected client script'
   self.script=True;self.buffer=''
 def handle_data(self,data):
  if self.script:self.buffer+=data
  if self.in_title:self.title+=data
 def handle_endtag(self,tag):
  if tag=='script' and self.script:self.schemas.append(json.loads(self.buffer));self.script=False
  if tag=='title':self.in_title=False
pages={p:Page(p.read_text()) for p in root.rglob('*.html')}
assert len(pages)>=9
assert len({p.title for p in pages.values()})==len(pages)
assert len({p.meta['description'] for p in pages.values()})==len(pages)
public=os.getenv('PUBLIC_INDEXABLE')=='true'
origin=os.getenv('SITE_URL','http://localhost:4321').rstrip('/')
base=os.getenv('BASE_PATH','/').rstrip('/')
for path,p in pages.items():
 assert p.h1==1,(path,'h1 count')
 assert p.canonical.startswith(origin+'/'),(path,'canonical')
 assert p.schemas and p.schemas[0]['@graph'][0]['name']=='Ojaas Hampiholi'
 expected='index, follow' if public and path.name!='404.html' else 'noindex, follow'
 assert p.meta['robots']==expected,(path,'index policy')
 for link in p.links:
  u=urlparse(link)
  if u.scheme or u.netloc:continue
  link_path=unquote(u.path)
  if base and base!='/' and (link_path==base or link_path.startswith(base+'/')):link_path=link_path[len(base):] or '/'
  target=root / link_path.lstrip('/') if link_path else path
  if u.path.endswith('/'):target=target/'index.html'
  assert target.exists(),(path,'broken link',link)
  if u.fragment:
   assert target in pages and u.fragment in pages[target].ids,(path,'broken fragment',link)
 assert 'first-post' not in path.as_posix()
rss=ET.parse(root/'rss.xml');sitemap=ET.parse(root/'sitemap.xml')
assert 'first-post' not in (root/'rss.xml').read_text()+(root/'sitemap.xml').read_text()
urls={x.text for x in sitemap.iter() if x.tag.endswith('loc')}
assert len(urls)==len(pages)-1,(len(urls),len(pages))
assert all(u.startswith(origin+'/') for u in urls)
assert not any('/404' in u for u in urls)
robots=(root/'robots.txt').read_text()
assert ('Allow: /' in robots) if public else ('Disallow: /' in robots)
if os.getenv('VERIFY_ARTICLE'):
 article=root/'writing/verification-fixture/index.html'
 assert article.exists()
 p=pages[article]
 blog=p.schemas[0]['@graph'][-1]
 assert blog['@type']=='BlogPosting' and blog['headline']=='Blog pipeline verification fixture'
 assert '2020-01-01' in blog['datePublished']
 assert any('verification-fixture' in e.text for e in rss.iter('link'))
 assert not (root/'writing/future-fixture/index.html').exists()
print(f'PASS: {len(pages)} HTML pages; unique titles/descriptions; canonical URLs; schema JSON; internal links/fragments; no client JS; RSS/sitemap; draft filtering; {"public" if public else "preview"} crawler policy.')
