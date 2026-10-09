"""Fetch public writing metadata and derive evidence-linked themes on each build.
No model calls: transparent tag/phrase rules, not claims about private beliefs.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse, urljoin, urlunparse
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from html import unescape
import json, re, time, xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parents[1]/'src/data/public-writing.json'
POSTS=Path(__file__).resolve().parents[1]/'src/data/linkedin-posts.txt'
PROFILE='https://www.linkedin.com/in/ojaashampiholi/recent-activity/posts/'
LINKEDIN='https://www.linkedin.com/posts/ojaashampiholi_ai-writes-the-design-doc-ai-writes-the-activity-7492304953819013120-HbmL'
BROWSER='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
SOURCES=[('LinkedIn',LINKEDIN),('Medium','https://medium.com/feed/@ojaashampiholi'),('Substack','https://ojaashampiholi.substack.com/feed'),('Cosmic Notebook','https://ojaashampiholi.github.io/the-cosmic-notebook/archives/')]
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def plain(s):
 p=Plain();p.feed(s);return re.sub(r'\s+',' ',' '.join(p.parts)).strip()
def clean_url(s):
 u=urlparse(s)
 if u.scheme!='https' or u.hostname not in {'ojaashampiholi.medium.com','medium.com','ojaashampiholi.substack.com','ojaashampiholi.github.io','www.linkedin.com','in.linkedin.com'}:raise ValueError('Unexpected publication URL')
 return urlunparse((u.scheme,u.netloc,u.path,'','',''))
def date(s):
 try:d=datetime.fromisoformat(s.replace('Z','+00:00'))
 except ValueError:d=parsedate_to_datetime(s)
 return (d if d.tzinfo else d.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
def fetch(url, browser=False):
 req=Request(url,headers={'User-Agent':BROWSER if browser else 'OjaasPortfolio/0.1 (public writing index)','Accept-Language':'en'})
 with urlopen(req,timeout=15) as response:
  if urlparse(response.url).hostname not in {'medium.com','ojaashampiholi.medium.com','ojaashampiholi.substack.com','ojaashampiholi.github.io','www.linkedin.com','in.linkedin.com'}:raise ValueError('Unexpected redirect')
  body=response.read(3_000_001)
  if len(body)>3_000_000:raise ValueError('Feed exceeds size bound')
  return body.decode('utf-8')
def extract(name,body,url):
 entries=[]
 if name=='LinkedIn':
  for raw in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',body,re.S):
   obj=json.loads(raw)
   roots=obj if isinstance(obj,list) else [obj]
   for post in roots:
    if post.get('@type')!='SocialMediaPosting':continue
    if '/in/ojaashampiholi' not in post.get('author',{}).get('url',''):continue
    entries.append({'title':plain(post.get('headline','')),'url':clean_url(url),'published':date(post['datePublished']).isoformat(),'source':name,'excerpt':plain(post.get('articleBody',''))[:280],'tags':[]})
 elif name!='Cosmic Notebook':
  for item in ET.fromstring(body).findall('.//item'):
   title=plain(item.findtext('title') or '')
   when=item.findtext('pubDate');link=item.findtext('link')
   if not title or not when or not link:continue
   description=plain(item.findtext('description') or '')
   description=re.sub(r'Continue reading.*$','',description).strip()
   entries.append({'title':title,'url':clean_url(link),'published':date(when).isoformat(),'source':name,'excerpt':description[:280],'tags':[plain(t.text or '') for t in item.findall('category')]})
 else:
  for card in re.findall(r'<li\b[^>]*data-post-card[^>]*>.*?</li>',body,re.S):
   link=re.search(r'<a\b[^>]*href="([^"]+)"',card);title=re.search(r'<h[23]\b[^>]*>(.*?)</h[23]>',card,re.S);when=re.search(r'<time\b[^>]*datetime="([^"]+)"',card)
   if not(link and title and when):continue
   summary=re.search(r'<p\b[^>]*class="tease"[^>]*>(.*?)</p>',card,re.S)
   tags=re.search(r'data-topics="([^"]*)"',card)
   entries.append({'title':plain(title[1]),'url':clean_url(urljoin(url,unescape(link[1]))),'published':date(when[1]).isoformat(),'source':name,'excerpt':plain(summary[1])[:280] if summary else '', 'tags':json.loads(unescape(tags[1])) if tags else []})
 if not entries:raise ValueError('No dated articles parsed; preserving last successful snapshot')
 return entries
RULES=[
 ('AI writes code','LinkedIn',r'AI writes|software engineer'),
 ('AI incident reporting framework','Medium',r'incident|evidence from explanation'),
 ('engineering AI agents','Medium',r'actuator|physical world'),
 ('AI agent communication protocol','Medium',r'communication|language ai agents'),
 ('sub-Neptune exoplanets','Cosmic Notebook',r'sub-neptune|sub neptune|retrograde'),
 ('planet formation in protoplanetary disks','Cosmic Notebook',r'planet formation|planet-forming|protoplanetary'),
 ('black hole jets explained','Cosmic Notebook',r'jet'),
 ('short stories about deception','Substack',r'appearance|wrong instructions|empty containers|real money')
]
def rank(label,entry):
 words=[w for w in re.findall(r"[a-z0-9]+",label.lower()) if len(w)>3]
 title=entry['title'].lower()
 return sum(w in title or w.rstrip('s') in title for w in words)
def choose(entries,source,count,windows,now):
 pool=sorted([e for e in entries if e['source']==source and date(e['published'])<=now],key=lambda e:e['published'],reverse=True)
 if not windows:return pool[:count],None
 windowed=[]
 for days in windows:
  start=now-timedelta(days=days)
  windowed=[e for e in pool if date(e['published'])>=start]
  if len(windowed)>=count:return windowed[:count],days
 return windowed[:count],windows[-1]
def select_display(entries,now):
 plan=[('LinkedIn',4,(180,365)),('Medium',4,(180,365)),('Substack',4,None),('Cosmic Notebook',4,None)]
 shown={}
 for source,count,windows in plan:
  chosen,days=choose(entries,source,count,windows,now)
  shown[source]={'count':count,'windowDays':days,'entries':chosen}
 return shown
def infer(entries,now):
 start=now-timedelta(days=90);themes=[]
 for label,source,pattern in RULES:
  evidence=[e for e in entries if e['source']==source and start<=date(e['published'])<=now and re.search(pattern,' '.join([e['title'],e['excerpt'],*e['tags']]),re.I)]
  evidence=sorted(evidence,key=lambda e:(rank(label,e),e['published']),reverse=True)
  if evidence:themes.append({'label':label,'source':source,'count':len(evidence),'basis':'Google autocomplete phrase matched to a public title, excerpt, or topic tag','evidence':[{'title':e['title'],'url':e['url'],'published':e['published']} for e in evidence[:3]]})
 return themes

def activity_stamp(url):
 match=re.search(r'activity-(\d+)',url)
 if not match:return datetime.min.replace(tzinfo=timezone.utc)
 return datetime.fromtimestamp((int(match.group(1))>>22)/1000,timezone.utc)
def author_posts(html):
 found=[];seen=set()
 for raw in re.findall(r'https://www\.linkedin\.com/posts/ojaashampiholi_[^"\s<]+',unescape(html)):
  url=clean_url(raw.split('?')[0])
  if url not in seen:seen.add(url);found.append(url)
 return found
def linkedin_targets(html=None):
 found=author_posts(html) if html else []
 if POSTS.exists():
  for line in POSTS.read_text().splitlines():
   line=line.split('#',1)[0].strip()
   if line:found.append(line)
 if LINKEDIN not in found:found.append(LINKEDIN)
 unique=[]
 for url in sorted(set(found),key=activity_stamp,reverse=True):
  if url not in unique:unique.append(url)
 return unique[:12]
def main():
 now=datetime.now(timezone.utc)
 previous=json.loads(OUT.read_text()) if OUT.exists() else {'entries':[],'sources':[]}
 def run(pair):
  name,url=pair
  try:
   if name=='LinkedIn':
    items=[];errors=[];seen=set()
    try:targets=linkedin_targets(fetch(PROFILE,browser=True))
    except Exception as e:targets=linkedin_targets();errors.append(str(e))
    for index,link in enumerate(targets):
     if index:time.sleep(1.2)
     try:
      for item in extract(name,fetch(link,browser=True),link):
       if item['url'] not in seen:seen.add(item['url']);items.append(item)
     except Exception as e:errors.append(str(e))
    if items:return name,items,None
    return name,[],'; '.join(errors) or 'No LinkedIn posts'
   body=fetch(url)
   if name=='Cosmic Notebook':body+=fetch('https://ojaashampiholi.github.io/the-cosmic-notebook/')
   return name,extract(name,body,url),None
  except Exception as e:return name,[],str(e)
 entries=[];statuses=[]
 with ThreadPoolExecutor(max_workers=3) as pool:
  for name,items,error in pool.map(run,SOURCES):
   old=next((s for s in previous['sources'] if s['name']==name),{})
   if error:items=[e for e in previous['entries'] if e['source']==name]
   elif name=='LinkedIn':
    seen={e['url'] for e in items}
    items=items+[e for e in previous['entries'] if e['source']=='LinkedIn' and e['url'] not in seen]
   statuses.append({'name':name,'status':'cached' if error and items else 'unavailable' if error else 'fresh','lastSuccess':old.get('lastSuccess') if error else now.isoformat(),'error':error})
   entries.extend(e for e in items if date(e['published'])<=now)
 unique={(e['source'],e['url']):e for e in entries}
 entries=sorted(unique.values(),key=lambda e:e['published'],reverse=True)
 result={'refreshed':now.isoformat(),'windowDays':90,'windowStart':(now-timedelta(days=90)).date().isoformat(),'sources':statuses,'entries':entries,'shown':select_display(entries,now),'themes':infer(entries,now),'method':'LinkedIn posts are discovered from the public profile, with permalinks in linkedin-posts.txt kept as a backup. LinkedIn and Medium cards are the four newest posts from the last 180 days, widened to 365 days only when 180 days does not yield four. Substack and The Cosmic Notebook show the four newest. Search phrases still use a 90-day match and are not a search-volume ranking.'}
 OUT.parent.mkdir(parents=True,exist_ok=True);tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');tmp.replace(OUT)
 print(json.dumps({'articles':len(entries),'themes':len(result['themes']),'sources':statuses},indent=2))
if __name__=='__main__':main()
