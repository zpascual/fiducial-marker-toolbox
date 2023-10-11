import cv2
import logging
import glob
import numpy as np
import calibration
import capture


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
    logging.info(f"OpenCV Version: {cv2.getVersionString()}")

    # Pulls in all images in the calibration images folder
    images = glob.glob('calibrationImages/*.png')

    # Imports saved camera intrinsics
    with np.load('cameraparams.npz') as file:
        mtx, dist, rvecs, tvecs = [file[i] for i in {'cameraMatrix', 'dist', 'rvecs', 'tvecs'}]


def calibrate():
    # Capture images for calibration
    
    selectedPort = capture.camPortSelector()
    capture.captureImg(selectedPort)


if __name__ == "__main__":
    main()
