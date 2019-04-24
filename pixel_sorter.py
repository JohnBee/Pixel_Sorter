from PIL import Image
from math import sin, cos, pi, sqrt
from random import randrange

SETTINGS = {
    #"filename":"test.bmp",
    #"filename":"test2.png",
    "filename":"monalisa.jpg",
}

def load_image(filename):
    """
    Loads image with relevant details stored in a dictionary.
    :param filename: Name of file to load
    :return: Dictionary containing image and relevant details, returns false if file not found.
    """
    try:
        im = Image.open(filename)
        xsize, ysize = im.size
        return {"im": im, "width": xsize, "height": ysize}
    except Exception as e:
        print(e)
        return False

def save_image(im_obj, filename):
        """
        Save given image object to file.
        :param im_obj: image object
        :param filename: name of the file to save to.
        """
        im_obj.save(filename + ".bmp", "BMP")

def luminosity(r,g,b):
    return sqrt( .241 * r + .691 * g + .068 * b )

def rgb_sort(colours, reverse=False):
    """
    Sorted using RGB, order by red then green then blue.
    :param colours: list of (r, g, b) triples
    :return: returns ordered pixels
    """
    sorted_col = sorted(colours, reverse=reverse)
    return sorted_col

def do_sort(pixels, sort_func, reverse=False):
    """
    Sorted using the given function, returns sorted pixels
    :param pixels: list of dictionary where col = (r,g,b), pos = (x,y)
    :param sort_func: function to sort the colours by.
    :return: returns ordered pixels and positions
    """
    pos = [pixel["pos"] for pixel in pixels]
    col = [pixel["col"] for pixel in pixels]

    sorted_col = sort_func(col, reverse)

    #combine back to positions
    out = [{"pos":pos, "col":col} for (pos,col) in zip(pos,sorted_col)]
    return out

def pixels_angle_select(image_dic, origin, length, d_angle, wrapx=False, wrapy=False):
    """
    Gets the list of pixels and positions a long a given line using origin, angle and length.
    Wraps the pixels in the X & Y direction.
    :param image_dic: dictionary containing the image, with and height {"im": <image>, "width": <int>, "height": <int>}
    :param origin: Tuple of x & y of where to start the sort from
    :param length: length of the line of pixels to sort
    :param d_angle: angle in degrees for direction of sorting line
    :return: list of pixels and locations
    """
    # convert degrees to radians
    angle = d_angle * pi / 180
    pixels = []
    or_x, or_y = origin

    for i in range(length):
        x = or_x + i * cos(angle)
        y = or_y + i * sin(angle)

        # Wrap
        if wrapx:
            x = x % image_dic["width"]
        else:
            if x < 0 or x >= image_dic["width"]:
                break

        if wrapy:
            y = y % image_dic["height"]
        else:
            if y < 0 or y >= image_dic["height"]:
                break

        r, g, b = image_dic["im"].getpixel((x, y))
        pixels.append({"col": (r, g, b) , "pos": (x,y)})

    return pixels

def pixel_horizontal_select(image_dic, origin, length, wrap=False):
    pixels = []
    or_x, or_y = origin
    for i in range(length):
        x = or_x + i

        if wrap:
            x = x % image_dic["width"]
        else:
            if x < 0 or x >= image_dic["width"]:
                break

        r, g, b = image_dic["im"].getpixel((x, or_y))
        pixels.append({"col": (r, g, b) , "pos": (x,or_y)})

    return pixels

def pixel_vertical_select(image_dic, origin, length, wrap=False):
    pixels = []
    or_x, or_y = origin
    for i in range(length):
        y = or_y + i

        if wrap:
            y = y % image_dic["height"]
        else:
            if y < 0 or y >= image_dic["height"]:
                break

        r, g, b = image_dic["im"].getpixel((or_x, y))
        pixels.append({"col": (r, g, b) , "pos": (or_x,y)})

    return pixels


def pixels_all_select(image_dic):
    pixels = []
    for y in range(image_dic["height"]):
        for x in range(image_dic["width"]):
            r, g, b = image_dic["im"].getpixel((x, y))
            pixels.append({"col": (r, g, b) , "pos": (x,y)})
    return pixels

def get_pixels(image_dic, func, *args, **kwargs):
    """
    Use the given function with passed arguments to return the wanted pixels.
    :param image_dic: dictionary containing the image, with and height {"im": <image>, "width": <int>, "height": <int>}
    :param func: The pixel selecting function to use
    :param *args: arguments to call the given function with.
    :param **kwargs: named arguments to call the given function with.
    :return: The pixels selected by the given function and selected arguments
    """
    return func(image_dic, *args, **kwargs)

def write_pixels(image, pixels):
    """
    Write the pixels to the image object.
    :param image: image object to write the pixels to
    :param pixels: list of dictionary of pixel information of {"col": (r, g, b), "pos": (x,y)}
    :return:
    """
    image_pix = image.load()
    for pixel in pixels:
        (x,y) = pixel["pos"]
        image_pix[x,y] = pixel["col"]


if __name__ == "__main__":
    image_dic = load_image(SETTINGS["filename"])
    if image_dic:
        out_img = image_dic["im"].copy()
        length = 20
        angle = 45
        # for y in range(image_dic["height"]):
        #     for x in range(image_dic["width"]):
        #         pixels = get_pixels(image_dic, (x,y), length, angle)
        #         pixels = do_sort(pixels, rgb_sort)
        #         write_pixels(out_img, pixels)
        x = 0
        y = 0
        length = 10
        for y in range(image_dic["width"]):
            pixels = pixel_vertical_select(image_dic,(y,0),image_dic["height"])
            pixels = do_sort(pixels, rgb_sort,reverse=True)
            write_pixels(out_img, pixels)
        save_image(out_img, "output")
