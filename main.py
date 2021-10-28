import random
import time
from typing import Optional
import cv2
import numpy
import pyautogui
import win32com.client
import win32gui
from pytesseract import Output
from pytesseract import pytesseract

BoundingBoxes = tuple[int, int, int, int]

# THESE ARE THE VARIABLE YOU SHOULD BE CHANGING!
Application = "BlueStacks"  # This is the Application you are using.
pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Copy paste the file directory then add \.
# ^^^^

Array_Items = ['Covenant', 'Mystic']
LEFT = 0
TOP = 1
WIDTH = 2
HEIGHT = 3


def capture(app_name: str):
    hwnd = win32gui.FindWindow(None, app_name)
    shell = win32com.client.Dispatch("WScript.Shell")
    if hwnd:
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        left, top = win32gui.ClientToScreen(hwnd, (left, top))
        right, bottom = win32gui.ClientToScreen(hwnd, (right - left, bottom - top))
        im = pyautogui.screenshot(region=(left, top, right, bottom))
        return image(im), left, top, right, bottom
    raise Exception('window not found')


def image(source_image):
    source_image = numpy.array(source_image)
    source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2RGB)
    source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    source_image = cv2.threshold(source_image, 127, 255, cv2.THRESH_TOZERO)
    source_image = numpy.array(source_image[1])
    return source_image


def get_bounding(source_image):
    data_list = pytesseract.image_to_data(source_image, output_type=Output.DICT)
    data_box = {}
    for i in range(len(data_list['level'])):
        bounding_box = (data_list['left'][i], data_list['top'][i], data_list['width'][i], data_list['height'][i])
        if data_list['text'][i] in data_box:
            data_box[data_list['text'][i]].append(bounding_box)
        else:
            data_box[data_list['text'][i]] = [bounding_box]
    return data_box


def locate_button(boxes: dict[str, list[BoundingBoxes]], x: int, y: int, text: str) -> Optional[BoundingBoxes]:
    def dist(bounding_box: BoundingBoxes):
        return (bounding_box[0] - x) ** 2 + (bounding_box[1] - y) ** 2

    return min(boxes[text], key=dist, default=None)


def click_buy(boxes: dict[str, list[BoundingBoxes]], x, y, item: str):
    if item in boxes:
        item_box = boxes[item][0]
        if 'Buy' in boxes:
            buy_button = locate_button(boxes, item_box[LEFT] + item_box[WIDTH], item_box[TOP] + item_box[HEIGHT], 'Buy')
            click_with_window_offset(buy_button, x, y)
            return True
    return False


def refresh_confirm(boxes: dict[str, list[BoundingBoxes]], x, y, ref_con):
    if ref_con in boxes:
        refresh_button = boxes[ref_con][0]
        click_with_window_offset(refresh_button, x, y)
        return True
    else:
        return False


def click_with_window_offset(box: BoundingBoxes, x, y):
    box_x, box_y, box_w, box_h = box[LEFT], box[TOP], box[WIDTH], box[HEIGHT]
    rand_x = random.randint(box_x, box_x + box_w)
    rand_y = random.randint(box_y, box_y + box_h)
    pyautogui.click(x + rand_x, y + rand_y, clicks=2, interval=0.05, button='left')


def scroll_down(x1: int, y1: int, x2: int, y2: int):
    from_pos_x = (((x2 - x1) * 3) / 4) + x1
    from_pos_y = ((y2 - y1) / 4) + y1
    to_pos_y = (((y2 - y1) * 3) / 4) + y1
    pyautogui.moveTo(x1 + from_pos_x, y1 + to_pos_y)
    pyautogui.dragTo(x1 + from_pos_x, y1 + from_pos_y, 0.25, button='left')


def get_capture_and_bounding_box():
    img, left, top, right, bottom = capture(Application)
    bounding_boxes = get_bounding(img)
    return img, bounding_boxes, left, top, right, bottom


def buy_sequence(img, bounding_boxes, left, top, right, bottom, item: str, item_bool: list[bool]):
    if (item == 'Covenant') and item_bool[0]:
        return
    if (item == 'Mystic') and item_bool[1]:
        return
    if click_buy(bounding_boxes, left, top, item):
        time.sleep(0.2)
        new_img, new_bounding_box, new_left, new_top, new_right, new_bottom = get_capture_and_bounding_box()
        click_buy(new_bounding_box, new_left, new_top, item)
        time.sleep(0.3)
        if item == 'Covenant':
            item_bool[0] = True
        else:
            item_bool[1] = True


def main_sequence(item_bool):
    for item in Array_Items:
        img, bounding_boxes, left, top, right, bottom = get_capture_and_bounding_box()
        buy_sequence(img, bounding_boxes, left, top, right, bottom, item, item_bool)
    return bounding_boxes, left, top, right, bottom


def main():
    failed = 0
    while failed <= 5:
        failed = 0
        item_bool = [False, False]
        bounding_boxes, left, top, right, bottom = main_sequence(item_bool)
        if not item_bool[0] or not item_bool[1]:
            scroll_down(left, top, right, bottom)
        time.sleep(0.2)
        main_sequence(item_bool)
        for i in range(3):
            if refresh_confirm(bounding_boxes, left, top, 'Refresh'):
                bounding_boxes, left, top, right, bottom = main_sequence(item_bool)
                time.sleep(0.2)
            else:
                failed += 1
            if refresh_confirm(bounding_boxes, left, top, 'Confirm'):
                time.sleep(0.2)
            else:
                failed += 1


if __name__ == '__main__':
    main()
