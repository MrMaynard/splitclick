def color_picker(img):
    import cv2
    import sys
    import numpy as np

    def nothing(x):
        pass

    # Create a window
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('HMin\n', 'image', 0, 179, nothing)  # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin\n', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin\n', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax\n', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax\n', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax\n', 'image', 0, 255, nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax\n', 'image', 179)
    cv2.setTrackbarPos('SMax\n', 'image', 255)
    cv2.setTrackbarPos('VMax\n', 'image', 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    output = img
    waitTime = 33

    while (1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin\n', 'image')
        sMin = cv2.getTrackbarPos('SMin\n', 'image')
        vMin = cv2.getTrackbarPos('VMin\n', 'image')

        hMax = cv2.getTrackbarPos('HMax\n', 'image')
        sMax = cv2.getTrackbarPos('SMax\n', 'image')
        vMax = cv2.getTrackbarPos('VMax\n', 'image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)

        # Print if there is a change in HSV value
        if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
            hMin, sMin, vMin, hMax, sMax, vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display output image
        cv2.imshow('image', output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(waitTime) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()