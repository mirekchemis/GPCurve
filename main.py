import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from matplotlib import pyplot
from matplotlib.widgets import Button as bt
import numpy as np
import pdfplumber
from statistics import mean
import pandas as pd


def main():
    def clear():
        lb1.delete(1, END)
        lb2.delete(1, END)
        entry_ff.delete(0, END)
        entry_ff.insert(0, '6,00')
        entry_sf.delete(0, END)
        entry_sf.insert(0, '10,00')
        entry_sp.delete(0, END)
        entry_sp.insert(0, 'auto')
        entry_ep.delete(0, END)
        entry_ep.insert(0, 'auto')
        entry_sb.delete(0, END)
        entry_sb.insert(0, 'auto')
        entry_eb.delete(0, END)
        entry_eb.insert(0, 'auto')

    def copy(event):
        print("doing copy")

    def start():

        flag1 = str(entry_ff.get())
        flag2 = str(entry_sf.get())
        input1 = str(lb1.get(1))
        input2 = str(lb2.get(1))
        if input2 != '':
            with open('const.txt', 'w') as fi:
                fi.write(input2)

        if '.pdf' not in input2:
            input1_pdf = input1.replace('.txt', '.pdf')
            print(input1_pdf)
            print(input1)
            with pdfplumber.open(input1_pdf) as pdf:
                page = pdf.pages[0]
                dt = page.extract_tables(table_settings={})
            dt = dt[0]
            for i in range(len(dt)):
                for j in range(len(dt[i])):
                    test = str(dt[i][j])
                    if 'Sequence' in test:
                        prefix = test
            prefix = prefix.split('\n')
            for i in range(len(prefix)):
                if 'Sequence' in str(prefix[i]):
                    prefix1 = str(prefix[i])
                    break
            prefix1 = prefix1.split(' ')
            for i in range(len(prefix1)):
                if '(' in str(prefix1[i]):
                    pr = str(prefix1[i])
                    break
            prefix = pr[6] + pr[7] + pr[8] + pr[9] + pr[3] + pr[4] + pr[0] + pr[1] + pr[-3] + pr[-2]
            name2 = input2 + '/' + prefix + '.pdf'
        else:
            name2 = input2
        print(name2)

        with pdfplumber.open(name2) as pdf:
            page = pdf.pages[0]
            ct = page.extract_tables(table_settings={})
        for i in range(len(ct)):
            for j in range(len(ct[i])):
                if ct[i][j] == ['C0', 'C1', 'C2', 'C3']:
                    const = ct[i][j + 1]
        for i in range(len(const)):
            const[i] = const[i].replace(' ', '')
            const[i] = const[i].replace(',', '.')
            const[i] = float(const[i])
        print('C0 - C3 = ' + str(const))

        with open(lb1.get(1)) as f:
            data = f.readlines()

        finished = False
        while not finished:
            if flag1 in data[0]:
                finished = True
            else:
                data.pop(0)
        finished = False
        while not finished:
            if flag2 in data[-1]:
                finished = True
            else:
                data.pop(-1)
        x = []
        vol = []
        y = []
        for i in range(len(data)):
            data[i] = data[i].replace('\n', '')
            data[i] = data[i].replace(',', '.')
            li = data[i].split('\t')
            vl = float(li[0])
            vol.append(vl)
            lgm = const[0] + const[1] * vl + const[2] * vl * vl + const[3] * vl ** 3
            x.append(lgm)
            y.append(float(li[2]))

        y_min = min(y)
        for i in range(len(y)):
            y[i] = y[i] - y_min
        y_max = max(y)
        for i in range(len(y)):
            y[i] = y[i] / y_max

        index_max = y.index(max(y))
        fig, axes = pyplot.subplots(1, 1, figsize=(9.0, 8.0), sharex=True)
        ax1 = axes
        ax1.plot(x, y, 'k--', label='original')
        ax1.set_xlim(ax1.get_xlim()[::-1])
        ax_copy = fig.add_axes([0.9, 0.2, 0.1, 0.075])
        b_copy = bt(ax_copy, 'Copy')
        b_copy.on_clicked(copy)
        x_np = np.array(x)
        y_np = np.array(y)

        sp = str(entry_sp.get())
        ep = str(entry_ep.get())
        count = 0
        if 'auto' in sp:
            index_left_min = index_max
            flag = True
            while flag:
                if y[index_left_min - 1] <= y[index_left_min]:
                    index_left_min -= 1
                else:
                    flag = False
        else:
            count = 1
            index_left_min = x.index(min(x, key=lambda xx: abs(xx - float(sp))))

        if 'auto' in ep:
            index_right_min = index_max
            flag = True
            while flag:
                if y[index_right_min + 1] <= y[index_right_min]:
                    index_right_min += 1
                else:
                    flag = False
        else:
            if count == 1 and sp <= ep:
                raise 'start lgM must be greater then end lgM'
            index_right_min = x.index(min(x, key=lambda xx: abs(xx - float(ep))))

        x_line = x_np[index_left_min], x_np[index_right_min]
        y_base = min(y_np[index_left_min], y_np[index_right_min])
        y_line = [y_base, y_base]

        sb = str(entry_sb.get())
        eb = str(entry_eb.get())
        if 'auto' not in sb:
            y_line[0] = float(sb)
        if 'auto' not in eb:
            y_line[1] = float(eb)

        k_line = -(y_line[1] - y_line[0]) / (x_line[0] - x_line[1])
        b_line = y_line[0] - k_line * x_line[0]
        ax1.plot(x_line, y_line, 'xr-')
        # ax1.fill_between(x, y, y_base, where=(x >= x[index_right_min]) & (x <= x[index_left_min]), color='red')

        x_peak = []
        vol_peak = []
        y_peak = []
        m_peak = []

        for i in range(index_right_min - index_left_min + 1):
            x_peak.append(x[i + index_left_min])
            vol_peak.append(vol[i + index_left_min])
            m_peak.append(10 ** x[i + index_left_min])
            y_peak.append(y[i + index_left_min] - (k_line * x[i + index_left_min] + b_line))

        m_avg = []
        slice_start = []
        slice_end = []
        slice_avg = []
        i_start = []
        i_end = []
        i_avg = []
        slice_area = []
        sa_m = []
        sa_d_m = []

        for i in range(len(x_peak) - 1):
            m_avg.append((m_peak[i] + m_peak[i + 1]) / 2)
            slice_start.append(vol_peak[i])
            slice_end.append(vol_peak[i + 1])
            slice_avg.append((slice_start[i] + slice_end[i]) / 2)
            i_start.append(y_peak[i])
            i_end.append(y_peak[i + 1])
            i_avg.append((i_start[i] + i_end[i]) / 2)
            slice_area.append(i_avg[i] * abs(slice_end[i] - slice_start[i]))
            sa_m.append(slice_area[i] * m_avg[i])
            sa_d_m.append(slice_area[i] / m_avg[i])

        m_n = sum(slice_area) / sum(sa_d_m)
        m_w = sum(sa_m) / sum(slice_area)
        mwd = m_w / m_n

        print('Mn = ' + str(m_n))
        print('Mw = ' + str(m_w))
        print('Mw/Mn = ' + str(mwd))
        print('peak area = ' + str(sum(slice_area)))
        print('number of slices = ' + str(len(x_peak) - 1))
        ax1.plot(x_peak, y_peak, 'b-')

        pyplot.show()

    root = TkinterDnD.Tk()  # instead of tk.Tk()
    root.geometry("350x300")

    for c in range(3):
        root.columnconfigure(index=c, weight=1)
    for r in range(10):
        root.rowconfigure(index=r, weight=1)

    lb1 = tk.Listbox(root, width=10, height=1)
    lb1.insert(1, "drag GPC txt data file")
    lb1.drop_target_register(DND_FILES)
    lb1.dnd_bind('<<Drop>>', lambda e: lb1.insert(tk.END, e.data))
    lb1.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="news")

    lb2 = tk.Listbox(root, width=10, height=1)
    lb2.insert(1, "drag constants pdf data file or folder")
    try:
        with open('const.txt') as f:
            const = f.read()
        lb2.insert(2, const)
    except:
        print("no const.txt file")
    lb2.drop_target_register(DND_FILES)
    lb2.dnd_bind('<<Drop>>', lambda e: lb2.insert(tk.END, e.data))
    lb2.grid(column=0, row=2, columnspan=3, rowspan=2, sticky="news")

    button_start = Button(root, text="START", command=start)
    button_start.grid(column=0, row=4, rowspan=3, sticky="news")

    button_clear = Button(root, text="CLEAR", command=clear)
    button_clear.grid(column=0, row=7, rowspan=3, sticky="news")

    label_first_flag = ttk.Label(text="first flag")
    label_first_flag.configure(anchor="center")
    label_first_flag.grid(column=1, row=4, sticky="news")

    entry_ff = Entry(root, width=10)
    entry_ff.insert(0, '6,00')
    entry_ff.grid(column=2, row=4)

    label_second_flag = ttk.Label(text="second flag")
    label_second_flag.configure(anchor="center")
    label_second_flag.grid(column=1, row=5, sticky="news")

    entry_sf = Entry(root, width=10)
    entry_sf.insert(0, '10,00')
    entry_sf.grid(column=2, row=5)

    label_sp = ttk.Label(text="start lgM(.)")
    label_sp.configure(anchor="center")
    label_sp.grid(column=1, row=6, sticky="news")

    entry_sp = Entry(root, width=10)
    entry_sp.insert(0, 'auto')
    entry_sp.grid(column=2, row=6)

    label_ep = ttk.Label(text="end lgM(.)")
    label_ep.configure(anchor="center")
    label_ep.grid(column=1, row=7, sticky="news")

    entry_ep = Entry(root, width=10)
    entry_ep.insert(0, 'auto')
    entry_ep.grid(column=2, row=7)

    label_sb = ttk.Label(text="start base(.)")
    label_sb.configure(anchor="center")
    label_sb.grid(column=1, row=8, sticky="news")

    entry_sb = Entry(root, width=10)
    entry_sb.insert(0, 'auto')
    entry_sb.grid(column=2, row=8)

    label_eb = ttk.Label(text="end base(.)")
    label_eb.configure(anchor="center")
    label_eb.grid(column=1, row=9, sticky="news")

    entry_eb = Entry(root, width=10)
    entry_eb.insert(0, 'auto')
    entry_eb.grid(column=2, row=9)

    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
