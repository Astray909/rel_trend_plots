import os
from tkinter import *

from configparser import ConfigParser
from tkinter.filedialog import askopenfile, askopenfilename
config = ConfigParser()

config_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), '.config') + '\\'

if not os.path.exists(config_dir + 'jhuang_rel_trend_plots\\'):
    os.makedirs(config_dir + 'jhuang_rel_trend_plots\\')

def config_read(mode):
    config.read(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini')
    interval_sel = config.get('interval', 'interval')
    
    rdsonul = config.get('rdson', 'upper')
    rdsonll = config.get('rdson', 'lower')
    rdsontf = config.get('rdson', 'tf')

    vthul = config.get('vth', 'upper')
    vthll = config.get('vth', 'lower')
    vthtf = config.get('vth', 'tf')

    idofful = config.get('idoff', 'upper')
    idoffll = config.get('idoff', 'lower')
    idofftf = config.get('idoff', 'tf')

    igssul = config.get('igss', 'upper')
    igssll = config.get('igss', 'lower')
    igsstf = config.get('igss', 'tf')

    dir_ent = config.get('dir', 'reference')

    if mode == 0:
        return interval_sel, rdsonul, rdsonll, rdsontf, vthul, vthll, vthtf, idofful, idoffll, idofftf, igssul, igssll, igsstf, dir_ent
    elif mode == 1:
        arr = [interval_sel, rdsonul, rdsonll, rdsontf, vthul, vthll, vthtf, idofful, idoffll, idofftf, igssul, igssll, igsstf, dir_ent]
        return arr

def config_write(interval_sel, rdsonul, rdsonll, rdsontf, vthul, vthll, vthtf, idofful, idoffll, idofftf, igssul, igssll, igsstf, dir_ent):
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
    if config.has_section('dir'):
        config.remove_section('dir')

    config.add_section('interval')
    config.set('interval', 'interval', interval_sel)

    config.add_section('rdson')
    config.set('rdson', 'upper', rdsonul)
    config.set('rdson', 'lower', rdsonll)
    config.set('rdson', 'tf', rdsontf)

    config.add_section('vth')
    config.set('vth', 'upper', vthul)
    config.set('vth', 'lower', vthll)
    config.set('vth', 'tf', vthtf)

    config.add_section('idoff')
    config.set('idoff', 'upper', idofful)
    config.set('idoff', 'lower', idoffll)
    config.set('idoff', 'tf', idofftf)

    config.add_section('igss')
    config.set('igss', 'upper', igssul)
    config.set('igss', 'lower', igssll)
    config.set('igss', 'tf', igsstf)

    config.add_section('dir')
    config.set('dir', 'reference', dir_ent)

    with open(config_dir + 'jhuang_rel_trend_plots\\' + 'config.ini', 'w') as f:
        config.write(f)

def gui():
    main = Tk()
    main.title('Configurator')
    def save():
        config_write(interval_sel.get(), rdsonul.get(), rdsonll.get(), rdsontf.get(), vthul.get(), vthll.get(), vthtf.get(), idofful.get(), idoffll.get(), idofftf.get(), igssul.get(), igssll.get(), igsstf.get(), dir_ent.get())
    def save_c():
        save()
        main.destroy()
    def default():
        clear()
        interval_sel.insert(0, 1000)
        rdsonul.insert(0, 150)
        rdsonll.insert(0, -50)
        rdsontf.insert(0, 5)
        vthul.insert(0, 50)
        vthll.insert(0, -50)
        vthtf.insert(0, 5)
        idofful.insert(0, 50)
        idoffll.insert(0, 0)
        idofftf.insert(0, 2)
        igssul.insert(0, 50)
        igssll.insert(0, 0)
        igsstf.insert(0, 2)
    def clear():
        interval_sel.delete(0, END)
        rdsonul.delete(0, END)
        rdsonll.delete(0, END)
        rdsontf.delete(0, END)
        vthul.delete(0, END)
        vthll.delete(0, END)
        vthtf.delete(0, END)
        idofful.delete(0, END)
        idoffll.delete(0, END)
        idofftf.delete(0, END)
        igssul.delete(0, END)
        igssll.delete(0, END)
        igsstf.delete(0, END)
        dir_ent.delete(0, END)
    def read_last():
        clear()
        interval_sel_r, rdsonul_r, rdsonll_r, rdsontf_r, vthul_r, vthll_r, vthtf_r, idofful_r, idoffll_r, idofftf_r, igssul_r, igssll_r, igsstf_r, dir_ent_r = config_read(0)

        interval_sel.insert(0, interval_sel_r)
        rdsonul.insert(0, rdsonul_r)
        rdsonll.insert(0, rdsonll_r)
        rdsontf.insert(0, rdsontf_r)
        vthul.insert(0, vthul_r)
        vthll.insert(0, vthll_r)
        vthtf.insert(0, vthtf_r)
        idofful.insert(0, idofful_r)
        idoffll.insert(0, idoffll_r)
        idofftf.insert(0, idofftf_r)
        igssul.insert(0, igssul_r)
        igssll.insert(0, igssll_r)
        igsstf.insert(0, igsstf_r)
    def file_browse():
        path = askopenfilename()
        dir_ent.delete(0, END)
        dir_ent.insert(0, path)

    main.geometry('750x150')
    Label(main, text = "Enter Interval:").grid(row=0, column=0)

    Label(main, text = "Upper Limit:").grid(row=2, column=0)
    Label(main, text = "Lower Limit:").grid(row=3, column=0)
    Label(main, text = "Tick Frequency:").grid(row=4, column=0)

    Label(main, text = "Rdson:").grid(row=1, column=1)
    Label(main, text = "Vth:").grid(row=1, column=3)
    Label(main, text = "Idoff:").grid(row=1, column=5)
    Label(main, text = "Igss:").grid(row=1, column=7)

    Label(main, text = "Reference File:").grid(row=6, column=0)


    interval_sel = Entry(main)

    rdsonul = Entry(main)
    rdsonll = Entry(main)
    rdsontf = Entry(main)

    vthul = Entry(main)
    vthll = Entry(main)
    vthtf = Entry(main)

    idofful = Entry(main)
    idoffll = Entry(main)
    idofftf = Entry(main)

    igssul = Entry(main)
    igssll = Entry(main)
    igsstf = Entry(main)

    dir_ent = Entry(main)


    interval_sel.grid(row=0, column=1)

    rdsonul.grid(row=2, column=1)
    rdsonll.grid(row=3, column=1)
    rdsontf.grid(row=4, column=1)

    vthul.grid(row=2, column=3)
    vthll.grid(row=3, column=3)
    vthtf.grid(row=4, column=3)

    idofful.grid(row=2, column=5)
    idoffll.grid(row=3, column=5)
    idofftf.grid(row=4, column=5)

    igssul.grid(row=2, column=7)
    igssll.grid(row=3, column=7)
    igsstf.grid(row=4, column=7)

    dir_ent.grid(row=6, column=1, columnspan=5, sticky=EW)


    Button(main, text='Save and Continue', bg = "#5fb878", command=save_c).grid(row=6, column=9, sticky=EW)
    Button(main, text='Default', command=default).grid(row=0, column=8, sticky=EW)
    Button(main, text='Clear', command=clear).grid(row=1, column=8, sticky=EW)
    Button(main, text='Save', command=save).grid(row=0, column=9, sticky=EW)
    Button(main, text='Load Last Saved', command=read_last).grid(row=1, column=9, sticky=EW)
    Button(main, text='Browse', command=file_browse).grid(row=6, column=7, sticky=EW)

    default()
    mainloop()