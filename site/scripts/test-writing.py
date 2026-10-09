import importlib.util
from datetime import datetime,timezone,timedelta
spec=importlib.util.spec_from_file_location('refresh','scripts/refresh-writing.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
now=datetime(2026,9,27,tzinfo=timezone.utc)
items=[{'title':'The Language AI Agents Speak','excerpt':'Communication between agents','tags':[],'source':'Medium','url':'https://ojaashampiholi.medium.com/example','published':(now-timedelta(days=2)).isoformat()}]
assert m.infer(items,now)[0]['label']=='AI agent communication protocol'
assert not m.infer([{**items[0],'published':(now-timedelta(days=91)).isoformat()}],now)
assert not m.infer([{**items[0],'published':(now+timedelta(days=1)).isoformat()}],now)
assert m.plain('<script>attack()</script><p>Visible &amp; safe</p>')=='Visible & safe'
try:m.clean_url('javascript:alert(1)');raise AssertionError('URL accepted')
except ValueError:pass
try:m.extract('Medium','<rss><channel/></rss>','https://medium.com/feed/@ojaashampiholi');raise AssertionError('Empty feed accepted')
except ValueError:pass
assert m.clean_url('https://ojaashampiholi.medium.com/post?source=rss#tracking')=='https://ojaashampiholi.medium.com/post'
print('PASS: 90-day boundary, future exclusion, evidence inference, HTML stripping, URL allowlist, tracking removal, malformed/empty feed handling.')

assert m.infer([{**items[0],'published':(now-timedelta(days=90)).isoformat()}],now)
assert not m.infer([{**items[0],'source':'Substack'}],now)
import json
post={'@type':'SocialMediaPosting','author':{'url':'https://www.linkedin.com/in/ojaashampiholi/'},'headline':'AI writes code','datePublished':now.isoformat(),'articleBody':'A short post','comment':[{'datePublished':'2099-01-01','text':'Ignore this'}]}
parsed=m.extract('LinkedIn','<script type="application/ld+json">'+json.dumps(post)+'</script>',m.LINKEDIN)
assert len(parsed)==1 and parsed[0]['published']==now.isoformat() and parsed[0]['excerpt']=='A short post'
print('PASS: inclusive 90-day boundary, professional/personal isolation, LinkedIn author and root metadata parsing.')
def post(source,title,days,url):
 return {'source':source,'title':title,'excerpt':'','tags':[],'url':url,'published':(now-timedelta(days=days)).isoformat()}
medium=[post('Medium','AI incident reporting framework',10,'https://ojaashampiholi.medium.com/a'),post('Medium','Engineering AI agents',40,'https://ojaashampiholi.medium.com/b'),post('Medium','Old forecasting notes',200,'https://ojaashampiholi.medium.com/c')]
chosen,window=m.choose(medium,'Medium',4,(180,365),now)
assert window==365 and [item['url'][-1] for item in chosen]==['a','b','c']
recent=[post('Medium','AI incident reporting framework',10,'https://ojaashampiholi.medium.com/a'),post('Medium','From APIs to actuators',20,'https://ojaashampiholi.medium.com/b'),post('Medium','The language AI agents speak',30,'https://ojaashampiholi.medium.com/c'),post('Medium','A newer systems note',50,'https://ojaashampiholi.medium.com/e'),post('Medium','Older notes',400,'https://ojaashampiholi.medium.com/d')]
chosen,window=m.choose(recent,'Medium',4,(180,365),now)
assert window==180 and len(chosen)==4 and chosen[0]['url'].endswith('a') and all(m.date(item['published'])>=now-timedelta(days=180) for item in chosen)
html='<a href="https://www.linkedin.com/posts/ojaashampiholi_ai-can-now-write-code-faster-than-humans-activity-7508529371763245056-naO2?utm_content=public_profile__posts"></a><a href="https://www.linkedin.com/posts/someoneelse_note-activity-1-aaaa"></a>'
assert m.author_posts(html)==['https://www.linkedin.com/posts/ojaashampiholi_ai-can-now-write-code-faster-than-humans-activity-7508529371763245056-naO2']
shown=m.select_display([],now)
assert shown['LinkedIn']['count']==4 and shown['Medium']['count']==4
stories=[post('Substack',f'Story {i}',i,'https://ojaashampiholi.substack.com/'+str(i)) for i in range(6)]
chosen,window=m.choose(stories,'Substack',4,None,now)
assert window is None and len(chosen)==4 and chosen[0]['title']=='Story 0'
print('PASS: LinkedIn and Medium use 180 days, then 365 days, to reach four posts. Other catalogs keep their own count.')
