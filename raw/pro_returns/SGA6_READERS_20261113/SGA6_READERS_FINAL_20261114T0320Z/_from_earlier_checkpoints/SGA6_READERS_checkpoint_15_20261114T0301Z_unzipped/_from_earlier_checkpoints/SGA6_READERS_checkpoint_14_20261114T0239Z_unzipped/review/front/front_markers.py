"""Exact front-matter boundaries established from the two supplied scans."""
from pathlib import Path

HERE=Path(__file__).resolve().parent

def mark(idx,folio):
    return f'%%%%%%%%%%  scan idx {idx}  |  folio {folio}  %%%%%%%%%%\n'

def integrate_front(text):
    pre,body=text.split('\\begin{document}',1)
    first=body.index('%%%%%%%%%%  scan idx 14  |  folio 1')
    front=body[:first]
    assert front.count('\\begin{center}')==1
    front=front.replace('\\begin{center}',mark(4,'III')+'\\begin{center}',1)
    for title,idx,blank,folio in [('Préface',6,'IV','V'),('Introduction',8,'VI','VII'),('Table des matières',12,'X','XI')]:
        anchor='\\section*{\\underline{'+title+'}}'
        assert front.count(anchor)==1,anchor
        front=front.replace(anchor,mark(idx-1,blank)+mark(idx,folio)+anchor,1)
    anchor='variante analytique complexe du théorème'
    assert front.count(anchor)==1
    front=front.replace(anchor,'variante analytique com%\n'+mark(9,'VIII')+'plexe du théorème',1)
    anchor="d'un morphisme projectif d'espaces analytiques complexes"
    assert front.count(anchor)==1
    front=front.replace(anchor,'\n'+mark(10,'IX')+anchor,1)
    anchor='\\underline{EXPOSÉ VII}'
    assert front.count(anchor)==1
    front=front.replace(anchor,mark(13,'XII')+anchor,1)
    return pre+'\\begin{document}\n'+(HERE/'printed_additions.tex').read_text()+front+body[first:]
