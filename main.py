from renderer import Renderer
import os
import cv2
import shutil
import time

PATH_FRAMES = "frames/"
PATH_SOURCE_VIDEO = "source_video/"
SAVE_FILE_NAME = "save.ini"

SOURCE_VIDEO_NAME = ""
IS_CONVERTED_TO_FRAME = False
IS_FRAME_RENDERED = False
IS_CLEAR = False

FRAME_EXCEPT_TIME = 1
WIDTH = 60

FRAMES = []


def save():
    file = open(SAVE_FILE_NAME, mode="wt", encoding="utf-8")
    file.write(SOURCE_VIDEO_NAME + "\n")
    file.write(str(IS_CONVERTED_TO_FRAME) + "\n")
    file.write(str(IS_FRAME_RENDERED) + "\n")
    file.write(str(IS_CLEAR) + "\n")
    file.write(str(FRAME_EXCEPT_TIME) + "\n")
    file.write(str(WIDTH) + "\n")
    for item in FRAMES:
        file.write(item + ".\n")
    file.close()


def load_save():
    global SOURCE_VIDEO_NAME
    global IS_CONVERTED_TO_FRAME
    global IS_FRAME_RENDERED
    global IS_CLEAR
    global FRAME_EXCEPT_TIME
    global WIDTH

    try:
        file = open(SAVE_FILE_NAME, mode="rt", encoding="utf-8")
        SOURCE_VIDEO_NAME = file.readline()
        IS_CONVERTED_TO_FRAME = file.readline() == "True\n"
        IS_FRAME_RENDERED = file.readline() == "True\n"
        IS_CLEAR = file.readline() == "True\n"
        FRAME_EXCEPT_TIME = int(file.readline())
        WIDTH = int(file.readline())

        frame = ""
        while True:
            frame += file.readline()
            if frame == "":
                break
            if "." in frame:
                frame = frame.replace(".", "")
                FRAMES.append(frame)
                frame = ""
        file.close()
        print("loaded save file")
    except Exception:
        print("no save file")


def is_source_video_exists():
    for item in os.listdir(PATH_SOURCE_VIDEO):
        if item == SOURCE_VIDEO_NAME:
            return True
    return False


def get_frame_count():
    file_list = os.listdir(PATH_FRAMES)
    return len(file_list)


def clear():
    os.system("cls")


def wait():
    print("press enter to continue...")
    input()


def get_clip_length():
    video = cv2.VideoCapture(PATH_SOURCE_VIDEO + SOURCE_VIDEO_NAME)
    return 1 / (video.get(cv2.CAP_PROP_FPS) / FRAME_EXCEPT_TIME)


def set_source_video_name(cmd):
    global SOURCE_VIDEO_NAME
    global IS_CONVERTED_TO_FRAME
    global IS_FRAME_RENDERED

    back_up = SOURCE_VIDEO_NAME
    try:
        SOURCE_VIDEO_NAME = cmd.split(" ")[1]
        if is_source_video_exists():
            print("source video name set to " + SOURCE_VIDEO_NAME)
        else:
            SOURCE_VIDEO_NAME = back_up
            print("source video name set failure")
    except Exception:
        SOURCE_VIDEO_NAME = back_up
        print("source video name set failure")
    IS_CONVERTED_TO_FRAME = False
    IS_FRAME_RENDERED = False


def render():
    global IS_FRAME_RENDERED

    if not IS_CONVERTED_TO_FRAME:
        print("source video has not been converted to frames")
    else:
        FRAMES.clear()

        print("rendering frames")

        for i in range(0, int(get_frame_count() / FRAME_EXCEPT_TIME)):
            FRAMES.append(Renderer.runner(
                PATH_FRAMES + "frame" + str(i * FRAME_EXCEPT_TIME) + ".jpg", WIDTH))
            if i % 100 == 0:
                clear()
                print("rendering " + str(i) + "/" +
                      str(int(get_frame_count() / FRAME_EXCEPT_TIME)))

        clear()
        print("rendering finished")
        IS_FRAME_RENDERED = True


def convert_to_frame():
    global IS_CONVERTED_TO_FRAME
    global IS_FRAME_RENDERED

    video_object = cv2.VideoCapture(PATH_SOURCE_VIDEO + SOURCE_VIDEO_NAME)

    print("deleting frames")
    shutil.rmtree(PATH_FRAMES)
    os.mkdir(PATH_FRAMES)

    frame_count = int(cv2.VideoCapture(PATH_SOURCE_VIDEO + SOURCE_VIDEO_NAME).get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0

    while True:
        success, image = video_object.read()
        if success:
            cv2.imwrite(PATH_FRAMES + "frame" + str(count) + ".jpg", image)

            count += 1

            if count % 100 == 0:
                clear()
                print("converting frame " + str(count) + "/" + str(frame_count))
        else:
            break

    print("converting finished")
    IS_CONVERTED_TO_FRAME = True
    IS_FRAME_RENDERED = False


def play():
    global IS_FRAME_RENDERED

    if not IS_CONVERTED_TO_FRAME:
        print("source video has not been converted to frames")
    else:
        if not IS_FRAME_RENDERED:
            render()

        clip_length = get_clip_length()

        last_time = time.time()

        count = 0

        while count < len(FRAMES):
            if time.time() - last_time > clip_length:
                if IS_CLEAR:
                    clear()
                print(FRAMES[int(count)])
                count += 1
                last_time = time.time()


def set_frame_except_time(cmd):
    global FRAME_EXCEPT_TIME
    global IS_FRAME_RENDERED

    back_up = FRAME_EXCEPT_TIME
    try:
        FRAME_EXCEPT_TIME = int(cmd.split(" ")[1])
        if FRAME_EXCEPT_TIME > 0:
            print("frame except time set to " + str(FRAME_EXCEPT_TIME))
        else:
            FRAME_EXCEPT_TIME = back_up
            print("frame except time set failure")
    except Exception:
        FRAME_EXCEPT_TIME = back_up
        print("frame except time set failure")
    IS_FRAME_RENDERED = FRAME_EXCEPT_TIME == back_up


def set_width(cmd):
    global WIDTH
    global IS_FRAME_RENDERED

    back_up = WIDTH
    try:
        WIDTH = int(cmd.split(" ")[1])
        if WIDTH > 0:
            print("width set to " + str(WIDTH))
            if IS_CONVERTED_TO_FRAME:
                print("rendered middle frame")
                print(Renderer.runner(PATH_FRAMES + "frame" + str(int(get_frame_count() / 2)) + ".jpg", WIDTH))
        else:
            WIDTH = back_up
            print("width set failure")
    except Exception:
        WIDTH = back_up
        print("width set failure")
    IS_FRAME_RENDERED = WIDTH == back_up


os.system("chcp 949")

while True:
    clear()
    cmd = input(">>>")

    if cmd.startswith("set_source_video"):
        clear()
        set_source_video_name(cmd)
        wait()

    if cmd.startswith("convert_to_frame"):
        clear()
        if not is_source_video_exists():
            print("source video not selected")
        else:
            convert_to_frame()
        wait()

    if cmd.startswith("play"):
        clear()
        if not is_source_video_exists():
            print("source video not selected")
        else:
            play()
        wait()

    if cmd.startswith("set_frame_except_time"):
        clear()
        set_frame_except_time(cmd)
        wait()

    if cmd.startswith("set_width"):
        clear()
        set_width(cmd)
        wait()

    if cmd.startswith("set_is_clear_on"):
        clear()
        print("is clear set to on")
        IS_CLEAR = True
        wait()

    if cmd.startswith("set_is_clear_off"):
        clear()
        print("is clear set to off")
        IS_CLEAR = False
        wait()

    if cmd.startswith("render"):
        clear()
        if not is_source_video_exists():
            print("source video not selected")
        else:
            render()
        wait()

    if cmd.startswith("save_and_exit"):
        save()
        break

    if cmd.startswith("load_save"):
        clear()
        load_save()
        wait()

    if cmd.startswith("save"):
        save()

    if cmd.startswith("exit"):
        break
