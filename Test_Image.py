import cv2

# Load an image from file
image = cv2.imread('Assets/image.jpg')

# Display the image in a window
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()