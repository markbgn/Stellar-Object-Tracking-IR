import cv2
import numpy as np

TRESHHOLD = 0.85  # Treshold for object location. Any smaller match is rejected.
LENVIEW = 100  # Camera lens' angle of view in degrees

observerMode = False # If True, every result will be displayed with pictures.
showMatchingResult = True  # If True template matching result weill be displayed

im = cv2.imread('sky.jpg')  # This is the current photo of the night sky
picw = im.shape[1]  # Width of picture for mapping
pich = im.shape[0]  # Height of picture for mapping


# Returns with the location of the object
def GetObjLocation():
    sky_img = cv2.imread('sky.jpg', cv2.IMREAD_UNCHANGED)
    object_img = cv2.imread('object.jpg', cv2.IMREAD_UNCHANGED)  # object.jpg is the stellar object to track.


    if observerMode:
        cv2.imshow('Sky', sky_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        cv2.imshow('Object', object_img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    result = cv2.matchTemplate(sky_img, object_img, cv2.TM_SQDIFF_NORMED)  # TODO: Handling missing result.

    if showMatchingResult:
        cv2.imshow('Result', result)
        cv2.waitKey()
        cv2.destroyAllWindows()

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if (min_val > 1-TRESHHOLD):
        raise Exception("Matching unsuccesful. Try with another object or lower the treshhold.")

    if observerMode:
        try:
            w = object_img.shape[1]
            h = object_img.shape[0]

            cv2.rectangle(sky_img, min_loc, (min_loc[0] + w, min_loc[1] + h), (0, 255, 255), 2)

            t_yloc, t_xloc = np.where(result <= TRESHHOLD)

            len(t_yloc)
            len(t_xloc)
            rectangles = []
            for (x, y) in zip(t_xloc, t_yloc):
                rectangles.append([int(x), int(y), int(w), int(h)])
                rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

            rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

            for (x, y, w, h) in rectangles:
                cv2.rectangle(sky_img, (x, y), (x + w, y + h), (0, 255, 255), 2)

            cv2.imshow('Rectangles', sky_img)
            cv2.waitKey()
            cv2.destroyAllWindows()
        except:
            print("An error occured while trying to display results.")

    return min_loc


# Returns with movement scale. By knowing the field of view (FOV) of the camera (LENVIEW) a pixels value can be
# transformed to degrees as scale.
def GetMovementScale():
    if (picw != null & picw > 0 & pich != null & pich > 0):
        t_xscale = LENVIEW / picw  # 1 unit of picture width = t_xscale degrees
        t_yscale = LENVIEW / pich  # 1 unit of picture height = t_yscale degrees

    return t_xscale, t_yscale


# Returns the Manhattan distance of the location of the object from focus point of the lens (screen)
def GetManhattanDistance(t_xloc, t_yloc):
    if (t_xloc != null & t_yloc != null):
        t_xdist = t_xloc - picw / 2
        t_ydist = pich / 2 - t_yloc

    return t_xdist, t_ydist

# This is the virtual endpoint for the script. Had I had the hardware strong enough for rotating the camera gear
# commands could be sent to a RaspberryPI unit with an Arduino controlling the (servo) motors.
def MotorDummy(t_xdist, t_ydist, t_xscale, t_yscale):
    xdeg = t_xdist * t_xscale
    ydeg = t_ydist * t_yscale

    print("Horizontal angle correction required: " + str(round(xdeg)) + " [degrees]")
    print("Vertical angle correction required: " + str(round(ydeg)) + " [degrees]")

xloc, yloc = GetObjLocation()  # Locating the tracked object
xscale, yscale = GetMovementScale()  # Calculating one pixels value in degrees
xdist, ydist = GetManhattanDistance(xloc, yloc)  # Calculating the objects distance from the center of the screen
MotorDummy(xdist, ydist, xscale, yscale)  # Endpoint
