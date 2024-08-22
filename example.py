import pyautogui as pag
import cv2
import numpy as np
import keyboard

def capture_screen(region=None):
    screenshot = pag.screenshot(region=region)
    screenshot = cv2.cvtColor(
        np.array(screenshot), cv2.COLOR_RGB2BGR
    )
    return screenshot

def find_target(image, target_color, threshold=10):
    mask = cv2.inRange(image, target_color - threshold, target_color + threshold)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2
    return None

def move_and_click(target):
    pag.moveTo(target)
    pag.click()

target_color = np.array([219, 174, 88])
screen_region = (0, 0, 1920, 1080)

while True:
    screen = capture_screen(region=screen_region)
    target_position = find_target(screen, target_color)

    if keyboard.is_pressed('q'):  # Press 'q' to stop the script
        print("Stopping...")
        break

    if target_position:
        move_and_click(target_position)
