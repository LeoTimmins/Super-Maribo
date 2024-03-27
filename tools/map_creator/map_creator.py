# Crate     -       (0,0,0)         #000000
# Enemy     -       (255,0,102)     #ff0066
# Myst      -       (0,255,0)       #00ff00
# Null      -       (255,255,255)   #ffffff
# Spikes    -       (66,135,245)    #4287f5
# Jumper    -       (245,120,66)    #f57842

# To do Checkpoints


print("-- Building Map -- ")
from PIL import Image
import lpf

# open image and get pixel rgba values
map_src = Image.open('tools/map_creator/map.png', 'r')
output_src = open('platform_spawn.txt', 'w')
pix_val = list(map_src.getdata())

# counts total coins in map
c_count = 0

pix_lines = []
addition_temp = []
for y in range(400):
    for x in range(400):
        if pix_val[x*400+y] == (255,255,255,255):
            addition_temp.append("Null")
        elif pix_val[x*400+y] == (0,0,0,255):
            addition_temp.append("Crate")
        elif pix_val[x*400+y] == (0,255,0,255):
            addition_temp.append("Myst")
            c_count += 1
        elif pix_val[x*400+y] == (255,0,102,255):
            addition_temp.append("Enemy")
        elif pix_val[x*400+y] == (66,135,245,255):
            addition_temp.append("Spikes")
        elif pix_val[x*400+y] == (245,120,66,255):
            addition_temp.append("Jumper")
        else:
            print(pix_val[x*400+y])
    pix_lines.append(addition_temp)
    addition_temp=[]

# Compiles to text
for line in pix_lines:
    for word in lpf.reverse(line):
        output_src.write(f"{word} ")
    output_src.write('\n')

print(f"\n-- Map Updated [{c_count}] --\n")