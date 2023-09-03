import cv2
import numpy as np
import glob
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

boardSize = (8, 7)
refiningCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Stores vectors of 3D points for each image
objPoints = []

# Stores vectors of 2D points for each image
imgPoints = []

# Define world cords for 3D points
objWorldPoints = np.zeros((1, boardSize[0] * boardSize[1], 3), np.float32)
objWorldPoints[0, :, :2] = np.mgrid[0:boardSize[0], 0:boardSize[1]].T.reshape(-1, 2)

# Holds the shape of the previous image
prevImgShape = None

# Pulls in all images in the calibration images folder
images = glob.glob('calibrationImages/*.png')

for fname in images:
    logging.info(f"Reading in image: {fname}")
    # Read the image into OpenCV
    img = cv2.imread(fname)

    # Turn the image gray scale - helps with detections
    gImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gImg, boardSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret:
        logging.info(f"Found values")
        objPoints.append(objWorldPoints)

        sharpCorners = cv2.cornerSubPix(gImg, corners, (11,11), (-1,-1), refiningCriteria)
        imgPoints.append(sharpCorners)

        imageWithDetections = cv2.drawChessboardCorners(img, boardSize, sharpCorners, ret)

        cv2.imshow(f"{fname}", imageWithDetections)
        cv2.waitKey(0)

    height, width = img.shape[:2]

if not objPoints:
    logging.error("Found no valid detections")
    exit(69)

cv2.destroyAllWindows()

ret, inMatrix, distCoef, rotVect, transVect = cv2.calibrateCamera(objPoints, imgPoints, gImg.shape[::-1], None, None)

print(f'Camera matrix: \n {inMatrix}')
print(f'Distortion Coeff: \n {distCoef}')
print(f'Rotation Vectors: \n {rotVect}')
print(f'Translation Vectors: \n {transVect}')

