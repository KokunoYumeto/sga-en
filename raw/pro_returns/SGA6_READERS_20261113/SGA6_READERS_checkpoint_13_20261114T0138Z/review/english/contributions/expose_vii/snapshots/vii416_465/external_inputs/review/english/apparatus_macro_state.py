#!/usr/bin/env python3
"""Freeze source-managed macro meanings at each variant's body occurrence.

The text's declarations are inventoried conservatively: dependencies from every
observed definition of a command are included. TeX, rather than this parser,
determines each command's actual meaning when the body occurrence is typeset.
The supported source declarations are all single-line in this corpus. A new
multiline declaration raises an error so that it cannot silently escape the
dependency inventory.
"""
import hashlib
import re

DECLARATION=re.compile(r'^\\(?:newcommand|providecommand|renewcommand|DeclareMathOperator)\*?\s*\{?\\([A-Za-z@]+)',re.M)
COMMAND=re.compile(r'\\([A-Za-z@]+)')


def prepare_macro_states(source,variants):
    declarations={}
    for match in DECLARATION.finditer(source):
        end=source.find('\n',match.start())
        line=source[match.start():end if end>=0 else len(source)]
        assert line.count('{')==line.count('}'),('multiline macro declaration needs inventory support',match.group(1))
        declarations.setdefault(match.group(1),[]).append(line)
    managed=set(declarations)
    dependencies={name:set().union(*(set(COMMAND.findall(line)) for line in lines)) & managed
                  for name,lines in declarations.items()}
    definitions=[];records=[]
    for variant in variants:
        name=variant['id']
        selected=set(COMMAND.findall(variant['printed']+'\n'+variant['corrected'])) & managed
        direct=sorted(selected)
        while True:
            expanded=selected | set().union(*(dependencies[token] for token in selected)) if selected else set()
            if expanded==selected:break
            selected=expanded
        tokens=sorted(selected)
        definitions.append(r'\expandafter\def\csname SGACapture@'+name+r'\endcsname{%'+'\n')
        for token in tokens:
            definitions.append(r'\global\expandafter\let\csname SGAState@'+name+'@'+token+'\\endcsname\\'+token+'%\n')
        definitions.append('}\n')
        definitions.append(r'\expandafter\def\csname SGARestore@'+name+r'\endcsname{%'+'\n')
        for token in tokens:
            definitions.append('\\expandafter\\let\\expandafter\\'+token+r'\csname SGAState@'+name+'@'+token+r'\endcsname'+'%\n')
        definitions.append('}\n')
        records.append(dict(variant_id=name,direct_source_managed_commands=direct,captured_commands=tokens,
                            relevant_declarations={token:declarations[token] for token in tokens}))
    return ''.join(definitions),dict(
        method='Global TeX let at the exact body variant; local let restoration inside the corresponding apparatus minipage. Source formula tokens are unchanged. The dependency closure includes all observed source definitions; TeX determines the active meaning.',
        source_before_variant_insertion_sha256=hashlib.sha256(source.encode()).hexdigest(),
        source_managed_command_count=len(managed),
        captured_command_union=sorted({token for row in records for token in row['captured_commands']}),
        variant_count=len(variants),variants=records,
        limitation='Source-managed command meanings are preserved. This does not assert a whole-volume font or semantic audit; literal branch and PDF checks remain separate.')
