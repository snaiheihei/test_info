'''
from PIL import Image, ImageFilter, ImageOps
img = Image.open('01.jpg')
def dodge(a, b, alpha):
    return min(int(a*255/(256-b*alpha)), 255)
def draw(img, blur=25, alpha=1.0):
    img1 = img.convert('L')        #图片转换成灰色
    img2 = img1.copy()
    img2 = ImageOps.invert(img2)
    for i in range(blur):          #模糊度
        img2 = img2.filter(ImageFilter.BLUR)
    width, height = img1.size
    for x in range(width):
        for y in range(height):
            a = img1.getpixel((x, y))
            b = img2.getpixel((x, y))
            img1.putpixel((x, y), dodge(a, b, alpha))
    img1.save('2.png')
draw(img)

'''

from PIL import Image
import os
 
image = "01.jpg"
img = Image.open(image)
img_all =  "03.jpg"
new = Image.new("L", img.size, 255)
width, height = img.size
img = img.convert("L") 
# 定义画笔的大小
Pen_size = 3
# 色差扩散器
Color_Diff = 6
for i in range(Pen_size + 1, width - Pen_size - 1):
    for j in range(Pen_size + 1, height - Pen_size - 1):
        # 原始的颜色
        originalColor = 255
        lcolor = sum([img.getpixel((i - r, j)) for r in range(Pen_size)]) // Pen_size
        rcolor = sum([img.getpixel((i + r, j)) for r in range(Pen_size)]) // Pen_size
 
        # 通道----颜料
        if abs(lcolor - rcolor) > Color_Diff:
            originalColor -= (255 - img.getpixel((i, j))) // 4
            new.putpixel((i, j), originalColor)
 
        ucolor = sum([img.getpixel((i, j - r)) for r in range(Pen_size)]) // Pen_size
        dcolor = sum([img.getpixel((i, j + r)) for r in range(Pen_size)]) // Pen_size
 
        # 通道----颜料
        if abs(ucolor - dcolor) > Color_Diff:
            originalColor -= (255 - img.getpixel((i, j))) // 4
            new.putpixel((i, j), originalColor)
 
        acolor = sum([img.getpixel((i - r, j - r)) for r in range(Pen_size)]) // Pen_size
        bcolor = sum([img.getpixel((i + r, j + r)) for r in range(Pen_size)]) // Pen_size
 
        # 通道----颜料
        if abs(acolor - bcolor) > Color_Diff:
            originalColor -= (255 - img.getpixel((i, j))) // 4
            new.putpixel((i, j), originalColor)
 
        qcolor = sum([img.getpixel((i + r, j - r)) for r in range(Pen_size)]) // Pen_size
        wcolor = sum([img.getpixel((i - r, j + r)) for r in range(Pen_size)]) // Pen_size
 
        # 通道----颜料
        if abs(qcolor - wcolor) > Color_Diff:
            originalColor -= (255 - img.getpixel((i, j))) // 4
            new.putpixel((i, j), originalColor)
 
new.save(img_all)
 
i = os.system('mshta vbscript createobject("sapi.spvoice").speak("%s")(window.close)' % '您的图片转换好了')
os.system(img_all)  



# img = Image.open('01.jpg')

# img1 = img.convert('L')
# img1.show()






