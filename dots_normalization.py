from extencions import Dot
from geometry_extencion import getDotProjectionOnLine, getDotProjectionOnPlane, getDistanceBetweenDots
from plane import Plane


def getNormalizedDots(dot_wrist, dot_index_mcp, dot_pinky_mcp,
                      dot_thumb, dot_index, dot_middle, dot_ring, dot_pinky):
    """Get new dot coordinates for thumb-pinky dots"""
    # Create main plain
    main_pl = Plane()
    main_pl.computePlaneCoefficientsWithThreeDots(dot_wrist, dot_index_mcp, dot_pinky_mcp)

    # Create "counter" plane to main plane
    counter_pl = Plane()
    pinky_mcp_projection = getDotProjectionOnLine(dot_pinky_mcp, dot_index_mcp, dot_wrist)
    counter_pl.computePlaneCoefficientsWithDotAndLine(dot_index_mcp, pinky_mcp_projection, dot_pinky_mcp)

    # Debug info
    print(f"Main plane: {main_pl}")
    print(f"Counter plane: {counter_pl}\n")
    # Debug info

    # Compute sign on left side of the counter_plane
    if counter_pl.getPlaneEquation(dot_pinky_mcp) >= 0:
        sign_on_left_side_of_counter_pl = 1
    else:
        sign_on_left_side_of_counter_pl = -1

    input_dots = [dot_thumb, dot_index, dot_middle, dot_ring, dot_pinky]
    output_dots = [None, None, None, None, None]

    # TODO: create class Line to store line coefficients,
    #       now they are computed 5 times in getProjectionOnLine function
    # Compute new coordinates of given dots
    for index, dot in enumerate(input_dots):
        print(f"Input dot: {dot}")

        projection_on_main_plane = getDotProjectionOnPlane(dot, main_pl)

        # Debug info
        print(f"Dot projection on plane: {projection_on_main_plane}")
        # Debug info

        projection_on_line = getDotProjectionOnLine(projection_on_main_plane, dot_index_mcp, dot_pinky_mcp)

        # Debug info
        print(f"Dot projection on line: {projection_on_line}")
        # Debug info

        x = getDistanceBetweenDots(dot_wrist, projection_on_line)

        y = getDistanceBetweenDots(projection_on_line, projection_on_main_plane)
        sign_of_x = counter_pl.getPlaneEquation(projection_on_main_plane)
        if sign_on_left_side_of_counter_pl * sign_of_x <= 0:
            y *= -1

        z = getDistanceBetweenDots(projection_on_main_plane, dot)

        output_dots[index] = Dot(x, y, z)

        # Debug info
        print(f"Output dot projection: {output_dots[index]}")
        # Debug info

    return output_dots
