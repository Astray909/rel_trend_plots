import os
from tkinter import *

from configparser import ConfigParser
config = ConfigParser()

config_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), '.config') + '\\'

if not os.path.exists(config_dir + 'jhuang_rel_trend_plots\\'):
    os.makedirs(config_dir + 'jhuang_rel_trend_plots\\')

def config_read(mode):
    config.read(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini')
    interval_sel = config.get('interval', 'interval')
    
    rdsonul = config.get('rdson', 'upper')
    rdsonll = config.get('rdson', 'lower')

    vthul = config.get('vth', 'upper')
    vthll = config.get('vth', 'lower')

    idofful = config.get('idoff', 'upper')
    idoffll = config.get('idoff', 'lower')

    igssul = config.get('igss', 'upper')
    igssll = config.get('igss', 'lower')

    if mode == 0:
        return interval_sel, rdsonul, rdsonll, vthul, vthll, idofful, idoffll, igssul, igssll
    elif mode == 1:
        arr = [interval_sel, rdsonul, rdsonll, vthul, vthll, idofful, idoffll, igssul, igssll]
        return arr

def config_write(interval_sel, rdsonul, rdsonll, vthul, vthll, idofful, idoffll, igssul, igssll):
    config.read(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini')
    if config.has_section('interval'):
        config.remove_section('interval')
    if config.has_section('rdson'):
        config.remove_section('rdson')
    if config.has_section('vth'):
        config.remove_section('vth')
    if config.has_section('idoff'):
        config.remove_section('idoff')
    if config.has_section('igss'):
        config.remove_section('igss')

    config.add_section('interval')
    config.set('interval', 'interval', interval_sel)

    config.add_section('rdson')
    config.set('rdson', 'upper', rdsonul)
    config.set('rdson', 'lower', rdsonll)

    config.add_section('vth')
    config.set('vth', 'upper', vthul)
    config.set('vth', 'lower', vthll)

    config.add_section('idoff')
    config.set('idoff', 'upper', idofful)
    config.set('idoff', 'lower', idoffll)

    config.add_section('igss')
    config.set('igss', 'upper', igssul)
    config.set('igss', 'lower', igssll)

    with open(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini', 'w') as f:
        config.write(f)

def gui():
    main = Tk()
    main.title('Configurator')
    def save():
        config_write(interval_sel.get(), rdsonul.get(), rdsonll.get(), vthul.get(), vthll.get(), idofful.get(), idoffll.get(), igssul.get(), igssll.get())
    def save_c():
        save()
        main.destroy()
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
    def read_last():
        clear()
        interval_sel_r, rdsonul_r, rdsonll_r, vthul_r, vthll_r, idofful_r, idoffll_r, igssul_r, igssll_r = config_read(0)

        interval_sel.insert(0, interval_sel_r)
        rdsonul.insert(0, rdsonul_r)
        rdsonll.insert(0, rdsonll_r)
        vthul.insert(0, vthul_r)
        vthll.insert(0, vthll_r)
        idofful.insert(0, idofful_r)
        idoffll.insert(0, idoffll_r)
        igssul.insert(0, igssul_r)
        igssll.insert(0, igssll_r)

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


    Button(main, text='Save and Continue', command=save_c).grid(row=4, column=0, sticky=W)
    Button(main, text='Default', command=default).grid(row=0, column=3, sticky=W)
    Button(main, text='Clear', command=clear).grid(row=0, column=5, sticky=W)
    Button(main, text='Save', command=save).grid(row=0, column=6, sticky=W)
    Button(main, text='Load Last Saved', command=read_last).grid(row=0, column=7, sticky=W)

    default()
    mainloop()