"""Resolve string-valued page keys for nonprinting continuation-macro FIXLOG rows."""
from review_helpers import Review
r=Review()
for sid in ['fixes/FIXLOG_6.jsonl#332','fixes/FIXLOG_6_CURRENT.jsonl#297']:
    r.source(sid,'The printed object abbreviation is lowercase ob; no macro-definition text is printed.',
      'These string-keyed FIXLOG rows address the nonprinting continuation block after183. The queued operation changes providecommand to renewcommand with an otherwise identical body, installing the continuation definition despite an earlier definition of Ob. The supplied body is operatorname{ob}; its lowercase spelling was independently inspected on183 (checker181_185#15) and in all four object-membership occurrences on187. Preserve that actual macro block unchanged rather than replaying the obsolete uppercase body from the historical log.',
      'Nonprinting ExposéII continuation block after183',verdict='retained; syntax-only transition',change='Retain the attached renewcommand with its already inspected lowercase ob body.',page=183)
for sid in ['fixes/FIXLOG_6.jsonl#333','fixes/FIXLOG_6_CURRENT.jsonl#298']:
    r.source(sid,'No printed identity-operator occurrence or macro definition is introduced at this boundary.',
      'These string-keyed FIXLOG rows address the nonprinting AppendixII block after198. The old and new queued commands have the same operatorname{id} body; renewcommand installs it despite the earlier operatorname{Id} definition, while providecommand would leave that earlier definition in effect. The supplied block already uses renewcommand, is preserved byte-for-byte, and no id invocation occurs in the inspected199–221 appendix body. This is a syntax/definition audit, with no inferred scan glyph or text patch.',
      'Nonprinting AppendixII additions after198',verdict='retained; syntax-only transition',change='Retain the existing nonprinting renewcommand; no content patch.',page=198)
r.commit()
