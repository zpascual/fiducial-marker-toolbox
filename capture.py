import cv2
import logging
import os
from datetime import datetime
from pathlib import Path


def camPortSelector():
    badPorts = list()
    devPort = 0
    workingPorts = list()
    availablePorts = list()

    while len(badPorts) < 6:
        camera = cv2.VideoCapture(devPort)
        if not camera.isOpened():
            badPorts.append(devPort)
            logging.info(f"Port {devPort} is not working")
        else:
            isReading, img = camera.read()
            width = camera.get(3)
            height = camera.get(4)
            if isReading:
                logging.info(f"Port {devPort} is working and had a res: ({width}, {height})")
                workingPorts.append([devPort, width, height])
            else:
                logging.info(f"Port {devPort} for camera ({width}, {height}) is present but doesn't read.")
                availablePorts.append(devPort)
        devPort += 1

    logging.info("Please select one of the following camera ports by typing in the number: ")

    for data in workingPorts:
        logging.info(f"Port: {data[0]} ({data[1]}, {data[2]}")
        while True:
            port = input("Selected Port: ")

            if port.isdigit():
                return port
            else:
                logging.error("Please enter a valid port")


def archiveImgs():
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


def captureImg(port):
    archiveImgs()

    source = cv2.VideoCapture(port)
    qtySavedImg = 0

    print("\nWelcome to capturing images to calibration!")
    print("Please choose an option below")
    print("esc key: stops capturing images")
    print("s key: captures the image displayed in the window \n")

    input("Press the enter key to continue")

    while source.isOpened():

        ret, img = source.read()

        if not ret:
            logging.error("Bitch you ain't got no image")
            continue

        cv2.imshow('Image', img)

        inputKey = cv2.waitKey(250)

        if inputKey == 27:  # Escape key
            break
        elif inputKey is ord("s"):
            cv2.imwrite(f'calibrationImages/img{qtySavedImg}.png', img)
            logging.info("Image Saved")
            qtySavedImg += 1

    source.release()
    cv2.destroyAllWindows()
