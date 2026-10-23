"""Turn an original memo docx (the test-report one, which has both list levels)
into a template: variable paragraphs -> single-run placeholders, 說明 list ->
marker paragraph, and export list-item prototypes per copy as JSON."""
import sys, zipfile, json, copy, re
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
q = lambda t: '{%s}%s' % (W, t)

src, out_docx, out_json = sys.argv[1:4]
zin = zipfile.ZipFile(src)
root = etree.fromstring(zin.read('word/document.xml'))

def ptext(p):
    return ''.join(p.itertext())

def best_rpr(p):
    """rPr of a run that carries the 標楷體 font, else first run."""
    runs = p.findall('w:r', NS)
    for r in runs:
        rp = r.find('w:rPr', NS)
        if rp is not None and rp.find('w:rFonts', NS) is not None and \
                rp.find('w:rFonts', NS).get(q('ascii')) == '標楷體':
            return copy.deepcopy(rp)
    rp = runs[0].find('w:rPr', NS)
    return copy.deepcopy(rp) if rp is not None else None

def set_single_run(p, text):
    rpr = best_rpr(p)
    for r in list(p):
        if r.tag != q('pPr'):
            p.remove(r)
    r = etree.SubElement(p, q('r'))
    if rpr is not None:
        r.append(rpr)
    t = etree.SubElement(r, q('t'))
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

body = root.find('w:body', NS)
tables = body.findall('w:tbl', NS)
assert len(tables) == 3, len(tables)
protos = []
for k, tbl in enumerate(tables):
    for p in tbl.iter(q('p')):
        t = ptext(p)
        if t.strip() in ('劉培森建築師事務所',):
            set_single_run(p, '{{MAIN_TO}}')
        elif t.startswith('內政部國土管理署'):
            set_single_run(p, '{{CC_TO}}')
        elif re.fullmatch(r'\d+年\d+月\d+日', t.strip()):
            set_single_run(p, '{{DATE}}')
        elif t.strip().startswith('UN023'):
            set_single_run(p, '{{DOCNO}}')
        elif t.strip() == '郭登慶':
            set_single_run(p, '{{HANDLER}}')
        elif t.startswith('主旨'):
            set_single_run(p, '{{SUBJECT}}')
    # 說明 list: the cell containing 主旨
    cell = [tc for tc in tbl.iter(q('tc')) if ptext(tc).startswith('{{SUBJECT}}')][0]
    paras = cell.findall('w:p', NS)
    numbered = [p for p in paras if p.find('w:pPr/w:numPr', NS) is not None]
    l0 = numbered[0]                      # "依工程契約…"  (一、)
    l1 = [p for p in numbered if ptext(p).startswith('混凝土')][0]   # (一)
    proto = {}
    for name, p in (('l0', l0), ('l1', l1)):
        c = copy.deepcopy(p)
        set_single_run(c, '{{TEXT}}')
        proto[name] = etree.tostring(c, encoding='unicode')
    protos.append(proto)
    # replace list + trailing empty paragraphs with a marker paragraph
    idx = list(cell).index(numbered[0])
    after = list(cell)[idx:]
    marker = copy.deepcopy(numbered[0])
    set_single_run(marker, '{{ITEMS_%d}}' % k)
    for e in after:
        if e.tag == q('p'):
            cell.remove(e)
    cell.append(marker)

xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
# strip namespace declarations noise from protos: they carry xmlns attrs; remove them
nsdecl = re.compile(r'\sxmlns:\w+="[^"]*"')
protos = [{k: nsdecl.sub('', v) for k, v in p.items()} for p in protos]

zout = zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = xml if item.filename == 'word/document.xml' else zin.read(item.filename)
    zout.writestr(item, data)
zout.close()
json.dump(protos, open(out_json, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok')
