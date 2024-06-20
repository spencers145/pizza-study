from matplotlib import axes, pyplot

def addHorizontalForkedLabel(
        axes: axes.Axes, 
        text: str, text_offset: float,
        source_x: float, x_offset: float,
        min_y: float, max_y: float,
        direction = "right", color = "black", text_nudge = (0, 0)
    ):
    match direction:
        case "right": pass
        case "left":
            x_offset *= -1
            text_offset *= -1
    center_y = (max_y + min_y)/2
    boundary_x = source_x + x_offset
    axes.text(source_x + text_offset + text_nudge[0], center_y + text_nudge[1], text, color = color)
    axes.add_line(pyplot.Line2D([boundary_x, source_x + text_offset], [center_y, center_y], color = color))
    axes.add_line(pyplot.Line2D([boundary_x, boundary_x], [min_y, max_y], color = color))
    axes.add_line(pyplot.Line2D([boundary_x - x_offset/4, boundary_x], [min_y, min_y], color = color))
    axes.add_line(pyplot.Line2D([boundary_x - x_offset/4, boundary_x], [max_y, max_y], color = color))
    return axes
    