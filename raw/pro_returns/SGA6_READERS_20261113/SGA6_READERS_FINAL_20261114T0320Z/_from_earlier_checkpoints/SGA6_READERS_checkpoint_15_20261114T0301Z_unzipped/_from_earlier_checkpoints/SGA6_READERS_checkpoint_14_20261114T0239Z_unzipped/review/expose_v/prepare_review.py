"""Prepare independent V tools from frozen IV helpers, without copying verdicts."""
from pathlib import Path
import shutil
here=Path(__file__).resolve().parent
prior=here.parent/'expose_iv'
for name in ['review_helpers.py','render_review.py','render_witness.py','render_detail.py','crop_image.py']:
    target=here/name
    if not target.exists():shutil.copyfile(prior/name,target)
print('Prepared V helper scripts only; no image verdict or page status created.')
