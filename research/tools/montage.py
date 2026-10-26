import sys, os
from PIL import Image
d=sys.argv[1]; n=int(sys.argv[2]); ims=[Image.open(os.path.join(d,f'p{i}.png')) for i in range(1,n+1)]
w,h=ims[0].size; cols=4; rows=(n+cols-1)//cols
M=Image.new('RGB',(w*cols,h*rows),'white')
for i,im in enumerate(ims): M.paste(im,((i%cols)*w,(i//cols)*h))
M.save(os.path.join(d,'montage.png'))
