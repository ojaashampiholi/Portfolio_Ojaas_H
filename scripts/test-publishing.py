from pathlib import Path
import subprocess, os
folder=Path('src/content/writing')
a=folder/'verification-fixture.md';b=folder/'future-fixture.md'
assert not a.exists() and not b.exists()
try:
 a.write_text('---\ntitle: Blog pipeline verification fixture\ndescription: Temporary content used to check the native blog, metadata, and feeds.\npublished: 2020-01-01\ndraft: false\n---\n## A question\n\nA concise answer.\n\n## Evidence\n\nA [source](https://docs.astro.build/).\n\n## Limitations\n\nThis is a temporary verification fixture, not an article by Ojaas.\n')
 b.write_text('---\ntitle: Future fixture\ndescription: Must not publish before its date.\npublished: 2099-01-01\ndraft: false\n---\nFuture content.\n')
 env={**os.environ,'SITE_URL':'https://portfolio.example.org','PUBLIC_INDEXABLE':'true','VERIFY_ARTICLE':'true'}
 subprocess.run(['npm','run','build'],env=env,check=True)
 subprocess.run(['python3','scripts/verify.py'],env=env,check=True)
finally:
 a.unlink(missing_ok=True);b.unlink(missing_ok=True)
 subprocess.run(['npm','run','build'],check=True)
 subprocess.run(['python3','scripts/verify.py'],check=True)
