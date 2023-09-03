import cv2
import logging
import os
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

path = './calibrationImages'
if os.listdir(path):
    now = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    newPath = f"./calibrationImages/Images_{now}"
    os.mkdir(newPath)
    for fileName in os.listdir(path):
        if ".png" in fileName:
            srcFile = Path(f"{path}/{fileName}")
            destFile = Path(f"{newPath}/{fileName}")
            srcFile.rename(destFile)
            logging.info(f"Moved File: {path}/{fileName} -> {newPath}/{fileName}")
else:
    logging.info("No Images Found")

source = cv2.VideoCapture(0)
qtySavedImg = 0

print("\nWelcome to capturing images to calibration!")
print("Please choose an option below")
print("esc key: stops capturing images")
print("s key: captures the image displayed in the window \n")

input("Press the enter key to continue")

while source.isOpened():

    ret, img = source.read()

    inputKey = cv2.waitKey(5)

    if inputKey == 27:  # Escape key
        break
    elif inputKey is ord("s"):
        cv2.imwrite(f'calibrationImages/img{qtySavedImg}.png', img)
        logging.info("Image Saved")
        qtySavedImg += 1

    cv2.imshow('Image', img)

source.release()
cv2.destroyAllWindows()
