import difflib
import re
from docx import Document
from pathlib import Path

def norm(text):
    t = re.sub(r"[\s\u2500\u2014]+", " ", text)
    return re.sub(r" +", " ", t).strip()

def all_text(path):
    doc = Document(str(path))
    return " ".join(p.text for p in doc.paragraphs if p.text.strip())

old = Path(r"c:\Users\a0106\Documents\조승영_202613111_SuperGame.docx.bak")
new = Path(r"d:\VicZero\Coding\SuperGame\docs\조승영_202613111_SuperGame.docx")
o, n = norm(all_text(old)), norm(all_text(new))
print("similarity", round(difflib.SequenceMatcher(None, o, n).ratio(), 4))
print("paragraphs new", len(Document(str(new)).paragraphs))
