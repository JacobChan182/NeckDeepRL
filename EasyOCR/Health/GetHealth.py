import cv2
import easyocr

reader = easyocr.Reader(['en'])

frame = cv2.imread("frame.png")

# Coordinates of the score region (x1, y1, x2, y2)
x1, y1, x2, y2 = 125, 150, 160, 175
score_crop = frame[y1:y2, x1:x2]

result = reader.readtext(score_crop, detail=0)
print("Health:", result[0])