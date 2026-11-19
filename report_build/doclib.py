# Helpers for building the WebtiqAI project report in Word format.
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
IMG = "img/"

# ----------------------------------------------------------------- low level
def _set_font(run, name=FONT, size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(a), name)


def _spacing(par, line=1.5, before=0, after=6):
    pf = par.paragraph_format
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)


def keep_with_next(par):
    pPr = par._p.get_or_add_pPr()
    k = OxmlElement("w:keepNext")
    pPr.append(k)


def page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)
    return p


def field(par, code):
    run = par.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = code
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = " "
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2); run._r.append(t); run._r.append(f3)
    _set_font(run, size=12)
    return run


# ----------------------------------------------------------------- document
def new_doc(a4=True, left=1.5, right=1.0, top=1.0, bottom=1.0):
    doc = Document()
    s = doc.sections[0]
    if a4:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
    s.left_margin = Inches(left)
    s.right_margin = Inches(right)
    s.top_margin = Inches(top)
    s.bottom_margin = Inches(bottom)

    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(12)
    rPr = st.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(a), FONT)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # heading styles -> Times New Roman, black
    for name, size in (("Heading 1", 14), ("Heading 2", 14), ("Heading 3", 13)):
        h = doc.styles[name]
        h.font.name = FONT
        h.font.size = Pt(size)
        h.font.bold = True
        h.font.color.rgb = RGBColor(0, 0, 0)
        hr = h.element.get_or_add_rPr()
        rf = hr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); hr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), FONT)
    return doc


def footer_pagenum(doc, different_first=True):
    s = doc.sections[0]
    s.different_first_page_header_footer = different_first
    p = s.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(p, line=1.0, after=0)
    field(p, "PAGE")


# ----------------------------------------------------------------- blocks
def h1(doc, text):
    p = doc.add_paragraph(style="Heading 1")
    r = p.add_run(text)
    _set_font(r, size=14, bold=True)
    _spacing(p, line=1.5, before=14, after=8)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    keep_with_next(p)
    return p


def h2(doc, text):
    p = doc.add_paragraph(style="Heading 2")
    r = p.add_run(text)
    _set_font(r, size=14, bold=True)
    _spacing(p, line=1.5, before=12, after=6)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    keep_with_next(p)
    return p


def h3(doc, text):
    p = doc.add_paragraph(style="Heading 3")
    r = p.add_run(text)
    _set_font(r, size=13, bold=True)
    _spacing(p, line=1.5, before=10, after=4)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    keep_with_next(p)
    return p


def para(doc, text, size=12, align="justify", indent=0, after=6, line=1.5, bold=False, italic=False):
    p = doc.add_paragraph()
    # inline **bold** support
    parts = text.split("**")
    for i, part in enumerate(parts):
        if part == "":
            continue
        r = p.add_run(part)
        _set_font(r, size=size, bold=(bold or i % 2 == 1), italic=italic)
    p.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                   "left": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER}[align]
    _spacing(p, line=line, after=after)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    return p


def bullet(doc, text, size=12, indent=0.35):
    p = doc.add_paragraph(style="List Bullet")
    parts = text.split("**")
    for i, part in enumerate(parts):
        if part == "":
            continue
        r = p.add_run(part)
        _set_font(r, size=size, bold=(i % 2 == 1))
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    _spacing(p, line=1.5, after=3)
    p.paragraph_format.left_indent = Inches(indent + 0.25)
    return p


_counter = [0]


def num_reset():
    _counter[0] = 0


def numbered(doc, text, size=12, indent=0.35):
    _counter[0] += 1
    p = doc.add_paragraph()
    _set_font(p.add_run("%d.  " % _counter[0]), size=size)
    parts = text.split("**")
    for i, part in enumerate(parts):
        if part == "":
            continue
        r = p.add_run(part)
        _set_font(r, size=size, bold=(i % 2 == 1))
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    _spacing(p, line=1.5, after=4)
    p.paragraph_format.left_indent = Inches(indent + 0.3)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    return p


def code(doc, lines, size=9.5, caption=None):
    if caption:
        c = doc.add_paragraph()
        r = c.add_run(caption)
        _set_font(r, size=11, bold=True)
        _spacing(c, line=1.0, before=8, after=3)
        keep_with_next(c)
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    shade(cell, "F4F4F8")
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
    for ln in lines:
        p = cell.add_paragraph()
        r = p.add_run(ln if ln else " ")
        _set_font(r, name="Consolas", size=size)
        _spacing(p, line=1.0, after=0)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sp = doc.add_paragraph()
    _spacing(sp, line=1.0, after=0)
    return tbl


def figure(doc, filename, caption, width=6.0, after_caption=10):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(p, line=1.0, before=8, after=2)
    run = p.add_run()
    run.add_picture(IMG + filename, width=Inches(width))
    keep_with_next(p)
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(c, line=1.0, before=0, after=after_caption)
    r = c.add_run(caption)
    _set_font(r, size=11, italic=True)
    return c


def two_figures(doc, f1, f2, caption, width=2.6):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell, fn in zip(tbl.rows[0].cells, (f1, f2)):
        pp = cell.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _spacing(pp, line=1.0, after=0)
        pp.add_run().add_picture(IMG + fn, width=Inches(width))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(c, line=1.0, before=4, after=10)
    r = c.add_run(caption)
    _set_font(r, size=11, italic=True)


def table(doc, headers, rows, caption=None, widths=None, size=11, header_fill="DCD6FB"):
    if caption:
        c = doc.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = c.add_run(caption)
        _set_font(r, size=11, bold=True)
        _spacing(c, line=1.0, before=10, after=4)
        keep_with_next(c)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, htxt in enumerate(headers):
        shade(hdr[i], header_fill)
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _spacing(p, line=1.0, after=2, before=2)
        r = p.add_run(htxt)
        _set_font(r, size=size, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            p = cells[i].paragraphs[0]
            _spacing(p, line=1.0, after=2, before=2)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            parts = str(val).split("**")
            for j, part in enumerate(parts):
                if part == "":
                    continue
                r = p.add_run(part)
                _set_font(r, size=size, bold=(j % 2 == 1))
    # header repeats on every page; no row is split across a page
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
    for row in t.rows:
        pr = row._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit"); pr.append(cs)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    sp = doc.add_paragraph()
    _spacing(sp, line=1.0, after=0)
    return t


# ----------------------------------------------------------------- cover page
STUDENTS = [("Ishika Mittal", "Email: ______________________"),
            ("Nikhil Sharma", "Email: ______________________"),
            ("Ojasvi Garg",   "Email: ______________________")]

TITLE = "WEBTIQAI — AN AI CHATBOT WEBSITE\nFOR SMALL BUSINESSES"
COURSE = "Front End Web Development (26CA205PCB)"
SESSION = "Academic Session 2026–27"
SUPERVISOR = "Dr. Shashank Bhardwaj"
SUP_DESIG = "Associate Professor"


def cover(doc, logo=IMG + "kiet.jpeg"):
    def line(text, size, bold=True, after=0, before=0):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _spacing(p, line=1.0, before=before, after=after)
        r = p.add_run(text)
        _set_font(r, size=size, bold=bold)
        return p

    for t in TITLE.split("\n"):
        line(t, 20, after=3)
    line("A PROJECT REPORT", 14, after=6, before=40)
    line("for", 14, after=8)
    line(COURSE, 16, after=4)
    line(SESSION, 14, after=0)

    line("Submitted by", 14, after=10, before=46)
    for name, mail in STUDENTS:
        line(name, 14, after=1)
        line(mail, 12, bold=False, after=9)

    line("Master of Computer Applications (MCA)", 19, after=0, before=46)

    line("Under the Supervision of", 14, after=8, before=46)
    line(SUPERVISOR, 14, after=0)
    line(SUP_DESIG, 14, after=8)
    line("Department of Computer Applications", 16, after=0)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(p, line=1.0, before=36, after=10)
    p.add_run().add_picture(logo, width=Inches(2.99))

    line("KIET Deemed to be University", 14, after=0)
    line("Delhi-NCR, Ghaziabad, Uttar Pradesh-201206", 14, after=0)
