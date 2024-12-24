"""
Draw various graphics
"""

from PIL import Image, ImageDraw

def icon_network(net_status=False, mqtt_status=False):
    """
    Draws a network icon based on current network and MQTT status.

    Green = Connected
    Red = Not connected
    Yellow = Unable to connect because of other errors (ie: MQTT can't connect because network is down)

    Returns a 4x4 image which can be pasted where needed.

    :param net_status: Network connection status
    :type net_status: bool
    :param mqtt_status: MQTT broker connection status
    :type mqtt_status: bool
    :return: Image
    """

    # determine the network status color based on combined network and MQTT status.
    if net_status is False:
        net_color = 'red'
        mqtt_color = 'yellow'
    elif net_status is True:
        net_color = 'green'
        if mqtt_status is False:
            mqtt_color = 'red'
        elif mqtt_status is True:
            mqtt_color = 'green'
        else:
            raise ValueError("Network Icon draw got invalid MQTT status value {}.".format(net_status))
    else:
        raise ValueError("Network Icon draw got invalid network status value {}.".format(net_status))

    x_input = 0
    y_input = 0
    img = Image.new("RGBA", (5, 5), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([x_input + 1, y_input, x_input + 3, y_input + 2], outline=mqtt_color, fill=mqtt_color)
    # Base network line.
    draw.line([x_input, y_input + 4, x_input + 4, y_input + 4], fill=net_color)
    # Network stem
    draw.line([x_input + 2, y_input + 3, x_input + 2, y_input + 4], fill=net_color)
    return img

def icon_vehicle(self, x_input=None, y_input=None):
        # Defaults because you can't reference object variables in parameters.
        # Default to lower_left.
        if x_input is None:
            x_input = 0
        if y_input is None:
            y_input = self._matrix_height

        w = self._matrix_width
        h = self._matrix_height
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw the vehicle box.

        draw.rectangle([x_input + 2, y_input, x_input + 4, y_input - 5], outline='green', fill='green')
        # Lateral sensor. Presuming one!
        draw.line([x_input + 3, y_input - 7, x_input + 3, y_input - 7],
                  fill=self._status_color()['fill'])
        # Lateral sensors.
        return img

def progress_bar(width, height, pct, progress_color='red', border=True, border_color='white'):
    """
    Draw a progress bar based on percentage of range covered.

    :param width: Width of the bar
    :type width: int
    :param height: Height of the bar
    :type height: int
    :param pct: Percentage to represent between 0 and 100.
    :type pct: int
    :param progress_color: Color of the progress bar. Any valid pillow color. Defaults to 'red'.
    :type progress_color: str
    :param border: Put a border on the bar? Uses some of the pixels so height should be at least 3! Defaults to True.
    :type border: True
    :param border_color: Color of the progress bar. Any valid pillow color. Defaults to 'white'.
    :type border_color: str
    :return: Image
    """
    # Check for input validity
    if pct > 100 or pct < 0:
        raise ValueError("RangePct must be between 0 and 100. Input was '{}'".format(pct))
    # Create our base image
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    # Create draw layer
    draw = ImageDraw.Draw(img)
    progress_pixels = int((width - 2) * (pct/100))
    print("Input Pct: {}\tProgress pixels: {}".format(pct, progress_pixels))
    # draw.line((1, height - 2, progress_pixels, height - 2), fill=progress_color, width=1)
    draw.rectangle((0, 0, progress_pixels,height - 1), fill=progress_color)
    if border:
        draw.rectangle((0, 0, width - 1, height - 1), fill=None, outline=border_color, width=1)
    return img

def rectangle_striped(width, height, pricolor='red', seccolor='yellow'):
    """
    Create a rectangle with zebra-stripes at a 45-degree angle.

    :param input_image: Image to draw onto
    :type input_image: Image
    :param width: Width in pixels
    :type width: int
    :param height: Height in pixels
    :type height: int
    :param pricolor: Primary color.
    :param seccolor: Secondary color.
    :return: Image
    """

    # Create our base image.
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    # Create a drawing object on top of our base image.
    draw = ImageDraw.Draw(img)

    # Initialize values for the loop.
    current_color = pricolor
    x_start = 0
    x_end = width
    y_start = 0
    y_end = height
    # track current column.
    current_x = x_start - (y_end - y_start)
    current_y = y_start
    while current_x <= x_end:
        line_start = [current_x, y_start]
        line_end = [current_x + (y_end - y_start), y_end]
        # Trim the lines.
        if line_start[0] < x_start:
            diff = x_start - line_start[0]
            # Move the X start to the right and the Y start down.
            line_start = [x_start, y_start + diff]
        if line_end[0] > x_end:
            diff = line_end[0] - x_end
            # Move the X start back to the left and the Y start up.
            line_end = [x_end, y_end - diff]
        draw.line([line_start[0], line_start[1], line_end[0], line_end[1]],
                  fill=current_color,
                  width=1
                  )
        # Rotate the color.
        if current_color == pricolor:
            current_color = seccolor
        else:
            current_color = pricolor
        # Increment the current X
        current_x += 1
    return img