from pc_dataman import *
from pc_drawer import *
from tkinter import *
from tkinter import ttk

s_active = None


# =====================================================================
# GUI FUNCTIONS
# =====================================================================

def pc_init():
    # Fill Setups listbox with datafiles in folder
    for s in get_setup_files():
        s_lb.insert(END, s)


def s_lb_click(e):
    global s_active
    # Save previous setup to file
    if s_active != None:
        data_to_txt(s_active)
    # Load selected setup file into setup data
    s_active = get_selected(s_lb)
    txt_to_data(s_active)
    # Erase all lists and fill cabs list and cables list 1
    erase_lists([c_lb, d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(c_lb, get_children([]))
    fill_list(cables_lb1, get_cable_ports())
    draw(get_setup(),canvas,s_active)


def s_i_enter(e):
    global s_active
    if s_active != None:
        data_to_txt(s_active)
    s_active = s_i.get()
    reset_setup()
    data_to_txt(s_active)
    erase_lists([s_lb,c_lb, d_lb, p_lb, cables_lb1, cables_lb2])
    for s in get_setup_files():
        s_lb.insert(END, s)
    set_selected(s_lb,s_active)
    s_i.delete(0,END)
    draw(get_setup(),canvas,s_active)

def s_bd_click(e):
    pass


def s_bc_click(e):
    pass


def s_br_click(e):
    pass


def c_lb_click(e):
    erase_lists([d_lb, p_lb])
    fill_list(d_lb, get_children([get_selected(c_lb)]))


def c_i_enter(e):
    add_cabinet(c_i.get())
    erase_lists([c_lb, d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(c_lb, get_children([]))
    fill_list(cables_lb1, get_cable_ports())
    c_i.delete(0, END)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def c_bd_click(e):
    del_item(get_selected(c_lb))
    erase_lists([c_lb, d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(c_lb, get_children([]))
    fill_list(cables_lb1, get_cable_ports())
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def c_br_click(e):
    ren_item(c_i.get(),get_selected(c_lb))
    erase_lists([c_lb, d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(c_lb, get_children([]))
    fill_list(cables_lb1, get_cable_ports())
    c_i.delete(0, END)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def d_lb_click(e):
    erase_lists([p_lb])
    fill_list(p_lb, get_children([get_selected(c_lb), get_selected(d_lb)]))


def d_i_enter(e):
    add_device(get_selected(c_lb), d_i.get())
    erase_lists([d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(d_lb, get_children([get_selected(c_lb)]))
    fill_list(cables_lb1, get_cable_ports())
    d_i.delete(0, END)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def d_bd_click(e):
    del_item(get_selected(c_lb), get_selected(d_lb))
    erase_lists([d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(d_lb, get_children([get_selected(c_lb)]))
    fill_list(cables_lb1, get_cable_ports())
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def d_br_click(e):
    ren_item(d_i.get(),get_selected(c_lb), get_selected(d_lb))
    erase_lists([d_lb, p_lb, cables_lb1, cables_lb2])
    fill_list(d_lb, get_children([get_selected(c_lb)]))
    fill_list(cables_lb1, get_cable_ports())
    d_i.delete(0, END)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def d_ccb_click(e):
    pass


def d_mcb_click(e):
    pass


def p_lb_click(e):
    pass


def p_i_enter(e):
    add_port(get_selected(c_lb), get_selected(d_lb), p_i.get())
    erase_lists([p_lb, cables_lb1, cables_lb2])
    fill_list(p_lb, get_children([get_selected(c_lb), get_selected(d_lb)]))
    fill_list(cables_lb1, get_cable_ports())
    p_i.delete(0, END)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def p_bd_click(e):
    del_item(get_selected(c_lb), get_selected(d_lb), get_selected(p_lb))
    erase_lists([p_lb, cables_lb1, cables_lb2])
    fill_list(p_lb, get_children([get_selected(c_lb), get_selected(d_lb)]))
    fill_list(cables_lb1, get_cable_ports())
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def p_br_click(e):
    ren_item(p_i.get(),get_selected(c_lb), get_selected(d_lb), get_selected(p_lb))
    erase_lists([p_lb, cables_lb1, cables_lb2])
    fill_list(p_lb, get_children([get_selected(c_lb), get_selected(d_lb)]))
    fill_list(cables_lb1, get_cable_ports())
    p_i.delete(0, END)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)


def cables_lb1_click(e):
    erase_lists([cables_lb2])
    fill_list(cables_lb2, get_cable_ports())
    cables_lb2.delete(cables_lb1.curselection()[0])
    cables_lb2.insert(END, "--- DISCONNECTED ---")
    c, d, p = tuple(get_selected(cables_lb1)[1:].replace("]", "").split("["))
    connections = get_connections(c, d, p)
    if len(connections) == 0:
        set_selected(cables_lb2,"--- DISCONNECTED ---")
    for port in connections:
        set_selected(cables_lb2,"[{}][{}][{}]".format(port[0],port[1],port[2]))



def cables_lb2_click(e):
    c1, d1, p1 = tuple(get_selected(cables_lb1)[1:].replace("]", "").split("["))
    del_connection(c1, d1, p1)
    if get_selected(cables_lb2) == "--- DISCONNECTED ---":
        data_to_txt(s_active)
        draw(get_setup(),canvas,s_active)
        return
    for i in cables_lb2.curselection():
        c2, d2, p2 = tuple((cables_lb2.get(i))[1:].replace("]", "").split("["))
        set_connection(c1, d1, p1, c2, d2, p2)
    data_to_txt(s_active)
    draw(get_setup(),canvas,s_active)





# =====================================================================
# List Manipulation Helper Functions
# =====================================================================

def get_selected(list):
    # Gets the name of the selected item in a list
    return list.get(list.curselection()[0])


def set_selected(list, item):
    # Selects a specific item in a list by name
    i = 0
    while list.get(i) != "":
        if list.get(i) == item:
            list.select_set(i)
            return
        i += 1


def erase_lists(lists_list):
    for list in lists_list:
        list.delete(0, END)


def fill_list(list, items):
    for item in sorted(items):
        list.insert(END, item)


def get_cable_ports():
    port_list = []
    for c in sorted(get_children([])):
        for d in sorted(get_children([c])):
            for p in sorted(get_children([c, d])):
                port_list.append("[%s][%s][%s]" % (c, d, p))
    return port_list

def window_resize(e):
    draw(get_setup(),canvas,s_active)


# =====================================================================
# GUI INTERFACE
# =====================================================================

root = Tk()

canvas = Canvas(root, bg="#FFF")

canvas.grid(row=0, column=0, rowspan=18, sticky=N + S + W + E)

s_l = Label(root, text="Setups")
s_lb = Listbox(root, height=0, selectmode=SINGLE, exportselection=False)
s_i = Entry(root)
s_bd = Button(root, text="Del")
s_bc = Button(root, text="Cop")
s_br = Button(root, text="Ren")

s_l.grid(row=0, column=1, columnspan=3, sticky=N + S + W + E)
s_lb.grid(row=1, column=1, columnspan=3, sticky=N + S + W + E)
s_i.grid(row=2, column=1, columnspan=3, sticky=N + S + W + E)
s_bd.grid(row=3, column=1, sticky=N + S + W + E)
s_bc.grid(row=3, column=2, sticky=N + S + W + E)
s_br.grid(row=3, column=3, sticky=N + S + W + E)

s_lb.bind("<ButtonRelease-1>", s_lb_click)
s_i.bind("<Return>", s_i_enter)
s_bd.bind("<ButtonRelease-1>", s_bd_click)
s_bc.bind("<ButtonRelease-1>", s_bc_click)
s_br.bind("<ButtonRelease-1>", s_br_click)

c_l = Label(root, text="Cabinets")
c_lb = Listbox(root, height=0, selectmode=SINGLE, exportselection=False)
c_i = Entry(root)
c_bd = Button(root, text="Del")
c_br = Button(root, text="Ren")

c_l.grid(row=4, column=1, columnspan=3, sticky=N + S + W + E)
c_lb.grid(row=5, column=1, columnspan=3, sticky=N + S + W + E)
c_i.grid(row=6, column=1, columnspan=3, sticky=N + S + W + E)
c_bd.grid(row=7, column=1, sticky=N + S + W + E)
c_br.grid(row=7, column=3, sticky=N + S + W + E)

c_lb.bind("<ButtonRelease-1>", c_lb_click)
c_i.bind("<Return>", c_i_enter)
c_bd.bind("<ButtonRelease-1>", c_bd_click)
c_br.bind("<ButtonRelease-1>", c_br_click)

d_l = Label(root, text="Devices")
d_lb = Listbox(root, height=0, selectmode=SINGLE, exportselection=False)
d_i = Entry(root)
d_bd = Button(root, text="Del")
d_br = Button(root, text="Ren")
d_cl = Label(root, text="Copy to cabinet")
d_ccb = ttk.Combobox(root, width=0)
d_ml = Label(root, text="Move to cabinet")
d_mcb = ttk.Combobox(root, width=0)

d_l.grid(row=8, column=1, columnspan=3, sticky=N + S + W + E)
d_lb.grid(row=9, column=1, columnspan=3, sticky=N + S + W + E)
d_i.grid(row=10, column=1, columnspan=3, sticky=N + S + W + E)
d_bd.grid(row=11, column=1, sticky=N + S + W + E)
d_br.grid(row=11, column=3, sticky=N + S + W + E)
d_cl.grid(row=12, column=1, columnspan=2, sticky=N + S + E)
d_ccb.grid(row=12, column=3, sticky=N + S + W + E)
d_ml.grid(row=13, column=1, columnspan=2, sticky=N + S + E)
d_mcb.grid(row=13, column=3, sticky=N + S + W + E)

d_lb.bind("<ButtonRelease-1>", d_lb_click)
d_i.bind("<Return>", d_i_enter)
d_bd.bind("<ButtonRelease-1>", d_bd_click)
d_br.bind("<ButtonRelease-1>", d_br_click)
d_ccb.bind("<<ComboboxSelected>>", d_ccb_click)
d_mcb.bind("<<ComboboxSelected>>", d_mcb_click)

p_l = Label(root, text="Ports")
p_lb = Listbox(root, height=0, selectmode=SINGLE, exportselection=False)
p_i = Entry(root)
p_bd = Button(root, text="Del")
p_br = Button(root, text="Ren")

p_l.grid(row=14, column=1, columnspan=3, sticky=N + S + W + E)
p_lb.grid(row=15, column=1, columnspan=3, sticky=N + S + W + E)
p_i.grid(row=16, column=1, columnspan=3, sticky=N + S + W + E)
p_bd.grid(row=17, column=1, sticky=N + S + W + E)
p_br.grid(row=17, column=3, sticky=N + S + W + E)

p_lb.bind("<ButtonRelease-1>", p_lb_click)
p_i.bind("<Return>", p_i_enter)
p_bd.bind("<ButtonRelease-1>", p_bd_click)
p_br.bind("<ButtonRelease-1>", p_br_click)

cables_lb1 = Listbox(root, selectmode=SINGLE, exportselection=False)
cables_lb2 = Listbox(root, selectmode=EXTENDED, exportselection=False)

cables_lb1.grid(row=0, column=4, rowspan=9, sticky=N + S + W + E)
cables_lb2.grid(row=9, column=4, rowspan=9, sticky=N + S + W + E)

cables_lb1.bind("<ButtonRelease-1>", cables_lb1_click)
cables_lb2.bind("<ButtonRelease-1>", cables_lb2_click)

root.columnconfigure(0, weight=15)
root.columnconfigure(1, weight=1, minsize=50)
root.columnconfigure(2, weight=1, minsize=50)
root.columnconfigure(3, weight=1, minsize=50)
root.columnconfigure(4, weight=4, minsize=200)

root.rowconfigure(1, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(9, weight=2)
root.rowconfigure(15, weight=2)

canvas.bind("<Configure>", window_resize)
root.state('zoomed')
root.wm_title("Port Connector 0.1 (c) 2016, Dieter Annys")

pc_init()

root.mainloop()
