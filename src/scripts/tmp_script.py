import json

# SVG 1: Product and Coproduct (700x340)
svg1 = open('/tmp/svg1.xml').read()

# SVG 2: Semiring table (680x280)
svg2 = open('/tmp/svg2.xml').read()

# SVG 3: Zipper (680x220)
svg3 = open('/tmp/svg3.xml').read()

with open('/home/jovyan/src/ta_product_coproduct.svg', 'w') as f:
    f.write(svg1)
print('Written ta_product_coproduct.svg')

with open('/home/jovyan/src/ta_semiring.svg', 'w') as f:
    f.write(svg2)
print('Written ta_semiring.svg')

with open('/home/jovyan/src/ta_zipper.svg', 'w') as f:
    f.write(svg3)
print('Written ta_zipper.svg')
print('Done!')
