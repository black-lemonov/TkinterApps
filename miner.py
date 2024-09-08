import random
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from typing import Any
import sys


class MineField:
    '''Игровое поле'''
    def __init__(self, rows: int, columns: int, mines: int) -> None | ValueError:
        if rows < 0:
            raise ValueError("Значение rows не может быть отрицательным!")
        self._rows = rows
        
        if columns < 0:
            raise ValueError("Значение columns не может быть отрицательным!")
        self._cols = columns
        
        if mines < 0:
            raise ValueError("Значение mines не может быть отрицательным!")
        if columns * rows < mines:
            raise ValueError("Слишком большое значение mines!")
        self._total_mines = mines
        self._active_mines = 0
        self._create_field()
        
    def _create_field(self) -> None:
        '''Создание поля'''
        self._field: list[list[int]] = [
            [0] * self._cols for _ in range(self._rows)
        ]
        
        while(self._active_mines != self._total_mines):
            rand_row, rand_col = self._get_random_cell()
            
            if self._field[rand_row][rand_col] == -1:
                continue
            
            self._field[rand_row][rand_col] = -1
            self._recalc_field(rand_row, rand_col)
            
            self._active_mines += 1
            
    def _get_random_cell(self) -> tuple[int, int]:
        '''Координата случайной клетки'''
        rand_row: int = random.randint(0, self._rows - 1)
        rand_col: int = random.randint(0, self._cols - 1)
        return rand_row, rand_col 
    
    def _recalc_field(self, mine_r: int, mine_c: int) -> None:
        '''Пересчитывает значения клеток в соответствии с координатой мины'''
        for r in range(self._rows):
            for c in range(self._cols):
                if self._field[r][c] == -1:
                    continue
                if abs(r - mine_r) <= 1 and abs(c - mine_c) <= 1:
                    self._field[r][c] += 1
    
    def get_cell(self, row: int, column: int) -> int | IndexError:
        '''Возвращает -1 если на клетке бомба иначе число'''
        return self._field[row][column]
    
    @property
    def cells(self) -> list[list[int]]:
        '''Минное поле'''
        return [row.copy() for row in self._field]
    
    @property
    def rows(self) -> int:
        '''Количество строк'''
        return self._rows
    
    @property
    def columns(self) -> int:
        '''Количество столбцов'''
        return self._cols    


class GameField:
    '''Виджет с минным полем'''
    def __init__(self, master: ttk.Frame, field_obj: MineField) -> None:
        self._master = master
        self._field = field_obj
        self._undefined_cell_mark = "*"
        self._warning_cell_mark = '!'
        self._mined_cell_mark = "BOOM"
        self._set_root()
        self._set_field()
        
    def _set_root(self) -> None:
        '''Создание корневого объекта'''
        self._root = ttk.Frame(self._master)
        
    def _set_field(self) -> None:
        '''Создание поля'''
        
        self._rows = self._field.rows
        self._cols = self._field.columns
        for r in range(self._rows):
            self._root.rowconfigure(index=r, weight=1)
        
        for c in range(self._cols):
            self._root.columnconfigure(index=c, weight=1)
        
        self._cells: list[list[ttk.Button]] = [
            [
                ttk.Button(
                    self._root,
                    text=self._undefined_cell_mark,
                    width=5
                )
                for _ in range(self._cols)
            ]
            for _ in range(self._rows)
        ]
        
        for r in range(self._rows):
            for c in range(self._cols):
                self._cells[r][c].grid(row=r, column=c)
                self._cells[r][c].bind(
                    '<Button-1>',
                    self._click_cell
                )
                self._cells[r][c].bind(
                    '<Button-3>',
                    self._mark_cell
                )
                
    def _mark_cell(self, e) -> None:
        '''Ставит или убирает метку с клетки при нажатии ПКМ'''
        cell: ttk.Button | Any = e.widget
        if cell['text'] == self._undefined_cell_mark:
            cell.config(text=self._warning_cell_mark)
            self._root.update()
            return
        cell.config(text=self._undefined_cell_mark)
        self._root.update()
    
    def _click_cell(self, e) -> None:
        '''Обработчик нажатия на клетку'''
        cell: ttk.Button | Any = e.widget
        row = cell.grid_info()['row']
        column = cell.grid_info()['column']
        
        if cell['text'] == self._warning_cell_mark:
            return
        
        if self._field.get_cell(row, column) == -1:
            self._reveal_all_cells()
            self._root.update()
            msg.showinfo(title='Поражение', message='Вы проиграли:(')
            return
        
        if self._all_revealed():
            self._reveal_all_cells()
            self._root.update()
            msg.showinfo(title='Победа', message='Вы выиграли!')
            return
                
        if not self._has_mines(row, column):
            self._reveal_area(row, column)
            self._root.update()
            return
        
        self._reveal_cell(row, column)
        self._root.update()
        
    def _reveal_cell(self, row: int, column: int) -> None:
        '''Раскрывает содержимое клетки'''
        val = self._field.get_cell(row, column)
        self._cells[row][column].config(text=f'{val}')
    
    def _has_mines(self, row: int, column: int) -> bool:
        '''Проверяет содержит ли область 3x3 вокруг клетки мины'''
        r_start = row if row - 1 < 0 else row - 1
        r_end = row if row + 1 > self._rows - 1 else row + 1
        
        c_start = column if column - 1 < 0 else column - 1 
        c_end = column if column + 1 > self._cols - 1 else column + 1
        
        for r in range(r_start, r_end + 1):
            for c in range(c_start, c_end + 1):
                if self._cells[r][c]['text'] == self._warning_cell_mark:
                    continue
                if self._field.get_cell(r, c) == -1:
                    return True
        return False
        
    def _reveal_area(self, row: int, column: int) -> None:
        '''Раскрывает значения клеток в области'''
        r_start = row if row - 1 < 0 else row - 1
        r_end = row if row + 1 > self._rows - 1 else row + 1
        
        c_start = column if column - 1 < 0 else column - 1 
        c_end = column if column + 1 > self._cols - 1 else column + 1
        for r in range(r_start, r_end + 1):
            for c in range(c_start, c_end + 1):
                if self._cells[r][c]['text'] == self._warning_cell_mark:
                    continue
                self._reveal_cell(r, c)
                
    def _all_revealed(self) -> bool:
        '''Все пустые клетки были раскрыты'''
        for r in range(self._rows):
            for c in range(self._cols):
                cell_mark = self._cells[r][c]['text']
                if cell_mark == self._undefined_cell_mark \
                    or cell_mark == self._warning_cell_mark:
                    if self._field.get_cell(r, c) == -1:
                        continue
                    return False
        return True
        
    def _reveal_all_cells(self) -> None:
        '''Раскрывает значения всех клеток'''
        for r in range(self._rows):
            for c in range(self._cols):
                val = self._field.get_cell(r, c)
                if val == -1:
                    self._cells[r][c].config(text=self._mined_cell_mark)
                    continue
                self._cells[r][c].config(text=f'{val}')
        
    @property        
    def root(self) -> ttk.Frame:
        '''Виджет на котором все стоит'''
        return self._root


class App:
    def __init__(self) -> None:
        self._app = tk.Tk()
        self._app.wm_protocol("WM_DELETE_WINDOW", self._exit)
        self._app.title('Игра сапер')
        self._field = None
        self._set_root()
        self._set_controls()
    
    def _set_root(self) -> None:
        self._root = ttk.Frame(self._app)
        self._root.pack(expand=True, fill='both')
        
    def _set_controls(self) -> None:
        btns_frame = ttk.Frame(self._root)
        btns_frame.pack(expand=True, fill='x', side='top')
        btns_frame.rowconfigure(index=0, weight=1)
        btns_frame.columnconfigure(index=0, weight=1)
        btns_frame.columnconfigure(index=1, weight=1)
        
        box_frame = ttk.Frame(btns_frame)
        box_frame.grid(row=0, column=0)
        box_frame.rowconfigure(index=0, weight=1)
        box_frame.columnconfigure(index=0, weight=1)
        box_frame.columnconfigure(index=1, weight=1)
        ttk.Label(box_frame, text='Сложность', width=11).grid(row=0, column=0)
        
        self._diff_var = tk.StringVar(value='Легко')
        
        ttk.Combobox(
            box_frame,
            textvariable=self._diff_var,
            values=['Легко', 'Средне', 'Сложно'],
            state='readonly',
            width=9
        ).grid(row=0, column=1)
        
        self._btn_var = tk.StringVar(value='Начать')
        
        ttk.Button(
            btns_frame,
            textvariable=self._btn_var,
            command=self._set_field,
            width=10
        ).grid(row=0, column=1)
        
    def _set_field(self) -> None:
        if self._field is not None:
            self._field.destroy()
            self._root.update()
        match self._diff_var.get():
            case 'Легко':
                field = MineField(5, 5, 4)
            case 'Средне':
                field = MineField(10, 10, 20)
            case 'Сложно':
                field = MineField(20, 20, 40)
            case _:
                pass
        self._field = GameField(self._root, field).root
        self._field.pack(expand=True, fill='both')
    
    def run(self) -> None:
        self._app.mainloop()
        
    def _exit(self) -> None:
        sys.exit() 
         

App().run()
        