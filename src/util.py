"""
RGB Multitool Utility Functions
"""

import PIL

def distance_string(distance, imperial):
    """
    Format a given distance value for output.

    :param distance:
    :param imperial: Should we output in imperial units? Will be metric otherwise.
    :type: boolean
    :return: str
    """
    if imperial:
        if abs(distance.to("in").magnitude) < 12:
            distance_string = "{}\"".format(round(distance.magnitude, 1))
        else:
            feet = int(distance.to("in").magnitude // 12)
            inches = round(distance.to("in").magnitude % 12)
            distance_string = "{}'{}\"".format(feet, inches)
    else:
        range_meters = distance.to("m").magnitude
        if range_meters <= 0.5:
            distance_string = "{} cm".format(round(range_meters / 100, 2))
        else:
            distance_string = "{} m".format(round(range_meters, 2))
    return distance_string

def scale_font(text, font, w, h):
    """
    Find the largest font size for font that fix within the space of width (w) x height (h)

    :param text: String to size.
    :type: str
    :param font:
    :param w: width in pixels
    :type: int
    :param h: height in pixels
    :type: int
    :return:
    """
    # Start at font size 1.
    fontsize = 1
    while True:
        font = PIL.ImageFont.truetype(font=font, size=fontsize)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width < w and text_height < h:
            fontsize += 1
        else:
            break
    return fontsize