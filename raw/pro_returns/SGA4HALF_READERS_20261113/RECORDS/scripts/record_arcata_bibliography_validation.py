from audit_support import *
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[{'id':'S45-ASTRA-A-0033','page':'74','place':'bibliography [5], Giraud exposé number','printed_reading':'266','tex_reading':'Printed bibliography omitted','change':'Keep266 diplomatically; correct to256 with apparatus in both languages','kind':'misprint_in_print','reason':'Arcata prints266, whereas Ariane p3 gives256. The original Bourbaki paper and primary record confirm exposé256, May1963: https://www.numdam.org/item/SB_1962-1964__8__189_0/.'}])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[{'id':'S45-ASTRA-A-0033','page':'74','place':'bibliography [5], Giraud exposé number','printed':'266','corrected':'256','en_printed':'266','en_corrected':'256','kind':'number','reason':'The same work is correctly numbered256 in Ariane p3; its primary Bourbaki record confirms256: https://www.numdam.org/item/SB_1962-1964__8__189_0/.'}])
p=ROOT/'work/arcata/variants.jsonl';rows=[json.loads(l) for l in p.read_text().splitlines()]
for r in rows:
 if r['id']=='S45-SOL-0038':r['sources']=['SGA45-CORR-0005','S45-SOL-0038']
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
