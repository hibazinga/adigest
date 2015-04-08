import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
#font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf",25)
img=Image.new("RGBA", (200,200),(0,0,0))
draw = ImageDraw.Draw(img)
draw.text((100, 100),"This is a test",(255,255,0))
draw = ImageDraw.Draw(img)
draw = ImageDraw.Draw(img)
img.save("a_test.png")
