import cv2
import numpy as np

checkerBoardSize = (8, 6)
failCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Define world cords for 3D points
objWorldPoints = np.zeros((1, checkerBoardSize[0] * checkerBoardSize[1], 3), np.float32)
objWorldPoints[0, :, :2] = np.mgrid[0:checkerBoardSize[0], 0:checkerBoardSize[1]].T.reshape(-1, 2)
