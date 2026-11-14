#!/usr/bin/env python3
from review_helpers import Review
r=Review();id='ASTRA-I-COMPOSITION-094'
reason=(
 'The complete main scan explicitly labels the successive transition maps '
 'v_{i-1}:E′_i→E′_{i-1}, with first map v_{n-1}:E→E′_{n-1}; it gives no cumulative definition of v_i. '
 'Construction1.4.1 changes only the chosen degree. In degree j<n, v_j^j is the inclusion '
 'E^j→E^j⊕M_j, while v_i^j for i<j is the identity of E^j⊕M_j. Thus those later v_i^j '
 'have source E′^j and cannot themselves be the map v^j:E^j→E′^j prescribed in the preceding corollary. '
 'The composite V_i=v_i v_{i+1}...v_{n-1}:E→E′_i has the required source. '
 'For i≤j within the declared sequence i≤n−1, V_{i-1}^j=v_{i-1}^j V_i^j=V_i^j because the additional transition is the identity in degree j. '
 'Hence V_i^j stabilizes with target the printed definition of E′^j. Each finite composite is a chain map, '
 'so its stable components define v:E→E′; the diagram identities u′_i V_i=u give u′v=u. '
 'This proves the replacement by the composite and leaves the already stable formula for u′ unchanged. '
 'The supplied mathematical context was also independently checked by the English reconstruction reviewer; the scan reading was performed here.'
)
r.own_finding(id,94,r'v^j=(v_i)^j, u′^j=(u′_i)^j for i≤j',r'v^j=(v_i)^j',
 r'Current: v^j=(v_i v_{i+1}\ldots v_{n-1})^j',reason,'Last displayed formula and the two preceding triangles',kind='misprint_in_print')
r.patch(94,'current',r'v^j=(v_i)^j',r'v^j=(v_i v_{i+1}\ldots v_{n-1})^j',id,reason)
r.commit()
