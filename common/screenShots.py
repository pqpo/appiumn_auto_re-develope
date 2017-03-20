import time


def screen_shot(case_name, driver, result_path):
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    screen_img = result_path + case_name + "_" + current_time + "_CheckPoint_NG.png"
    driver.get_screenshot_as_file(screen_img)
    return screen_img
