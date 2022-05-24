import os
from tkinter import *

from configparser import ConfigParser
config = ConfigParser()

config_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), '.config') + '\\'

if not os.path.exists(config_dir + 'jhuang_rel_trend_plots\\'):
    os.makedirs(config_dir + 'jhuang_rel_trend_plots\\')

def config_read():
    config.read(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini')

    print(config.get('main', 'key1'))
    print(config.get('main', 'key2'))
    print(config.get('main', 'key3'))

def config_write():
    config.read(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini')
    if config.has_section('main'):
        config.remove_section('main')
    config.add_section('main')
    config.set('main', 'key1', 'value1')
    config.set('main', 'key2', 'value2')
    config.set('main', 'key3', 'value3')
    with open(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini', 'w') as f:
        config.write(f)

def gui():
    main = Tk()
    main.title('Configurator')
    def save():
        print(interval_sel.get())
        config_write()
        config_read()
    def default():
        clear()
        interval_sel.insert(0, 1000)
        rdsonul.insert(0, 150)
        rdsonll.insert(0, -50)
        vthul.insert(0, 50)
        vthll.insert(0, -50)
        idofful.insert(0, 50)
        idoffll.insert(0, 0)
        igssul.insert(0, 50)
        igssll.insert(0, 0)
    def clear():
        interval_sel.delete(0, END)
        rdsonul.delete(0, END)
        rdsonll.delete(0, END)
        vthul.delete(0, END)
        vthll.delete(0, END)
        idofful.delete(0, END)
        idoffll.delete(0, END)
        igssul.delete(0, END)
        igssll.delete(0, END)

    main.geometry('800x100')
    Label(main, text = "Enter Interval:").grid(row=0, column=0)

    Label(main, text = "Rdson UL:").grid(row=1, column=0)
    Label(main, text = "Rdson LL:").grid(row=2, column=0)

    Label(main, text = "Vth UL:").grid(row=1, column=2)
    Label(main, text = "Vth LL:").grid(row=2, column=2)

    Label(main, text = "Idoff UL:").grid(row=1, column=4)
    Label(main, text = "Idoff LL:").grid(row=2, column=4)

    Label(main, text = "Igss UL:").grid(row=1, column=6)
    Label(main, text = "Igss LL:").grid(row=2, column=6)


    interval_sel = Entry(main)

    rdsonul = Entry(main)
    rdsonll = Entry(main)

    vthul = Entry(main)
    vthll = Entry(main)

    idofful = Entry(main)
    idoffll = Entry(main)

    igssul = Entry(main)
    igssll = Entry(main)


    interval_sel.grid(row=0, column=1)

    rdsonul.grid(row=1, column=1)
    rdsonll.grid(row=2, column=1)

    vthul.grid(row=1, column=3)
    vthll.grid(row=2, column=3)

    idofful.grid(row=1, column=5)
    idoffll.grid(row=2, column=5)

    igssul.grid(row=1, column=7)
    igssll.grid(row=2, column=7)


    Button(main, text='Quit', command=main.destroy).grid(row=4, column=0, sticky=W)
    Button(main, text='Default', command=default).grid(row=0, column=3, sticky=W)
    Button(main, text='Clear', command=clear).grid(row=0, column=4, sticky=W)
    Button(main, text='Save', command=save).grid(row=0, column=5, sticky=W)

    mainloop()