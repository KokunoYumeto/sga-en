#!/usr/bin/env python3
from review_helpers import Review,ROOT,read,underline_words
r=Review()
for p,labels,n in[(84,['1.1.1.','1.1.2.','1.1.3.'],6),(85,['1.1.4.','1.1.5.','1.2.'],3)]:
    id=f'ASTRA-I-PARANUM-{p:03d}';reason='Each of these paragraph numbers is plain upright type in the scan; the nearby definition words carry the underline. Restore the observed plain paragraph-number convention independently of the permitted bold statement-label convention.'
    r.own_finding(id,p,'Plain paragraph numbers '+', '.join(labels),r'\textbf paragraph numbers','Plain numbers with unchanged text and punctuation',reason,'Numbered paragraphs',kind='font')
    for label in labels:r.patch(p,'both',r'\textbf{'+label+'}',label,id,reason)
    id=f'ASTRA-I-WORDGROUPS-{p:03d}';reason='The base site S within the defined phrases has its own single short rule. Keep mathematical symbols outside the prose-rule wrappers so their independent underlines remain a single printed notation rather than receiving an extra rule.'
    r.own_finding(id,p,'Word-group underlining with individually underlined site letters',r'\uline wrappers containing inline math','Split prose-rule wrappers at inline mathematical formulas',reason,'Defined phrases containing S-category or S-functor')
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in read('patches.jsonl')+r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:
                assert old.count(patch['old'])==patch['expected_count']
                old=old.replace(patch['old'],patch['new'])
        assert old.count(r'\uline{')==n
        new,count=underline_words(old.replace(r'\uline{',r'\emph{'));assert count==n
        r.patch(p,layer,old,new,id,reason)
r.commit()
