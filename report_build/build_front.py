from doclib import *
doc = new_doc()
s = doc.sections[0]
s.top_margin = Inches(0.62); s.bottom_margin = Inches(0.5)
s.left_margin = Inches(1.0); s.right_margin = Inches(1.0)
cover(doc)
doc.save("WebtiqAI_Front_Page.docx")
print("saved")
