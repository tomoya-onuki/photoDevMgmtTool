import cv2
import sys
import os
import glob
import shutil
from tkinter import filedialog
import tkinter as tk


def init_tk():
    root = tk.Tk()
    root.withdraw()


def show_file_dialog():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    dirname = filedialog.askdirectory(initialdir=root_dir)
    return f'{dirname}/'


def get_dirname():
    args = sys.argv
    # print(args)
    if len(args) == 1:
        print('arg error: python3 photoSelectTool.py [dirname]')
        exit()
    else:
        dirname = args[1]
        dirname = dirname if dirname.endswith('/') else f'{dirname}/'
        return dirname


def read_img_filenames(dirname):
    if os.path.isdir(dirname):
        files = sorted(glob.glob(f'{dirname}*.JPG'))
        return files
    else:
        print(f'Error: {dirname} is NOT directory.')
        exit()


def show_img(filename):
    cv_img = cv2.imread(filename)
    height, width, channels = cv_img.shape[:3]
    resize_ratio = 600 / max(width, height)
    cv_img = cv2.resize(cv_img, None, fx=resize_ratio, fy=resize_ratio)
    cv2.imshow("image", cv_img)
    print(f'file name = {filename}')


def select_img(root_dirname, filename):
    SELECTED_IMG_DIR_JPG = f'{root_dirname}selected/'
    SELECTED_IMG_DIR_RAW = f'{root_dirname}selected/RAW/'
    if not os.path.exists(SELECTED_IMG_DIR_JPG):
        os.mkdir(SELECTED_IMG_DIR_JPG)
    if not os.path.exists(SELECTED_IMG_DIR_RAW):
        os.mkdir(SELECTED_IMG_DIR_RAW)

    shutil.copy(filename, SELECTED_IMG_DIR_JPG)
    shutil.copy(filename.replace('JPG', 'RW2'), SELECTED_IMG_DIR_RAW)

    # if os.path.exists(SELECTED_IMG_DIR1) == False:
    #     os.mkdir(SELECTED_IMG_DIR1)

    # # 縦長と横長で保存先を変える
    # cv_img = cv2.imread(filename)
    # height, width, channels = cv_img.shape[:3]
    # if width > height:
    #     shutil.copy(filename, SELECTED_IMG_DIR0)
    # else:
    #     shutil.copy(filename, SELECTED_IMG_DIR1)


def increment_file_idx(file_idx, max):
    if file_idx < max:
        file_idx += 1
        return file_idx
    else:
        print('File is finished.')
        print('Please Enter (ESC)')
        return -1


def main():
    init_tk()
    dirname = show_file_dialog()
    start_msg = 'Usage:\n'\
                '   (ESC) >> 終了\n'\
                '   (Y)   >> 画像を採用する\n'\
                '   (N)   >> 画像を不採用にする\n'\
                '   (B)   >> 1つまえの画像に戻る\n'\
                '   (R)   >> 現在の選択画像ディレクトリをクリアする'
    print(start_msg)
    filenames = read_img_filenames(dirname)

    file_idx = 0
    MAIN_LOOP = True
    while MAIN_LOOP:
        if -1 < file_idx and file_idx < len(filenames):
            show_img(filenames[file_idx])
        else:
            print(f'Error: file_idx overflow. file_idx = {file_idx}')
            exit()

        key = cv2.waitKey(0)
        if key == 121:
            print('(Y)')
            select_img(dirname, filenames[file_idx])
            file_idx = increment_file_idx(file_idx, len(filenames))
        elif key == 110:
            print('(N)')
            file_idx = increment_file_idx(file_idx, len(filenames))
        elif key == 98:
            print('(B) Back')
            if file_idx > 0:
                file_idx -= 1
        elif key == 114:
            print('(R) Clear Selected Img Directory.')
            shutil.rmtree(f'{dirname}/selected0')
            shutil.rmtree(f'{dirname}/selected1')
        elif key == 27:  # ESCで終了
            print('(ESC) Quit')
            MAIN_LOOP = False

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
