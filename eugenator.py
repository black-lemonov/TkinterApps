
import tkinter as tk
import tkinter.ttk as ttk


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Я ЖЕНЯ')
        self.geometry('500x400+400+100')
        
        for i in range(5): self.rowconfigure(index=i, weight=1)
        self.rowconfigure(index=0, weight=2)
        self.rowconfigure(index=1, weight=2)
        for i in range(2): self.columnconfigure(index=i, weight=1)        
        
        norm_font = ('Arial', 14)
        self._err_msg = tk.StringVar()
        self._name_var = tk.StringVar()
        self._success_msg = tk.StringVar()
                
        ttk.Label(text='Здравствуйте, как вас зовут?', font=norm_font).grid(row=0, column=0, columnspan=2)
        
        check = (self.register(self.is_input_correct), "%P")
        ttk.Entry(textvariable=self._name_var, font=norm_font, validate='key', validatecommand=check).grid(row=1, column=0, columnspan=2)

        ttk.Label(font=norm_font, foreground='red', textvariable=self._err_msg).grid(row=2, column=0, columnspan=2)
        ttk.Label(font=norm_font, foreground='green', textvariable=self._success_msg).grid(row=3, column=0, columnspan=2)       
        
        ttk.Button(text='Подтвердить', command=self.check_name).grid(row=4, column=0)
        ttk.Button(text='Очистить', command=self.clear_name).grid(row=4, column=1)
        
        self.mainloop()     
        
    def is_input_correct(self, val: str) -> bool:
        print(val)
        res = val.isalpha()   
        if not res:
            self._err_msg.set('Имя должно состоять только из букв!')
        else:
            self._err_msg.set('')
        return res
    
    def check_name(self) -> None:
        print(self._name_var)
        cap_name = self._name_var.get().capitalize()
        if cap_name == '':
            self._err_msg.set('Имя не может быть пустым!')
        elif  cap_name == 'Женя' or cap_name == 'Рамзан' or cap_name == 'Ахмат':
            self._success_msg.set('Прекрасное имя, поздравляем!')
        else:
            self._err_msg.set('Ужасное имя. Введите другое.')

    def clear_name(self) -> None:
        self._name_var.set('')
        self._err_msg.set('')
        self._success_msg.set('')
        
            
                   
        
        
App()
        
        