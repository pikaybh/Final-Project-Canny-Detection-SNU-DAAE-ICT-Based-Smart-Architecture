# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt


class CannyEdge:
    image = np.ndarray

    def __init__(self, _input_dir : str, _target : str, _save_file_dir : str) -> None:
        self.input_dir = _input_dir
        self.target = _target
        self.save_file_dir = _save_file_dir
        CannyEdge.image = cv2.imread(self.input_dir + '/' + self.target)

    def contouring(self, save = True) -> tuple:
        # 컨투어 찾기 전 이미지 전처리
        gray = cv2.cvtColor(CannyEdge.image, cv2.COLOR_BGR2GRAY)# 이미지 출력
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.bitwise_not(gray) # 객체보다 배경이 밝은 경우 이미지 반전
        # canny edge, threshold 등 다양한 전처리 시도 -> 객체와 배경을 가장 잘 분리하는 전처리 사용
        edge = cv2.Canny(gray, 100, 100)
        # Save the Canny edge image
        if save : cv2.imwrite(f"{self.save_file_dir}/{self.target.split('.')[0]}_edge.jpg", edge)
        return gray, edge


if __name__ == "__main__":
    canny_obj = CannyEdge("D:/Projects/canny/scr/data/test", "smile_cat.jpg", "D:/Projects/canny/scr/data/test")
    image = canny_obj.image
    image2 = CannyEdge.image.copy()
    gray, edge = canny_obj.contouring()

    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    adaptive_threshold= cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    # 컨투어 찾기
    contours, hierachy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 컨투어 면적이 큰 순으로 정렬
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for i in range(len(sorted_contours)):
        contour = sorted_contours[i]
        # 근사 컨투어 계산을 위한 0.01의 오차 범위 지정 
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        cv2.drawContours(image, [contour], -1, (0,255,0), 3)
        cv2.drawContours(image2, [approx], -1, (0,255,0), 3)

        extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
        extRight = tuple(contour[contour[:, :, 0].argmax()][0])
        extTop = tuple(contour[contour[:, :, 1].argmin()][0])
        extBot = tuple(contour[contour[:, :, 1].argmax()][0])

        cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
        cv2.circle(image, extRight, 8, (0, 255, 0), -1)
        cv2.circle(image, extTop, 8, (255, 0, 0), -1)
        cv2.circle(image, extBot, 8, (255, 255, 0), -1)
    # 결과 출력
    cv2.imshow('contour', image)
    cv2.imshow('approx', image2)
    cv2.waitKey()
    cv2.destroyAllWindows()
# %%
