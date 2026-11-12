#!/usr/bin/env python3
"""Focused regression tests for exact-span source attribution."""
import collections
import unittest
from french import token_changes
from french_provenance import PositionSources, AttributionSources, signature


class AttributionTests(unittest.TestCase):
    def matcher(self, records):
        matcher = object.__new__(PositionSources)
        matcher.by_page = collections.defaultdict(list)
        matcher.by_ref = {}; matcher.quote_cache = {}; matcher.token_changes = token_changes
        for record in records:
            row = {'page': '1', 'file': 'test.tex', 'id': record['id'], 'ref': record['id'],
                   'old': record['old'], 'new': record['new']}
            row['source_row_sha256'] = signature(row)
            matcher.add('7I', row, reversible=record.get('reversible', False))
        return matcher

    def context(self, matcher, old, new, comparison='A'):
        old = r'\SGApage{I}{1}' + old; new = r'\SGApage{I}{1}' + new
        hunks = [dict(h, id=str(i), page='1') for i, h in enumerate(token_changes(old, new))]
        return AttributionSources.context(matcher, 'changes', '7I', 'TEST', 'test.tex', old, new,
                                          hunks, 'old.tex', 'new.tex', comparison), hunks

    def proofs(self, matcher, context, hunk):
        return matcher.candidates(context, '1', (hunk['a0'], hunk['a1']), (hunk['b0'], hunk['b1']))[0]

    def test_nearby_longer_record_is_rejected(self):
        matcher = self.matcher([{'id': 'right', 'old': 'Reguliers', 'new': 'Réguliers'},
                                {'id': 'wrong', 'old': 'Ferrier Seminaire Algebres', 'new': 'Ferrier Séminaire Algèbres'}])
        context, hunks = self.context(matcher, 'Reguliers; Ferrier Seminaire Algebres',
                                     'Réguliers; Ferrier Séminaire Algèbres')
        self.assertEqual([p['record'] for p in self.proofs(matcher, context, hunks[0])], ['right'])

    def test_unchanged_manual_patch_context_is_rejected(self):
        matcher = self.matcher([{'id': 'ED', 'old': 'supports, notées H', 'new': 'supports, notée H'}])
        context, hunks = self.context(matcher, '"supports, notée H"', '«supports, notée H»')
        self.assertTrue(all(not self.proofs(matcher, context, h) for h in hunks))

    def test_repeated_generic_atom_is_not_attributed(self):
        matcher = self.matcher([{'id': 'ambiguous', 'old': 'x', 'new': 'y'}])
        context, hunks = self.context(matcher, 'x then x', 'y then y')
        self.assertTrue(all(not self.proofs(matcher, context, h) for h in hunks))

    def test_unanchored_atom_is_not_attributed(self):
        matcher = self.matcher([{'id': 'unanchored', 'old': 'other x context', 'new': 'other y context'}])
        context, hunks = self.context(matcher, 'actual x passage', 'actual y passage')
        self.assertFalse(self.proofs(matcher, context, hunks[0]))

    def test_same_filename_baseline_contexts_have_separate_caches(self):
        matcher = self.matcher([{'id': 'R', 'old': 'foo x bar', 'new': 'foo y bar'}])
        context_a, hunks_a = self.context(matcher, 'foo x bar', 'foo y bar', 'A')
        self.assertTrue(self.proofs(matcher, context_a, hunks_a[0]))
        context_b, hunks_b = self.context(matcher, 'a different x phrase', 'a different y phrase', 'B')
        self.assertFalse(self.proofs(matcher, context_b, hunks_b[0]))

    def test_recorded_diplomatic_restoration_can_be_reversed(self):
        matcher = self.matcher([{'id': 'D', 'old': 'a bar', 'new': 'a foo', 'reversible': True}])
        context, hunks = self.context(matcher, 'a foo', 'a bar')
        proofs = self.proofs(matcher, context, hunks[0])
        self.assertEqual(len(proofs), 1)
        self.assertIn('diplomatic restoration', proofs[0]['record_orientation'])


if __name__ == '__main__':
    unittest.main()
