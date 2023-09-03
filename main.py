import cv2
import logging


def main():

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
    logging.info(f"OpenCV Version: {cv2.getVersionString()}")

    #source = cv2.VideoCapture(0)


if __name__ == "__main__":
    main()
