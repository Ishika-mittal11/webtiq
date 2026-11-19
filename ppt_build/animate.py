"""
Inject PowerPoint entrance animations + slide transitions into a .pptx.

pptxgenjs cannot write animations, so we add the <p:timing> tree ourselves.

Shape naming convention written by deck.js:
    <effect>_<group>__<part>
      effect : fade | fly | zoom | wipe
      group  : shapes sharing a group animate together
    names starting with "bg" are never animated

Every slide auto-plays its sequence on entry, staggered.
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "WebtiqAI_Presentation.pptx")
UNPACK = Path("unpacked")

DUR = 500           # effect duration, ms
STAGGER = 150       # gap between groups, ms
EFFECTS = {"fade", "fly", "zoom", "wipe"}


# ---------------------------------------------------------------- XML pieces
def _set_visible(cid, spid):
    return (
        f'<p:set><p:cBhvr><p:cTn id="{cid}" dur="1" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
    )


def _anim_effect(cid, spid, filt="fade"):
    return (
        f'<p:animEffect transition="in" filter="{filt}">'
        f'<p:cBhvr><p:cTn id="{cid}" dur="{DUR}"/>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
    )


def _anim_attr(cid, spid, attr, frm, to):
    return (
        f'<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">'
        f'<p:cTn id="{cid}" dur="{DUR}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr>'
        f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="{frm}"/></p:val></p:tav>'
        f'<p:tav tm="100000"><p:val><p:strVal val="{to}"/></p:val></p:tav></p:tavLst></p:anim>'
    )


def _anim_attr_num(cid, spid, attr, frm_val, to):
    return (
        f'<p:anim calcmode="lin" valueType="num"><p:cBhvr>'
        f'<p:cTn id="{cid}" dur="{DUR}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr>'
        f'<p:tavLst><p:tav tm="0"><p:val><p:fltVal val="{frm_val}"/></p:val></p:tav>'
        f'<p:tav tm="100000"><p:val><p:strVal val="{to}"/></p:val></p:tav></p:tavLst></p:anim>'
    )


def build_effect(effect, spids, delay, node_type, next_id):
    """One <p:par> holding every shape of a group, as one entrance effect."""
    cid = next_id[0]; next_id[0] += 1

    if effect == "fly":          # Float In (up) - fade plus a small rise
        preset, subtype = 42, 4
    elif effect == "zoom":       # Grow / Zoom in
        preset, subtype = 23, 16
    elif effect == "wipe":       # Wipe from bottom
        preset, subtype = 22, 4
    else:                        # Fade
        preset, subtype = 10, 0

    body = []
    for spid in spids:
        body.append(_set_visible(next_id[0], spid)); next_id[0] += 1

        if effect == "fade":
            body.append(_anim_effect(next_id[0], spid)); next_id[0] += 1
        elif effect == "wipe":
            body.append(_anim_effect(next_id[0], spid, "wipe(up)")); next_id[0] += 1
        elif effect == "fly":
            body.append(_anim_effect(next_id[0], spid)); next_id[0] += 1
            body.append(_anim_attr(next_id[0], spid, "ppt_y", "#ppt_y+0.07", "#ppt_y"))
            next_id[0] += 1
        elif effect == "zoom":
            body.append(_anim_effect(next_id[0], spid)); next_id[0] += 1
            body.append(_anim_attr_num(next_id[0], spid, "ppt_w", "0.6", "#ppt_w"))
            next_id[0] += 1
            body.append(_anim_attr_num(next_id[0], spid, "ppt_h", "0.6", "#ppt_h"))
            next_id[0] += 1

    return (
        f'<p:par><p:cTn id="{cid}" presetID="{preset}" presetClass="entr" '
        f'presetSubtype="{subtype}" fill="hold" nodeType="{node_type}">'
        f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>'
        f'<p:childTnLst>{"".join(body)}</p:childTnLst></p:cTn></p:par>'
    )


def build_timing(groups):
    """groups: ordered list of (effect, [spid, ...])"""
    if not groups:
        return ""
    next_id = [5]
    pars = []
    for i, (effect, spids) in enumerate(groups):
        pars.append(
            build_effect(effect, spids, i * STAGGER,
                         "afterEffect" if i == 0 else "withEffect", next_id)
        )
    return (
        '<p:timing><p:tnLst><p:par>'
        '<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
        '<p:seq concurrent="1" nextAc="seek">'
        '<p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
        '<p:par><p:cTn id="3" fill="hold"><p:stCondLst>'
        '<p:cond delay="indefinite"/>'
        '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>'
        '</p:stCondLst><p:childTnLst>'
        '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:childTnLst>{"".join(pars)}</p:childTnLst>'
        '</p:cTn></p:par>'
        '</p:childTnLst></p:cTn></p:par>'
        '</p:childTnLst></p:cTn>'
        '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
    )


# ---------------------------------------------------------------- main
def plan_slide(xml):
    """Return ordered [(effect, [spids])] from the shape names on the slide."""
    tree = xml.split("<p:spTree>", 1)[1]
    found = re.findall(r'<p:cNvPr id="(\d+)" name="([^"]*)"', tree)

    order, groups = [], {}
    for spid, name in found:
        if spid == "1" and name == "":
            continue                      # the spTree group shape itself
        if name.lower().startswith("bg"):
            continue
        key = name.split("__")[0] if name else f"anon{spid}"
        head = key.split("_")[0]
        effect = head if head in EFFECTS else "fade"
        if key not in groups:
            groups[key] = (effect, [])
            order.append(key)
        groups[key][1].append(spid)

    return [groups[k] for k in order]


def main():
    if UNPACK.exists():
        shutil.rmtree(UNPACK)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(UNPACK)

    slides = sorted(
        (UNPACK / "ppt" / "slides").glob("slide*.xml"),
        key=lambda p: int(re.search(r"\d+", p.name).group()),
    )

    for path in slides:
        xml = path.read_text(encoding="utf-8")
        if "<p:timing>" in xml:
            continue

        groups = plan_slide(xml)
        timing = build_timing(groups)
        transition = '<p:transition spd="med"><p:fade/></p:transition>'

        xml = xml.replace("</p:sld>", transition + timing + "</p:sld>")
        path.write_text(xml, encoding="utf-8")
        print(f"{path.name}: {len(groups)} animation groups")

    out = Path("animated.pptx")
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(UNPACK.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(UNPACK).as_posix())
    print("wrote", out)


if __name__ == "__main__":
    main()
