import lane_detection
import numpy as np


def get_lane_center(img: np.ndarray, lanes: np.ndarray):
    """
    Takes a list of lanes and returns the center of the closest lane and its slope.

        Parameters:
            img (np.ndarray): The image
            lanes (np.ndarray): The list of lanes to process.

        Returns:
            center_intercept (float): The horizontal intercept of the center of the closest lane.
            center_slope (float): The slope of the closest lane.
    """

    height, width, _ = img.shape
    center = width / 2
    closest = center - lanes[0][2]

    for lane in lanes[1:]:
        # Loop through each lane
        # => [
        #       [[x1, y1, x2, y2], slope, x-intercept],
        #       [[x1, y1, x2, y2], slope, x-intercept],
        # ]
        # Determine distance of lane from center
        # Use x-intercept, compare to current
        curr = center - lane[2]
        if abs(curr) < abs(closest):
            # It's closer
            closest = curr

    return closest


def recommend_direction(img: np.ndarray, center: float, slope: float):
    """
    Takes the center of the closest lane and its slope as inputs and returns a direction.

        Parameters:
            center (float): The center of the closest lane.
            slope (float): The slope of the closest lane.

        Returns:
            direction (float): 0 forward, - or + for left and right respectively
    """

    height, width, _ = img.shape
    lines = lane_detection.detect_lines(img)
    lanes = lane_detection.detect_lanes(img, lines)
    closest = get_lane_center(img, lanes)
    return (0.5 - closest / width) * 2
