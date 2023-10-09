import cv2
import numpy as np
import logging
import const


def runCalibration(images):
    # Holds the shape of the previous image
    prevImgShape = None

    # Stores vectors of 2D points for each image
    imgPoints = []

    # Stores vectors of 3D points for each image
    objPoints = []

    boardSize = const.checkerBoardSize

    for fname in images:
        logging.info(f"Reading in image: {fname}")
        # Read the image into OpenCV
        img = cv2.imread(fname)

        # Turn the image gray scale - helps with detections
        gImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gImg, boardSize, None)

        if ret:
            logging.info(f"Found values")
            objPoints.append(const.objWorldPoints)

            sharpCorners = cv2.cornerSubPix(gImg, corners, (11, 11), (-1, -1), const.failCriteria)
            imgPoints.append(sharpCorners)

            cv2.drawChessboardCorners(img, boardSize, sharpCorners, ret)
            cv2.imshow(f"{fname}", img)
            cv2.waitKey(250)

    if not objPoints:
        logging.error("Found no valid detections")
        exit(69)
    else:
        cv2.destroyAllWindows()

    ret, inMatrix, distCoef, rotVect, transVect = cv2.calibrateCamera(objPoints, imgPoints, gImg.shape[:2], None, None)

    print(f"Camera Calibrated: {ret}")
    print(f'Camera matrix: \n {inMatrix}')
    print(f'Distortion Coeff: \n {distCoef}')

    np.savez("camera-params", cameraMatrix=inMatrix, dist=distCoef, rvecs=rotVect, tvecs=transVect)


def verifyCalibration(images, inMatrix, distCoef):
    img = cv2.imread(images[0])
    h, w = img.shape[:2]
    newCamMatrix, roi = cv2.getOptimalNewCameraMatrix(inMatrix, distCoef, (w, h), 1, (w, h))

    dst = cv2.undistort(img, inMatrix, distCoef, None, newCamMatrix)
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite('calibrationImages/calResultUndistort.png', dst)

    mapx, mapy = cv2.initUndistortRectifyMap(inMatrix, distCoef, None, newCamMatrix, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite('calibrationImages/calResultMap.png', dst)


def calcError(rotVect, transVect, inMatrix, distCoef, objPoints, imgPoints):
    meanError = 0

    for i in range(len(objPoints)):
        imgPoints2, _ = cv2.projectPoints(objPoints[i], rotVect[i], transVect[i], inMatrix, distCoef)
        error = cv2.norm(imgPoints[i], imgPoints2, cv2.NORM_L2) / len(imgPoints2)
        meanError += error

    print(f'Total Error: {meanError / len(objPoints)}')
