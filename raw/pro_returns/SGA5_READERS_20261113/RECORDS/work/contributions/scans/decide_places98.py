#!/usr/bin/env python3
"""Reproduce the recorded visual decisions; supplied scans are the evidence.

The coordinates and classifications below were determined by direct visual
inspection of every occurrence, rather than estimated from source line numbers.
Run from a directory containing the extracted SGA5_FR, SGA5_EN and SGA5_SCANS
directories, or supply --sources.  Pillow is needed only for evidence crops.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


# id-order: (folio, strip, bounding box in original strip pixels).
# Boxes contain the R, its two lower strokes and the neighbouring Gamma.
REGIONS = [
    (457, 1, (655, 505, 744, 565)),
    (457, 1, (538, 580, 615, 640)),
    (457, 1, (790, 580, 874, 641)),
    (457, 1, (1145, 580, 1227, 641)),
    (457, 3, (199, 477, 280, 540)),
    (457, 3, (457, 477, 535, 540)),
    (457, 3, (831, 477, 918, 540)),
    (458, 2, (320, 480, 400, 540)),
    (458, 2, (832, 480, 914, 540)),
    (458, 2, (991, 552, 1072, 614)),
    (458, 2, (1172, 653, 1245, 708)),
    (459, 3, (165, 478, 249, 543)),
    (460, 1, (175, 207, 245, 270)),
    (460, 1, (668, 207, 740, 270)),
    (460, 1, (1395, 204, 1468, 266)),
    (460, 1, (548, 474, 618, 534)),
    (460, 1, (1396, 468, 1469, 529)),
    (460, 2, (708, 42, 784, 103)),
    (460, 2, (1397, 78, 1477, 140)),
    (460, 1, (1057, 161, 1119, 225)),
    (460, 1, (984, 410, 1045, 472)),
    (460, 1, (1221, 621, 1285, 681)),
    (461, 2, (463, 412, 533, 473)),
    (461, 2, (1038, 401, 1107, 458)),
    (470, 3, (1238, 102, 1307, 154)),
    (470, 3, (922, 181, 991, 233)),
    (472, 2, (1002, 425, 1073, 483)),
    (472, 3, (1082, 506, 1153, 560)),
    (473, 1, (1003, 629, 1074, 685)),
    (473, 2, (233, 92, 305, 144)),
    (474, 1, (866, 551, 938, 606)),
    (474, 1, (1260, 567, 1332, 621)),
]

LOCATIONS = [
    'Proposition 2(c), endomorphism in the statement',
    'Proposition 2(c), first object of the displayed composite',
    'Proposition 2(c), middle object of the displayed composite',
    'Proposition 2(c), final object of the displayed composite',
    'Proof of Proposition 2, first object in the second factorization',
    'Proof of Proposition 2, middle object in the second factorization',
    'Proof of Proposition 2, final object in the second factorization',
    'Proof of Proposition 2(c), first identification with H^0',
    'Proof of Proposition 2(c), second identification with H^0',
    'Proof of Proposition 2(c), endomorphism identified with psi_I',
    'Proof of Proposition 2(c), subscript of the concluding identity',
    'Corollary to Proposition 3, endomorphisms in the statement',
    'Corollary diagram, node A at upper left',
    'Corollary diagram, node B at upper centre',
    'Corollary diagram, node C at upper right',
    'Corollary diagram, node D at middle left',
    'Corollary diagram, node E at middle right',
    'Corollary diagram, lower diagonal arrow label represented by node F in TeX',
    'Corollary diagram, node G at lower right',
    'Corollary diagram, upper horizontal arrow label B to C',
    'Corollary diagram, middle horizontal arrow label D to E',
    'Corollary diagram, lower right arrow label E to G',
    'Definition of geometric Frobenius, subscript of fr',
    'Definition of geometric Frobenius, following automorphism object',
    'Proper-case proof, first subscript in the Frobenius inverse relation',
    'Proper-case proof, second subscript in the Frobenius inverse relation',
    'Formula (3), subscript on the right-hand trace',
    'Inverse-limit cohomology formula at the end of the paragraph',
    'Application to Proposition 2, defining K_nu',
    'Application to Proposition 2, defining h_nu',
    'Mittag-Leffler argument, K_nu in the case under consideration',
    'Mittag-Leffler argument, h_nu in the case under consideration',
]

DIP = r'\underline{\underline{\mathrm{R}}}\Gamma'
COR = r'\mathrm{R}\Gamma'


def source_occurrences(text):
    marker = re.compile(r'%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+(\d+)')
    pages = list(marker.finditer(text))
    result = []
    for i, p in enumerate(pages):
        folio = int(p.group(2))
        if not 457 <= folio <= 474:
            continue
        end = pages[i + 1].start() if i + 1 < len(pages) else len(text)
        for m in re.finditer(r'\\(?:RGamma|R\\Gamma)', text[p.end():end]):
            pos = p.end() + m.start()
            result.append({'folio': folio, 'source_tex': m.group(),
                           'start': pos, 'end': p.end() + m.end(),
                           'line': text.count('\n', 0, pos) + 1,
                           'context': text[max(p.end(), pos - 90):min(end, pos + 130)].replace('\n', ' ')})
    assert len(result) == 32, len(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, default=Path('scans_decisions'))
    args = parser.parse_args()
    fr = args.sources / 'SGA5_FR'
    en = args.sources / 'SGA5_EN'
    scans = args.sources / 'SGA5_SCANS'
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    evidence = output / 'evidence'
    evidence.mkdir(exist_ok=True)

    with (scans / 'PLACES_98.tsv').open(encoding='utf-8', newline='') as f:
        original = list(csv.DictReader(f, delimiter='\t'))
    current_path = 'fr/sga5/current/s5.tex'
    dip_path = 'fr/sga5/diplomatic/s5.tex'
    cur_text = (fr / current_path).read_text()
    dip_text = (fr / dip_path).read_text()
    currents = source_occurrences(cur_text)
    diplomatics = source_occurrences(dip_text)

    en_path = 'en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
    en_text = (en / en_path).read_text()
    en_start = en_text.index(r'\section*{Exposé XV}')
    en_matches = list(re.finditer(r'\\RGamma|(?<![A-Za-z\\])R\\Gamma', en_text[en_start:]))
    assert len(en_matches) == 33, len(en_matches)
    targets = en_matches[:22] + en_matches[23:]
    assert len(targets) == 32

    try:
        from PIL import Image
    except ImportError:
        Image = None

    decisions = []
    table = []
    for n, ((folio, strip, box), location, initial, current, dip, english) in enumerate(
        zip(REGIONS, LOCATIONS, original, currents, diplomatics, targets), 1
    ):
        ident = f'R98-{n:02d}'
        assert ident == initial['id']
        assert folio == int(initial['folio']) == current['folio'] == dip['folio']
        image_path = f'scans/page_{folio}_s{strip}.png'
        image_region = image_path + ' [x0,y0,x1,y1=' + ','.join(map(str, box)) + '; origin=upper-left; native pixels]'
        reason = (location + ': the scan shows the R body and two separate short horizontal strokes immediately beneath it. '
                  'The diplomatic reading reproduces those two strokes; the corrected reading uses the existing upright-R derived-functor convention recorded in GLOBAL_ISSUES 98. '
                  'This is a recorded typographic variant; the argument, subscript and Gamma are retained.')
        if n == 18:
            reason += (' The full lower label in strip s2 supplies both strokes, correcting the provisional plain-R description in GLOBAL_ISSUES 98.')
        if n == 25:
            reason += (' checker_crops/c470_frRG.png cuts off the lower edge; the full strip and checker_crops/c470_frRG2.png reveal both strokes.')
        if n == 26:
            reason += (' checker_crops/c470_fRG.png independently shows both strokes.')
        supplemental = initial['checker_crops']
        en_pos = en_start + english.start()
        entry = {
            'id': ident, 'ordinal': n, 'folio': folio,
            'print_has': 'other: ordinary upright/typescript R with two underlines',
            'image': image_path, 'region_native_pixels': list(box),
            'image_sha256': hashlib.sha256((scans / image_path).read_bytes()).hexdigest(),
            'checker_crops_inspected': supplemental.split(',') if supplemental else [],
            'diplomatic_reading': DIP, 'corrected_reading': COR,
            'kind': 'derived-functor typography; GLOBAL_ISSUES 98',
            'reason': reason,
            'fr_current': {'path_in_zip': current_path, **current},
            'fr_diplomatic': {'path_in_zip': dip_path, **dip},
            'en_ported': {
                'path_in_zip': en_path, 'source_tex': english.group(),
                'ordinal_in_xv_RGamma_sequence': en_matches.index(english) + 1,
                'start': en_pos, 'end': en_start + english.end(),
                'line': en_text.count('\n', 0, en_pos) + 1,
                'context': en_text[en_pos - 90:en_pos + 130].replace('\n', ' '),
            },
        }
        decisions.append(entry)
        table.append([ident, folio, entry['print_has'], image_region, DIP, COR, reason,
                      location, supplemental, f'evidence/{ident}.png'])
        if Image:
            im = Image.open(scans / image_path)
            im.crop(box).save(evidence / f'{ident}.png')

    with (output / 'PLACES_98_DECIDED.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(['id', 'folio', 'printed_reading', 'image_region', 'diplomatic_reading',
                         'corrected_reading', 'reason', 'place', 'checker_crops', 'evidence_crop'])
        writer.writerows(table)

    plain = en_matches[22]
    plain_pos = en_start + plain.start()
    control = {
        'id': 'R98-control-461', 'folio': 461,
        'print_has': 'plain upright/typescript R with no underlining',
        'included_in_requested_32': False,
        'image': 'scans/page_461_s2.png', 'region_native_pixels': [90, 88, 159, 151],
        'checker_crop': 'checker_crops/p461_RGamma1.png',
        'diplomatic_reading': COR, 'corrected_reading': COR,
        'reason': 'The R in the sentence saying that the endomorphism is defined by the pair has a bare lower margin. The two underlined occurrences later on the same strip carry distinct visible lower strokes. French already uses explicit upright R here. English has RGamma, so replace it explicitly in every English form.',
        'en_ported': {'path_in_zip': en_path, 'source_tex': plain.group(),
                      'ordinal_in_xv_RGamma_sequence': 23, 'start': plain_pos,
                      'end': en_start + plain.end(),
                      'line': en_text.count('\n', 0, plain_pos) + 1,
                      'context': en_text[plain_pos - 90:plain_pos + 180].replace('\n', ' ')},
    }
    payload = {'counts': {'requested_places': 32, 'double_underlined_R': 32, 'plain_R': 0,
                           'bold_R': 0, 'double_struck_R': 0},
               'coordinates': 'Native image pixels: [x0,y0,x1,y1], origin upper left, right and lower edges exclusive.',
               'decisions': decisions, 'outside_set_control': control}
    (output / 'PLACES_98_PATCHES.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    if Image:
        im = Image.open(scans / 'scans/page_460_s2.png')
        im.crop((685, 35, 1050, 120)).resize((1460, 340)).save(evidence / 'R98-18-detail.png')
        im = Image.open(scans / control['image'])
        im.crop(control['region_native_pixels']).save(evidence / 'R98-control-461.png')
        from PIL import ImageDraw
        for start in (1, 17):
            sheet = Image.new('RGB', (1280, 1240), 'white')
            draw = ImageDraw.Draw(sheet)
            for j, number in enumerate(range(start, start + 16)):
                im = Image.open(evidence / f'R98-{number:02d}.png').convert('RGB')
                im = im.resize((im.width * 3, im.height * 3))
                x, y = (j % 4) * 320, (j // 4) * 310
                sheet.paste(im, (x + 10, y + 40))
                draw.text((x + 15, y + 10), f'R98-{number:02d}', fill='black')
            sheet.save(evidence / f'contact_{start:02d}.png')
    print(json.dumps(payload['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
