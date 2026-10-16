"""Build portable static HTML with optional analytics. Run from any directory with Python 3."""
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from html import escape as e

ROOT=Path(__file__).resolve().parents[1]
pubs=json.loads((ROOT/'data/publications.json').read_text())
patents=json.loads((ROOT/'data/patents.json').read_text())
scholar=json.loads((ROOT/'data/scholar-citations.json').read_text())
analytics=json.loads((ROOT/'data/analytics.json').read_text())
site_code=analytics.get('goatcounter_site_code', '')
if site_code and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', site_code):
    raise ValueError('Invalid GoatCounter site code')

def link(url,label,cls=''):
    return f'<a href="{e(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+f'>{label}</a>'

def display_date(value):
    date=datetime.strptime(value, '%d %B %Y')
    return f'{date.day} {date:%b %Y}'

def document(title,description,body,current=''):
    tracking=(f'<script data-goatcounter="https://{site_code}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>' if site_code else '')
    css_version=hashlib.sha256((ROOT/'assets/style.css').read_bytes()).hexdigest()[:12]
    nav=[('index.html#about','About','about'),('index.html#experience','Experience','experience'),('publications.html','Publications','publications'),('patents.html','Patents','patents'),('index.html#contact','Contact','contact')]
    links=''.join(f'<a href="{url}"'+(' aria-current="page"' if key==current else '')+f'>{label}</a>' for url,label,key in nav)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}"><meta name="theme-color" content="#244f9d"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css?v={css_version}"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="header"><div class="wrap nav"><a class="brand" href="index.html">Donggyu Joo <span>주동규</span></a><nav class="nav-links" aria-label="Main navigation">{links}<a class="nav-cv" href="assets/CV_DonggyuJoo.pdf" download data-goatcounter-click="cv-download" data-goatcounter-title="CV download click">CV PDF</a></nav></div></header>
<main id="main" class="wrap">{body}</main><footer class="wrap footer"><span>© 2026 Donggyu Joo</span><span>Computer Vision · Multimodal Learning · On-Device Deployment</span></footer>{tracking}</body></html>'''

def authors(p):
    result=[]
    for i,a in enumerate(p['authors']):
        name=f'<strong>{e(a)}</strong>' if a=='Donggyu Joo' else e(a)
        result.append(name+('<sup>*</sup>' if i in p.get('equal',[]) else ''))
    return ', '.join(result)

def citation_summary():
    total=scholar.get('total_citations')
    if total is None:return ''
    return f'<p class="citation-summary">{link(scholar["profile_url"], f"{total:,} total citations")} <span>· Google Scholar · 14 Oct 2026</span></p>'

def publication(p,archive=False):
    links=[link(p['url'],'Paper')]
    for key,label in [('pdf','PDF'),('poster','Poster')]:
        if p.get(key) and p[key]!=p['url']:links.append(link(p[key],label))
    count=scholar['publications'].get(p['id'])
    count_label='citation' if count==1 else 'citations'
    citation=f'<span class="citation-count" title="Google Scholar · 14 Oct 2026">{count:,} {count_label}</span>' if count is not None else ''
    topic=f'<span class="topic">{e(p["topic"])}</span>' if 'topic' in p and not archive else ''
    return f'''<article class="pub" id="{p['id']}"><div class="venue">{e(p['venue'])}{topic}</div><div><div class="pub-heading"><h3>{link(p['url'],e(p['title']))}</h3>{citation}</div><p class="authors">{authors(p)}</p><p class="summary">{e(p['summary'])}</p><div class="links">{''.join(links)}</div></div></article>'''

selected=''.join(publication(p) for p in pubs if p.get('selected'))
patent_previews=''.join(f'<article class="patent-preview"><h3>{link("patents.html#"+p["id"], e(p["title"]))}</h3><p>{e(p.get("grant",p["publication"]))} · {e(p["status"])}</p></article>' for p in patents)
home=f'''
<section class="hero" id="about" aria-labelledby="name"><div class="hero-copy"><p class="eyebrow">Computer Vision · Multimodal AI · Model Efficiency</p><h1 id="name">Donggyu Joo</h1><p class="role">Senior Machine Learning Scientist · Samsung Research</p><div class="bio"><p>At Samsung Research, I develop on-device models for Galaxy devices, including visual recognition and image–text retrieval.</p><p>My research has focused on model pruning and generative adversarial networks (GANs), with additional work on knowledge distillation, continual learning, depth estimation, and video generation. I received my Ph.D. in Electrical Engineering from KAIST.</p></div><div class="links"><a class="button" href="assets/CV_DonggyuJoo.pdf" download data-goatcounter-click="cv-download" data-goatcounter-title="CV download click">Download CV</a><div class="profile-links"><a href="mailto:jdg10126@gmail.com">Email: jdg10126@gmail.com</a><a href="https://www.linkedin.com/in/donggyu-joo-a0a8ba22b/">LinkedIn</a><a href="https://scholar.google.com/citations?user=C5ULtbwAAAAJ&amp;hl=en">Google Scholar</a></div></div></div><figure class="portrait"><img src="assets/donggyu-joo.jpg" width="200" height="255" alt="Portrait of Donggyu Joo" fetchpriority="high"><figcaption>Seoul, South Korea</figcaption></figure></section>
<div class="focus-strip" aria-label="Research and engineering focus"><div><p class="label">Computer Vision &amp; Multimodal AI</p><p class="value">Visual Recognition &amp; Image–Text Retrieval</p></div><div><p class="label">Model Efficiency</p><p class="value">Compression &amp; Optimization</p></div><div><p class="label">Product Experience</p><p class="value">Deployment &amp; Edge-Case Handling</p></div></div>
<section class="section" id="experience" aria-labelledby="experience-heading">
<div class="section-heading"><h2 id="experience-heading">Experience</h2></div>
<article class="employment">
<header class="employment-heading">
<div><h3>Samsung Research</h3><p class="employment-role">Senior Machine Learning Scientist · Samsung Electronics</p></div>
<p class="employment-meta">Sep 2022 – Present<span>Seoul, South Korea</span></p>
</header>
<div class="employment-impact" aria-label="Production deployment">
<div class="impact-stat"><p class="impact-count">8 models shipped</p><p class="impact-label">On-device AI · Galaxy devices</p></div>
<div class="impact-context"><p>Deployed on <strong>tens of millions of Galaxy devices</strong>.</p><p class="impact-note">Credited as the developer of the deployed models.</p></div>
</div>
<div class="contribution-list">
<section class="contribution-row"><h4>Gallery Search</h4><p>Developed and deployed visual recognition and image–text retrieval models for Galaxy Gallery search. Built GenAI-assisted labeling and filtering workflows for multimodal training data.</p></section>
<section class="contribution-row"><h4>Unintended Touch Detection</h4><p>Developed sequential models to detect unintended pocket touches, optimized for real-time inference on mobile CPUs and deployed on Galaxy devices.</p></section>
<section class="contribution-row"><h4>Model Efficiency &amp; Reliability</h4><p>Optimized models for on-device deployment through TFLite conversion, latency tuning, and device validation. Resolved edge cases using feedback from real-world use.</p></section>
<section class="contribution-row"><h4>Technical Leadership</h4><p>Lead a team of 6 engineers across data curation, modeling, evaluation, and release, coordinating with product and engineering teams.</p></section>
</div>
<p class="experience-tools"><span>Tools:</span> PyTorch · TensorFlow · TFLite</p>
</article>
</section>
<section class="section" id="publications"><div class="section-heading"><div><h2>Selected Publications</h2>{citation_summary()}</div><a href="publications.html">All Publications (13)</a></div><div>{selected}</div><p class="small-note">* Equal contribution.</p></section>
<section class="section" id="education" aria-labelledby="education-heading"><div class="section-heading"><h2 id="education-heading">Education</h2></div><div class="education-list">
<article class="education-row"><div class="education-title"><div class="education-identity"><h3>Ph.D. in Electrical Engineering</h3><p class="education-school">KAIST</p></div><p class="education-years">Feb 2018 – Aug 2022</p></div><p class="thesis"><span>Thesis:</span> Effective Deep Neural Network Compression Based on the Network Pruning</p><p>Advisor: Prof. Junmo Kim</p></article>
<article class="education-row"><div class="education-title"><div class="education-identity"><h3>M.S. in Electrical Engineering</h3><p class="education-school">KAIST</p></div><p class="education-years">Sep 2016 – Feb 2018</p></div><p class="thesis"><span>Thesis:</span> Unconstrained Control of Feature Map Size Using Non-integer Strided Sampling</p><p>Advisor: Prof. Junmo Kim</p></article>
<article class="education-row"><div class="education-title"><div class="education-identity"><h3>B.S. in Electrical Engineering</h3><p class="education-school">KAIST</p></div><p class="education-years">Mar 2013 – Aug 2016</p></div><p class="education-honor">Summa Cum Laude</p></article>
<article class="education-row"><div class="education-title"><div class="education-identity"><h3>High School</h3><p class="education-school">Korea Science Academy of KAIST (KSA)</p></div><p class="education-years">Feb 2010 – Feb 2013</p></div></article>
</div></section>
<section class="section" id="patents" aria-labelledby="patents-heading"><div class="section-heading"><h2 id="patents-heading">Patents</h2><a href="patents.html">Patent Details</a></div><div class="patent-list">{patent_previews}</div></section>
<section class="contact" id="contact"><div><h2>Contact</h2></div><div class="links"><a href="mailto:jdg10126@gmail.com">jdg10126@gmail.com</a><a href="https://www.linkedin.com/in/donggyu-joo-a0a8ba22b/">LinkedIn</a></div></section>'''
(ROOT/'index.html').write_text(document('Donggyu Joo | Computer Vision & Multimodal AI','Donggyu Joo develops on-device visual recognition and image-text retrieval models at Samsung Research, with research in model pruning and GANs.',home))

body='<div class="page-intro"><p class="eyebrow">Research</p><h1>Publications</h1><p>Work on efficient networks, knowledge transfer, continual learning, and visual generation.</p><p class="small-note">* Equal contribution. Preprints and published versions are listed once.</p></div>'
body+=citation_summary()
for year in sorted({p['year'] for p in pubs},reverse=True):
    body+=f'<section class="year-block" aria-labelledby="year-{year}"><h2 id="year-{year}">{year}</h2><div>'+''.join(publication(p,True) for p in pubs if p['year']==year)+'</div></section>'
body+='<p class="small-note archive-end">Publication metadata checked against papers, publisher records, and institutional records; links rechecked on 14 Oct 2026.</p>'
(ROOT/'publications.html').write_text(document('Publications | Donggyu Joo','Publications by Donggyu Joo on model compression, computer vision, continual learning, and generative modeling.',body,'publications'))

body='<div class="page-intro"><p class="eyebrow">Inventions</p><h1>Patent Details</h1><p>Inventors, application and publication numbers, dates, and official records.</p></div>'
for p in patents:
    fields=[('Inventors',', '.join(p['inventors'])),('Country',p['country']),('Application',p['application']),('Publication',p['publication'])]
    if p.get('grant'):fields.append(('Grant number',p['grant']))
    fields += [(label, display_date(value)) for label, value in p['dates'].items()]
    links=[link(p['url'],'Patent record')]
    if p.get('official'):links.append(link(p['official'],'USPTO original PDF'))
    if p.get('official_record'):links.append(link(p['official_record'],'KIPRIS metadata'))
    if p.get('gazette'):links.append(link(p['gazette'],'Original gazette PDF'))
    note='<p class="small-note">Bibliographic details from Google Patents. Official gazette verification is pending.</p>' if p.get('limited') else ''
    body+=f'<article class="patent" id="{p["id"]}"><span class="status">{e(p["country"])} · {e(p["status"])}</span><h2>{e(p["title"])}</h2><dl>'+''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k,v in fields)+'</dl><div class="links">'+''.join(links)+'</div>'+note+'</article>'
body+='<p class="small-note archive-end">Korean titles are provided in English translation; inventor romanizations follow the CV. Registration and gazette publication dates are shown separately. Records reviewed on 8 Oct 2026.</p>'
(ROOT/'patents.html').write_text(document('Patent Details | Donggyu Joo','Public patent records for inventions by Donggyu Joo in neural network learning, knowledge transfer, and image processing.',body,'patents'))
(ROOT/'404.html').write_text(document('Page Not Found | Donggyu Joo','Page Not Found.','<div class="page-intro"><p class="eyebrow">404</p><h1>Page Not Found</h1><p>The page may have moved.</p><a href="index.html">Return to the homepage</a></div>'))
print(f'Built 4 pages, {len(pubs)} publications, {len(patents)} patent records.')
