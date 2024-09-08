import tkinter as tk
from tkinter import ttk
from random import sample, choice


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Русская рулетка')
        self.geometry('500x500+420+228')
        self.resizable(True, True)
        self.minsize(500, 500)
        self.attributes('-toolwindow', False)
               
        self._rev = Revolver(6)
        
        ttk.Label(text='Правила игры:').pack(expand=True)
        ttk.Label(text='Зарядить патрон: ПКМ').pack(expand=True)
        ttk.Label(text='Вращать барабан: Колесо мыши').pack(expand=True)
        ttk.Label(text='Выстрелить: ЛКМ').pack(expand=True)
        
        self._loaded_label = ttk.Label(text='Заряжено патронов: 0')
        self._loaded_label.pack(expand=True)
        
        self._actions_label = ttk.Label()
        self._actions_label.pack(expand=True)
        
        self._res_label = ttk.Label()
        self._res_label.pack(expand=True)
        
        self.bind(
            '<ButtonPress-3>',
            self.load_cartridge
        )
        
        self.bind(
            '<MouseWheel>',
            self.rotate_cylinder
        )
        
        self.bind(
            '<ButtonPress-1>',
            self.shoot
        )
        
    def load_cartridge(self, e) -> None:
        if not self._rev.full:
            self._rev.load_cartridge()
            self._actions_label.configure(text='Заряжаю...')
            self._loaded_label.configure(text=f'Заряжено патронов: {self._rev.loaded}')
        else:
            self._actions_label.configure(text='Барабан заряжен полностью')
        
    def rotate_cylinder(self, e) -> None:
        if e.delta > 0:
            self._rev.rotate_clockwise()
            self._actions_label.configure(text='Поворачиваю по часовой стрелке...')
        else:
            self._rev.rotate_counterclockwise()
            self._actions_label.configure(text='Поворачиваю против часовой стрелки...')
    
    def shoot(self, e) -> None:
        if self._rev.shoot() == 1:
            self._actions_label.configure(text='БАХ')
            self._loaded_label.configure(text=f'Заряжено патронов: {self._rev.loaded}')
            self._res_label.configure(text='УБИТ') 
        else:
            self._actions_label.configure(text='Щелк')
            self._res_label.configure(text='ЖИВ')
        

class Revolver:
    def __init__(self, chambers: int) -> None:
        self._chambers: list[int] = [0] * chambers
        self._barrel_index: int = 0
        
    def load_cartridge(self) -> None:
        print('Заряжаю...')
        if len(self._chambers) == sum(self._chambers):
            print('Барабан полон')
        else:
            while True:
                i = choice(range(len(self._chambers)))
                if self._chambers[i] == 0:
                    self._chambers[i] = 1
                    break          
    
    def rotate_clockwise(self) -> None:
        self._barrel_index += 1
        self._barrel_index %= len(self._chambers)
        print('Повернул по часовой.')
        
    def rotate_counterclockwise(self) -> None:
        self._barrel_index -= 1
        self._barrel_index %= len(self._chambers)
        print('Повернул против часовой.')
    
    def shoot(self) -> int:
        if self._chambers[self._barrel_index] == 1:
            print('БАХ')
            self._chambers[self._barrel_index] = 0
            return 1
        else:
            print('Щёлк')
            return 0
    
    @property
    def loaded(self) -> int:
        print(f'Заряжено {sum(self._chambers)} патронов.')
        return sum(self._chambers)
    
    @property
    def full(self) -> bool:
        return sum(self._chambers) == len(self._chambers)
        
if __name__ == '__main__':
    App().mainloop()
