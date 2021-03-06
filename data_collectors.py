"""
This script contains the functions used to collect data on the polarization
and spatial extent of the shoal. These are collected ONLY on the fish agents,
not any obstructions. The data collected are, currently:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal Area: convex hull
    4. Mean Distance From Centroid
    6. Positions of each of the fish in the shoal
    5. Center of mass of the shoal. This is calculated separately because the
       data structure for this function is different from the output needed for
       the positions of the fish.

From Herbert-Read et al. (2017) Anthropogenic noise pollution from pile-driving
disrupts the structure and dynamics of fish shoals.
    5. "Distance from each fish to its nearest-neighbour perpendicular to their
       direction of travel (i.e. how far apart side-by-side) and...
    6. parallel to their direction of travel (i.e. how far apart in front-or-
       behind one another)."
    7. "Bearing angle to a fish's nearest neighbour, which represents the
       direction that a neighbour was most likely to be found in relation to
       the focal individual."
    8. "The heading difference between neighbours, i.e. the angle between the
       direction nearest neighbours were fishing" - directional organization

More functions will be added as more methods for conceptualizing the shoal are
found in the literature.

These are used in shoal_model.py and elsewhere.
"""

import numpy as np
import math
import itertools
from scipy.spatial import KDTree, ConvexHull
from scipy.ndimage import center_of_mass
from statsmodels.robust.scale import mad


def test(model):
    """
    Data collector for testing whether the model is generating agents correctly.
    """
    fish = [agent.pos for agent in model.schedule.agents if agent.tag == "fish"]
    obstruct = [agent.pos for agent in model.schedule.agents if agent.tag == "obstruct"]
    return fish, obstruct


def polar(model):
    """
    Computes median absolute deviation (MAD) from the mean velocity of the
    group. As the value approaches 0, polarization increases.
    To find the MAD, the x,y coordinates are converted to radians by finding
    the arc tangent of y/x. The function used pays attention to the sign of
    the input to make sure that the correct quadrant for the angle is determined.

    Collects velocity from ONLY the agents tagged as "fish".
    """
    velocity_x = [agent.velocity[0] for agent in model.schedule.agents
                  if agent.tag == "fish"]
    velocity_y = [agent.velocity[1] for agent in model.schedule.agents
                  if agent.tag == "fish"]
    angle = []
    for (y, x) in zip(velocity_y, velocity_x):
        a = math.atan2(y, x)
        angle.append(a)
    return mad(np.asarray(angle), center=np.median)


def nnd(model):
    """
    Computes the average nearest neighbour distance for each agent as another
    measure of cohesion. Method finds & averages the nearest neighbours
    using a KDTree, a machine learning concept for clustering or
    compartmentalizing data. Right now, the 5 nearest neighbors are considered.

    Collects position from ONLY the agents tagged as "fish".
    """
    fish = np.asarray([agent.pos for agent in model.schedule.agents
                       if agent.tag == "fish"])
    fish_tree = KDTree(fish)
    means = []
    for me in fish:
        neighbours = fish_tree.query(x=me, k=6)  # includes agent @ dist = 0
        dist = list(neighbours[0])  # select dist from .query output
        dist.pop(0)  # removes closest agent - itself @ dist = 0
        means.append(sum(dist) / len(dist))
    return sum(means) / len(means)


def area(model):
    """
    Computes convex hull (smallest convex set that contains all points) as a
    measure of shoal area. Uses the area variable from the scipy.spatial
    ConvexHull function.

    Collects position from ONLY the agents tagged as "fish".
    """
    # Data needs to be a numpy array of floats - two columns (x,y)
    pos_x = np.asarray([agent.pos[0] for agent in model.schedule.agents
                        if agent.tag == "fish"])
    pos_y = np.asarray([agent.pos[1] for agent in model.schedule.agents
                        if agent.tag == "fish"])
    return ConvexHull(np.column_stack((pos_x, pos_y))).area


def centroid_dist(model):
    """
    Extracts xy coordinates for each agent, finds the centroid, and then
    calculates the mean distance of each agent from the centroid.

    Collects position from ONLY the agents tagged as "fish".
    """
    pos_x = np.asarray([agent.pos[0] for agent in model.schedule.agents
                        if agent.tag == "fish"])
    pos_y = np.asarray([agent.pos[1] for agent in model.schedule.agents
                        if agent.tag == "fish"])
    mean_x, mean_y = np.mean(pos_x), np.mean(pos_y)
    centroid = (mean_x, mean_y)
    pos = [agent.pos for agent in model.schedule.agents]
    cent_dist = []
    for p in pos:
        dist = model.space.get_distance(p, centroid)
        cent_dist = np.append(cent_dist, dist)
    return np.mean(cent_dist)


def positions(model):
    """ Extracts xy coordinates for each agent tagged as "fish"."""
    pos = [(agent.pos[0], 50-agent.pos[1]) for agent in model.schedule.agents
           if agent.tag == "fish"]
    pos = list(itertools.chain(*pos))  # creates lists of positions, rather than tuples
    return pos


def heading(model):
    """
    Extracts heading of each agent tagged as "fish". Heading is determined from
    velocity in the agent creation, even though there's no movement element The
    velocity is a tuple - (x, y), here transformed into radians here..
    """
    head = [agent.velocity for agent in model.schedule.agents
            if agent.tag == "fish"]
    degrees = [math.atan2(x, -y) for (x, y) in head]  # from x,y to radians with y inverted
    return degrees


def center_mass(model):
    """
    Calculates the center of mass of the shoal. Same as the centroid when the
    body has a uniform density. Calculated with the scipy.ndimage.center_of_mass
    function.
    """
    pos = np.asarray([agent.pos for agent in model.schedule.agents
                      if agent.tag == "fish"])
    center = center_of_mass(pos)
    return np.asarray(center)


def nn_perp_d(model):
    """
    Mean nearest neighbour distance perpendicular to the direction of travel,
    i.e. how far a part the fish are, side to side.
    """


def nn_para_d(model):
    """
    Mean nearest neighbour distance parallel to the direction of travel, i.e.
    how far apart the fish are in front or behind each other.
    """


def nn_bearing(model):
    """
    Mean bearing angle to a fish's nearest neighbour. 90 degrees = a neighbour
    directly to the side of the focal fish. 0 degrees = neighbour directly
    ahead; 180 = neighbour directly behind.
    """


def heading_diff(model):
    """
    Mean heading difference between nearest neighbours as a measure of
    alignment. 0 degrees = high alignment; 180 = opposite alignment.
    """
