"""Create the public CV from approved summaries and verified metadata.
Requires reportlab. The supplied private CV is never copied into the site.
"""
from pathlib import Path
import json
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
pubs=json.loads((ROOT/'data/publications.json').read_text())
patents=json.loads((ROOT/'data/patents.json').read_text())
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Name',fontName='Helvetica',fontSize=27,leading=32,textColor=HexColor('#182332'),spaceAfter=9))
styles.add(ParagraphStyle(name='Section',fontName='Helvetica-Bold',fontSize=13,leading=18,textColor=HexColor('#244f9d'),spaceBefore=15,spaceAfter=8))
styles.add(ParagraphStyle(name='Text',fontName='Helvetica',fontSize=9.5,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallText',fontName='Helvetica',fontSize=8.5,leading=12,spaceAfter=8))
story=[]
def para(s,style='Text'):return Paragraph(s,styles[style])
def add(s,style='Text'):story.append(para(s,style))
add('Donggyu Joo','Name')
add('Senior Machine Learning Scientist | Samsung Research')
add('Seoul, South Korea | <link href="mailto:jdg10126@gmail.com">jdg10126@gmail.com</link>')
add('Research interests','Section')
add('Computer vision, vision-language models, image-text retrieval, model compression, knowledge distillation, generative modeling, and on-device AI.')
add('Experience','Section')
add('<b>Samsung Research, Samsung Electronics</b> | Seoul, South Korea<br/>Senior Machine Learning Scientist | September 2022 - Present')
for s in [
 'Developed and shipped eight on-device AI models, including Gallery Search and unintended touch detection, deployed across tens of millions of Galaxy devices with my name credited as their developer.',
 'Develop on-device visual recognition and vision-language models for semantic photo search in Galaxy Gallery.',
 'Build multimodal data curation, labeling, filtering, training, and evaluation workflows.',
 'Optimize and deploy models on Galaxy devices, including TFLite conversion, latency tuning, on-device validation, and debugging edge cases from user feedback.',
 'Develop sequential classification models for unintended pocket-touch detection with real-time mobile CPU inference.',
 'Lead a team of six engineers across data, modeling, evaluation, and release in collaboration with product and engineering teams.']:
 add('• '+s)
add('Education','Section')
add('<b>KAIST - Ph.D. in Electrical Engineering</b> | March 2018 - August 2022<br/>Thesis: Effective Deep Neural Network Compression Based on the Network Pruning<br/>Advisor: Prof. Junmo Kim')
add('<b>KAIST - M.S. in Electrical Engineering</b> | September 2016 - February 2018<br/>Thesis: Unconstrained Control of Feature Map Size Using Non-integer Strided Sampling<br/>Advisor: Prof. Junmo Kim')
add('<b>KAIST - B.S. in Electrical Engineering</b> | February 2013 - August 2016<br/>Summa Cum Laude')
add('<b>High School</b><br/>Korea Science Academy of KAIST (KSA) | 2010 - 2013')
add('Skills','Section')
add('Python, PyTorch, TensorFlow, TFLite, Git; model optimization, quantization, distillation, data curation, robustness evaluation, and on-device deployment.')
story.append(PageBreak())
add('Publications','Section')
add('* Equal contribution. Preprints are listed once.','SmallText')
for p in pubs:
 names=[]
 for i,a in enumerate(p['authors']):
  n=escape(a)+('*' if i in p.get('equal',[]) else '')
  names.append('<b>'+n+'</b>' if a=='Donggyu Joo' else n)
 story.append(KeepTogether([para(escape(p['title'])+'<br/>'+', '.join(names)+'<br/><i>'+escape(p['venue'])+'</i> · <link color="#244f9d" href="'+escape(p['url'],quote=True)+'">Paper</link>','SmallText')]))
story.append(PageBreak())
add('Patents','Section')
for p in patents:
 if p.get('limited'): continue
 detail=escape(p['grant'] if p.get('grant') else p['publication'])+' | '+escape(p['status'])
 date='; '.join(k+': '+v for k,v in p['dates'].items())
 story.append(KeepTogether([para('<b>'+escape(p['title'])+'</b><br/>'+escape(', '.join(p['inventors']))+'<br/>'+detail+'<br/>Application: '+escape(p['application'])+'<br/>'+escape(date)+'<br/><link color="#244f9d" href="'+escape(p.get('official',p.get('official_record',p['url'])),quote=True)+'">Public record</link>','SmallText')]))
def footer(canvas,doc):
 canvas.setFont('Helvetica',8);canvas.setFillColor(HexColor('#596474'))
 canvas.drawString(42,26,'Donggyu Joo | Public CV | Updated 14 October 2026')
 canvas.drawRightString(553,26,str(doc.page))
doc=SimpleDocTemplate(str(ROOT/'assets/Donggyu_Joo_Public_CV.pdf'),pagesize=(595.28,841.89),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=42,title='Donggyu Joo - Public Curriculum Vitae',author='Donggyu Joo')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Created public CV.')
