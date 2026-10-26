import fitz, sys, os
pdf=sys.argv[1]; out=sys.argv[2]; os.makedirs(out,exist_ok=True)
d=fitz.open(pdf)
for i,pg in enumerate(d):
    txt=pg.get_text()
    flag=[w for w in ('References','Use of Generative AI','Discussion and Limitations','Conclusion','Table 1.','Table 2.','Figure 1.','Figure 2.') if w in txt]
    print(i+1,flag)
    pix=pg.get_pixmap(dpi=70); pix.save(os.path.join(out,f'p{i+1}.png'))
