import os
import glob
import shutil
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from datetime import datetime

image = []


class App(tk.Frame):
    def __init__(self, root):
        self.W = 620
        self.H = 620
        self.CVS_W = 600
        self.CVS_H = 400
        self.file_idx = 0
        self.selected_file_idx_list = []

        self.dirname = self.show_file_dialog()
        self.filenames = self.read_img_filenames()
        self.pil_img_list = self.get_pil_img_list()
        if len(self.pil_img_list) == 0:
            exit()

        self.make_main_window(root)

        # 写真番号ラベルの設置
        self.photo_no_label = tk.Label(root,
                                       text=f'Photo No.{self.file_idx}',
                                       anchor=tk.W)
        self.photo_no_label.place(x=10, y=self.CVS_H + 10)

        # 使い方ラベルの設置
        l0 = tk.Label(root, text='[USAGE]: Please input key.', anchor=tk.W)
        l0.place(x=10, y=self.CVS_H + 40)
        l1 = tk.Label(root, text='(y) Select this Photo.', anchor=tk.W)
        l1.place(x=10, y=self.CVS_H + 60)
        l2 = tk.Label(root, text='(n) NOT Select this Photo', anchor=tk.W)
        l2.place(x=10, y=self.CVS_H + 80)
        l3 = tk.Label(root, text='(b) Back to previous Photo.', anchor=tk.W)
        l3.place(x=10, y=self.CVS_H + 100)
        l4 = tk.Label(root, text='(r) Clear All Selected Photos.', anchor=tk.W)
        l4.place(x=10, y=self.CVS_H + 120)

        # コンソール作成
        l5 = tk.Label(root, text='Console', anchor=tk.W)
        l5.place(x=250, y=self.CVS_H + 10)
        self.console_label = tk.Label(root, text='', anchor=tk.NW,
                                      width=50,
                                      height=12,
                                      borderwidth=1,
                                      relief=tk.SOLID,
                                      font=('Courier', '12'))
        self.console_label.place(x=250, y=self.CVS_H + 30)

        # 画像表示用canvasの作成
        self.canvas = self.make_canvas(root)
        # 画像表示
        self.show_img()

        root.bind("<KeyPress>", self.key_event)

    def show_file_dialog(self):
        root_dir = os.path.abspath(os.path.dirname(__file__))
        dirname = filedialog.askdirectory(initialdir=root_dir)
        return f'{dirname}/'

    def read_img_filenames(self):
        if os.path.isdir(self.dirname):
            files = sorted(glob.glob(f'{self.dirname}*.JPG'))
            return files
        else:
            print(f'Error: {self.dirname} is NOT directory.')
            exit()

    def select_img(self):
        filename = self.filenames[self.file_idx]
        SELECTED_IMG_DIR_JPG = f'{self.dirname}selected/'
        SELECTED_IMG_DIR_RAW = f'{self.dirname}selected/RAW/'
        if not os.path.exists(SELECTED_IMG_DIR_JPG):
            os.mkdir(SELECTED_IMG_DIR_JPG)
        if not os.path.exists(SELECTED_IMG_DIR_RAW):
            os.mkdir(SELECTED_IMG_DIR_RAW)
        shutil.copy(filename, SELECTED_IMG_DIR_JPG)
        shutil.copy(filename.replace('JPG', 'RW2'), SELECTED_IMG_DIR_RAW)
        self.selected_file_idx_list.append(self.file_idx)

    def increment_file_idx(self):
        self.file_idx += 1
        if self.file_idx >= len(self.pil_img_list):
            self.file_idx = 0

    def make_main_window(self, root):
        root.geometry(f'{self.W}x{self.H}')
        root.title('Photo Select Tool')

    def make_canvas(self, root):
        canvas = tk.Canvas(root, height=self.CVS_H, width=self.CVS_W)
        canvas.place(x=10, y=0)
        return canvas

    def get_pil_img_list(self):
        pil_img_list = []

        for filename in self.filenames:
            img = Image.open(filename)
            pil_img_list.append(img)

        return pil_img_list

    def pil_img2tk_img(self, pil_img):
        img_w, img_h = pil_img.size
        resize_ratio = max(self.CVS_W, self.CVS_H) / max(img_w, img_h)
        resized_img_w = int(img_w * resize_ratio)
        resized_img_h = int(img_h * resize_ratio)
        tmp = pil_img.resize((resized_img_w, resized_img_h))
        return ImageTk.PhotoImage(tmp)

    def show_img(self):
        global tk_img
        tk_img = self.pil_img2tk_img(self.pil_img_list[self.file_idx])
        self.canvas.create_image(0, 0, image=tk_img, anchor=tk.NW)
        image.append(tk_img)

    def show_img_no(self):
        photo_no_text = f'Photo No.{self.file_idx}'
        if self.file_idx in self.selected_file_idx_list:
            photo_no_text += ' (selected)'
        self.photo_no_label['text'] = photo_no_text

    def add_console_label(self, text):
        date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        text = text.ljust(26, " ")
        new_text = f'{date} {text}\n{self.console_label["text"]}'
        # print(new_text)
        self.console_label['text'] = new_text

    def key_event(self, e):
        key = e.keysym
        self.show_img_no()

        if key == 'y':
            self.select_img()
            self.add_console_label(f'Select photo (no.{self.file_idx})')
            self.increment_file_idx()
            self.show_img()
        elif key == 'n':
            self.increment_file_idx()
            self.add_console_label(f'NOT select photo (no.{self.file_idx})')
            self.show_img()
        elif key == 'b':
            self.add_console_label('Back to previous photo.')
            if self.file_idx > 0:
                self.file_idx -= 1
            self.show_img()
        elif key == 'r':
            subprocess.call(f'rm -rf {self.dirname}/selected/*', shell=True)
            self.selected_file_idx_list = []
            self.add_console_label('Clear all selected photos.')


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
