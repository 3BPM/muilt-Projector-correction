import cv2
import numpy as np




def get_max_inscribed_rect(src, contour):
    max_inscribed_rect = (0, 0, 0, 0)
    empty_rect = (0, 0, 0, 0)
    all_rect = []
    all_point = list(contour.reshape(-1, 2))

    for i in range(len(contour)):
        for j in range(i + 1, len(contour)):
            p1 = tuple(contour[i][0])
            p2 = tuple(contour[j][0])
            if p1[1] == p2[1] or p1[0] == p2[0]:
                continue
            temp_rect = from_two_points(p1, p2)
            all_point.extend(get_all_corners(temp_rect))
            for rect in all_rect:
                intersect_r = rect_intersect(temp_rect, rect)
                if intersect_r != empty_rect:
                    all_point.extend(get_all_corners(intersect_r))
            all_rect.append(temp_rect)

    distinct_points = all_point
    for i in range(len(distinct_points)):
        for j in range(i + 1, len(distinct_points)):
            temp_rect = from_two_points(distinct_points[i], distinct_points[j])
            if not contain_points(contour, get_all_corners(temp_rect)) or contains_any_pt(temp_rect, contour):
                continue
            cv2.rectangle(src, temp_rect, (0, 255, 0), 2)
            if temp_rect[2] * temp_rect[3] > max_inscribed_rect[2] * max_inscribed_rect[3]:
                max_inscribed_rect = temp_rect

    cv2.rectangle(src, max_inscribed_rect, (0, 255, 255), 2)
    return cv2.boundingRect(contour) if max_inscribed_rect == empty_rect else max_inscribed_rect


def from_two_points(p1, p2):
    if p1[0] == p2[0] or p1[1] == p2[1]:
        return (0, 0, 0, 0)

    x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
    x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
    return (x1, y1, x2 - x1, y2 - y1)

def rect_intersect(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    xi1, yi1 = max(x1, x2), max(y1, y2)
    xi2, yi2 = min(x1 + w1, x2 + w2), min(y1 + h1, y2 + h2)
    if xi1 < xi2 and yi1 < yi2:
        return (xi1, yi1, xi2 - xi1, yi2 - yi1)
    return (0, 0, 0, 0)

def contain_points(contour, points):
    for point in points:
        if cv2.pointPolygonTest(contour, point, False) < 0:
            return False
    return True

def contains_any_pt(rect, points):
    x, y, w, h = rect
    for point in points:
        if x < point[0] < x + w and y < point[1] < y + h:
            return True
    return False
def get_all_corners(rect):
    x, y, w, h = rect
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

def contain_point(contour, p1):
    return cv2.pointPolygonTest(contour, p1, False) > 0

def contain_points(contour, points):
    for point in points:
        if cv2.pointPolygonTest(contour, point, False) < 0:
            return False
    return True
def draw_contour(mat, contour, color, thickness):
    for i in range(len(contour)):
        if i + 1 < len(contour):
            cv2.line(mat, tuple(contour[i][0]), tuple(contour[i+1][0]), color, thickness)

# src = cv2.imread(r"C:\Users\robert\Desktop\muilt-Projector-correction\data\aruco1.png", cv2.IMREAD_COLOR)
# dst = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
# dst = cv2.Canny(dst, 10, 70)
# # r.cv_show("haha",dst)
# contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# approx_contours = []
# for contour in contours:
#     approx_contour = cv2.approxPolyDP(contour, 20, True)
#     approx_contours.append(approx_contour)
#     draw_contour(src, approx_contour, (255, 255, 255), 1)

# for contour in approx_contours:
#     get_max_inscribed_rect(src, contour)

# cv2.imshow("src", src)
# cv2.waitKey(0)
