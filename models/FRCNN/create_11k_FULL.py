import os
from decimal import Decimal

import numpy as np
import math

from numpy.linalg import lstsq, norm


# -------------------------------------------------
# TODO:  hand will be considered to be all DORSAL from the LEFT hand
# TODO: from PINKY to THUMB from LEFT to RIGHT
# -------------------------------------------------

# TODO: add to not make the code crash if no boxes are found
# return (x,y) for the center of the box
def box_center(minx, maxx, miny, maxy):
    return (minx + maxx) / 2, (miny + maxy) / 2


def order_dict(dict):
    keys = list(dict.keys())
    keys.sort()
    dict = {i: dict[i] for i in keys}
    return dict


def create_dict(dict, part):
    dict = order_dict(dict)
    annotated_dict = {}
    ct = 0
    keys = dict.keys()

    if part == 'fingers':
        for el in keys:

            if ct == 5:
                break
            annotated_dict[ct + 1] = dict[el]
            ct += 1

    return annotated_dict


def distance_from_point_to_line(x0, y0, A, B, C):
    return abs(A * x0 + B * y0 + C) / math.sqrt(A ** 2 + B ** 2)


def box_distance(box1, box2):
    # Unpack the coordinates
    x1_min, x1_max, y1_min, y1_max = box1
    x2_min, x2_max, y2_min, y2_max = box2

    # Calculate horizontal and vertical distances
    if x1_max < x2_min:  # box1 is to the left of box2
        x_dist = x2_min - x1_max
    elif x2_max < x1_min:  # box1 is to the right of box2
        x_dist = x1_min - x2_max
    else:  # boxes overlap or are aligned vertically
        x_dist = 0

    if y1_max < y2_min:  # box1 is above box2
        y_dist = y2_min - y1_max
    elif y2_max < y1_min:  # box1 is below box2
        y_dist = y1_min - y2_max
    else:  # boxes overlap or are aligned horizontally
        y_dist = 0

    # Calculate the Euclidean distance
    distance = (x_dist ** 2 + y_dist ** 2) ** 0.5
    return distance


def calculate_angle(point1, point2):
    # Unpack the points
    x1, y1 = point1
    x2, y2 = point2

    delta_x = x2 - x1
    delta_y = y2 - y1

    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)

    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees


# calculate the distance from p3 to the line formed by p1 and p2
def distance_from_point_to_line(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
    return d


def set_major_knuckles(major_knuckles, fingernails, minor_knuckles):
    major_knuckles = order_dict(major_knuckles)
    finger_keys = list(fingernails.keys())
    final_dict = {1: None, 2: None, 3: None, 4: None, 5: None}
    major_knuckles_keys = list(major_knuckles.keys())

    print(major_knuckles_keys)

    for major_knuckle in major_knuckles_keys:

        if (final_dict[1] is not None and final_dict[2] is not None
                and final_dict[3] is not None and final_dict[4] is not None):
            break

        m_point = box_center(major_knuckles[major_knuckle][0], major_knuckles[major_knuckle][2],
                             major_knuckles[major_knuckle][1], major_knuckles[major_knuckle][3])

        min_distance = float('inf')
        closest_finger = None

        try:
            for finger_counter in finger_keys[:-1]:
                finger_coord = fingernails[finger_counter]
                minor_knuckle_coord = minor_knuckles[finger_counter]

                point1 = box_center(finger_coord[0], finger_coord[2], finger_coord[1], finger_coord[3])
                point2 = box_center(minor_knuckle_coord[0], minor_knuckle_coord[2], minor_knuckle_coord[1],
                                    minor_knuckle_coord[3])

                distance = distance_from_point_to_line(point1, point2, m_point)

                if distance < min_distance:
                    min_distance = distance
                    closest_finger = finger_counter

            final_dict[closest_finger] = major_knuckles[major_knuckle]
            finger_keys.remove(closest_finger)
        except:
            continue

    thumb_distance = float('inf')
    if len(finger_keys) < 1:
        return final_dict

    for finger in finger_keys:
        finger_coord = fingernails[finger]
        p1 = box_center(finger_coord[0], finger_coord[2], finger_coord[1], finger_coord[3])
        for knuckle_key in major_knuckles_keys:
            knuckle_coord = major_knuckles[knuckle_key]
            p2 = box_center(knuckle_coord[0], knuckle_coord[2], knuckle_coord[1], knuckle_coord[3])
            distance = math.dist(p1, p2)
            if distance < thumb_distance:
                thumb_distance = distance
                final_dict[5] = knuckle_coord

    return final_dict


def set_base_knuckles(base_knuckles, fingernails, major_knuckles):
    final_dict = {1: None, 2: None, 3: None, 4: None, 5: None}
    finger_keys = list(fingernails.keys())
    major_knuckles_keys = list(major_knuckles.keys())
    base_knuckles_keys = list(base_knuckles.keys())

    for base_knuckle in base_knuckles_keys:

        try:
            m_point = box_center(base_knuckles[base_knuckle][0], base_knuckles[base_knuckle][2],
                                 base_knuckles[base_knuckle][1], base_knuckles[base_knuckle][3])

            min_distance = float('inf')
            closest_finger = None

            for finger_counter in finger_keys:
                finger_coord = fingernails[finger_counter]
                major_knuckle_coord = major_knuckles[finger_counter]

                point1 = box_center(finger_coord[0], finger_coord[2], finger_coord[1], finger_coord[3])
                point2 = box_center(major_knuckle_coord[0], major_knuckle_coord[2], major_knuckle_coord[1],
                                    major_knuckle_coord[3])

                distance = distance_from_point_to_line(point1, point2, m_point)

                if distance < min_distance:
                    min_distance = distance
                    closest_finger = finger_counter

            final_dict[closest_finger] = base_knuckles[base_knuckle]
            finger_keys.remove(closest_finger)

        except:
            continue

    return final_dict


def set_minor_knuckles(knuckles, fingers):
    final_dict = {}
    finger_keys = list(fingers.keys())
    knuckle_keys = list(knuckles.keys())

    for finger in finger_keys[:-1]:
        last_smallest_distance = float('inf')
        f_x = (fingers[finger][0] + fingers[finger][2]) / 2
        closest_box = []
        closest_knuckle = None
        for knuckle in knuckle_keys:
            k_x = (knuckles[knuckle][0] + knuckles[knuckle][2]) / 2
            distance = abs(f_x - k_x)
            if distance < last_smallest_distance:
                last_smallest_distance = distance
                closest_box = knuckles[knuckle]
                closest_knuckle = knuckle
        knuckle_keys.remove(closest_knuckle)
        final_dict[finger] = closest_box

    try:
        del final_dict[5]
    except KeyError:
        pass

    for i in range(1, 6):
        if i not in final_dict.keys():
            final_dict[i] = None

    return final_dict


def set_lunules(lunules, fingers):
    final_dict = {1: None, 2: None, 3: None, 4: None, 5: None}
    for lunule in lunules.keys():
        last_smallest_distance = float('inf')
        closest_box = []
        closest_finger = None
        for finger in fingers.keys():
            distance = box_distance(lunules[lunule], fingers[finger])
            if distance < last_smallest_distance:
                last_smallest_distance = distance
                closest_box = lunules[lunule]
                closest_finger = finger
        final_dict[closest_finger] = closest_box

    for i in range(1, 6):
        if i not in final_dict.keys():
            final_dict[i] = None

    return final_dict


def get_per_finger_in_order(output_dict):
    new_dict = {}
    ct = 1
    for key in output_dict.keys():
        new_dict[ct] = output_dict[key]
        ct += 1
    return new_dict


def annotate_flk_results(output_dict):
    fingers = {}
    lunules = {}
    knuckles_major = {}
    knuckles_minor = {}
    knuckles_base = {}

    for hand_part in output_dict.keys():
        for box in output_dict[hand_part]:

            x_center, y_center = box_center(box[0], box[2], box[1], box[3])

            if hand_part == '1':
                fingers[x_center] = box
            elif hand_part == '2':
                lunules[x_center] = box
            elif hand_part == '4':
                knuckles_major[x_center] = box
            elif hand_part == '3':
                knuckles_minor[x_center] = box
            elif hand_part == '5':
                knuckles_base[x_center] = box

    # print('fingers: ', fingers)

    # sort the dictionaries by the keys
    fingers = create_dict(fingers, "fingers")

    print('fingers: ', fingers)
    # print('-----------------')

    if fingers == {}:
        print('NO FINGERS FOUND')
        dictionary = {'f1': None, 'f2': None, 'f3': None, 'f4': None, 'f5': None,
                      'l1': None, 'l2': None, 'l3': None, 'l4': None, 'l5': None,
                      'k_m1': None, 'k_m2': None, 'k_m3': None, 'k_m4': None, 'k_m5': None,
                      "k_M1": None, "k_M2": None, "k_M3": None, "k_M4": None, "k_M5": None,
                      'k_b1': None, 'k_b2': None, 'k_b3': None, 'k_b4': None, 'k_b5': None}
        fingers = {1: None, 2: None, 3: None, 4: None, 5: None}
        angles = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        return dictionary, fingers, angles

    for i in range(1, 6):
        if i not in fingers.keys():
            fingers[i] = None

    # try:
    #     lunules = set_lunules(lunules, fingers)
    # except:
    lunules = {1: None, 2: None, 3: None, 4: None, 5: None}

    try:
        knuckles_minor = set_minor_knuckles(order_dict(knuckles_minor), fingers)
    except:
        try:
            knuckles_minor = get_per_finger_in_order(order_dict(knuckles_minor))
            if 5 in knuckles_minor.keys():
                del knuckles_minor[5]
            for i in range(1, 5):
                if i not in knuckles_minor.keys():
                    knuckles_minor[i] = None
            print('knuckles_minor: ', knuckles_minor)
        except:
            knuckles_minor = {1: None, 2: None, 3: None, 4: None}

    try:
        knuckles_major = set_major_knuckles(knuckles_major, fingers, knuckles_minor)
    except:
        try:
            knuckles_major = get_per_finger_in_order(order_dict(knuckles_major))
            for i in range(1, 6):
                if i not in knuckles_major.keys():
                    knuckles_major[i] = None
        except:
            knuckles_major = {1: None, 2: None, 3: None, 4: None, 5: None}

    try:
        knuckles_base = set_base_knuckles(knuckles_base, fingers, knuckles_major)
    except:
        try:
            knuckles_base = get_per_finger_in_order(order_dict(knuckles_base))
            for i in range(1, 6):
                if i not in knuckles_base.keys():
                    knuckles_base[i] = None
        except:
            knuckles_base = {1: None, 2: None, 3: None, 4: None, 5: None}

    angle_dict = {}

    # for finger in fingers.keys():
    #     if fingers[finger] is not None:
    #         if knuckles_major[finger] is not None:
    #             angle_dict[finger] = 90 + calculate_angle(box_center(fingers[finger][0], fingers[finger][2], fingers[finger][1], fingers[finger][3]),
    #                                              box_center(knuckles_major[finger][0], knuckles_major[finger][2], knuckles_major[finger][1], knuckles_major[finger][3]))
    #         elif knuckles_base[finger] is not None:
    #             angle_dict[finger] = 90 + calculate_angle(box_center(fingers[finger][0], fingers[finger][2], fingers[finger][1], fingers[finger][3]),
    #                                              box_center(knuckles_base[finger][0], knuckles_base[finger][2], knuckles_base[finger][1], knuckles_base[finger][3]))
    #         else:
    #             angle_dict[finger] = 0
    #     else:
    #         angle_dict[finger] = 0

    # for finger in range(1, 5):
    #     if knuckles_minor[finger] is not None:
    #             angle_dict[finger] = 90 + calculate_angle(box_center(fingers[finger][0], fingers[finger][2], fingers[finger][1], fingers[finger][3]),
    #                                              box_center(knuckles_minor[finger][0], knuckles_minor[finger][2], knuckles_minor[finger][1], knuckles_minor[finger][3]))

    #     else:
    #         angle_dict[finger] = 0

    # print('angle_dict: ', angle_dict)

    dict = {'f1': fingers[1],
            'f2': fingers[2],
            'f3': fingers[3],
            'f4': fingers[4],
            'f5': fingers[5],
            'l1': lunules[1],
            'l2': lunules[2],
            'l3': lunules[3],
            'l4': lunules[4],
            'l5': lunules[5],
            'k_m1': knuckles_minor[1],
            'k_m2': knuckles_minor[2],
            'k_m3': knuckles_minor[3],
            'k_m4': knuckles_minor[4],
            'k_M1': knuckles_major[1],
            'k_M2': knuckles_major[2],
            'k_M3': knuckles_major[3],
            'k_M4': knuckles_major[4],
            'k_M5': knuckles_major[5],
            'k_b1': knuckles_base[1],
            'k_b2': knuckles_base[2],
            'k_b3': knuckles_base[3],
            'k_b4': knuckles_base[4],
            'k_b5': knuckles_base[5]
            }

    return dict, fingers, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
















