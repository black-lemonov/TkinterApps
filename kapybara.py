
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('КАПИБАРА: ПУТЬ К БОГАТСТВУ')
        self.geometry('550x660+500+100')
        self.resizable(True, True)
        self.minsize(550, 660)
        
        self._money = 0
        self._money_label = ttk.Label(text=f'Баланс: {0:08}', font=('Comic Sans', 16))
        self._money_label.pack(anchor=tk.NE)
        
        # картинка с капибарой
        self._img = ImageTk.PhotoImage(Image.open('static/капибара.png'))
        
        self._img_label = ttk.Label(image=self._img)
        self._img_label.pack(expand=True, anchor=tk.CENTER)
        
        
        self.bind(
            '<ButtonPress-1>',
            self.inc_money
        )
        
    def inc_money(self, e) -> None:
        self._money += 1
        self._money_label['text'] = f'Баланс: {self._money:08}'



if __name__ == '__main__':    
    App().mainloop()
        