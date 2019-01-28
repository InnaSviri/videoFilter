from pascal_voc_writer import Writer


class OutputFormer :

    def __init__(self):



# Writer(path, width, height)

writer = Writer('path/to/img.jpg', 800, 400)

# ::addObject(name, xmin, ymin, xmax, ymax)

writer.addObject('cat', 100, 100, 200, 200)

# ::save(path)

writer.save('path/to/img.xml')