"""Reproduce the directly examined native witness37 formula crop."""
from pathlib import Path
from PIL import Image
O=Path(__file__).resolve().parent
Image.open(O/'witness_037.png').crop((100,500,1850,1650)).save(O/'witness_037_formula_detail.png')
