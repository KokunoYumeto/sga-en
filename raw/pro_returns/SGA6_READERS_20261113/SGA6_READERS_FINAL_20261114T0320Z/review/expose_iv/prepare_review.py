"""Prepare IV review helpers from frozen II tools; do not create scan verdicts."""
from pathlib import Path
import shutil
here=Path(__file__).resolve().parent
prior=here.parent/'expose_ii'
for name in ('review_helpers.py','render_review.py','render_witness.py','render_detail.py','crop_image.py'):
    target=here/name
    if not target.exists():shutil.copyfile(prior/name,target)
print('Prepared review helpers only; no evidence or page status created.')
