# import EAN13 from barcode module


# import ImageWriter to generate an image file
from barcode.writer import ImageWriter

# Make sure to pass the number as string
number = '5901234123457'

import random
import barcode
from barcode.writer import ImageWriter
from barcode import EAN13
# Now, let's create an object of EAN13 class and
# pass the number with the ImageWriter() as the
# writer

# Barcode list
barcode_list = []
barcode_images = []

# Generate 10 barcodes
for i in range(10):
    code = str(random.randint(100000000000, 999999999999))  # 12-digit number
    barcode_list.append(code)

    # Generate barcode image
    ean = barcode.get('ean13', code, writer=ImageWriter())
    image_path = f'brcode/barcode_{i}'
    ean.save(image_path)
    barcode_images.append(image_path)
#
# my_code = EAN13(number, writer=ImageWriter())

# # Our barcode is ready. Let's save it.
# my_code.save("new_code1")
