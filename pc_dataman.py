import os

# Dictionary with:
setup = {"cabinets": {}, "cables": []}


# ====================================================================================================

def reset_setup():
    global setup
    setup = {"cabinets": {}, "cables": []}

def data_to_txt(file):
    data = ""
    try:
        for c in setup["cabinets"]:
            data += "#" + c + "\n"
            for d in setup["cabinets"][c]:
                data += "##" + d + ":"
                for p in setup["cabinets"][c][d]:
                    data += p + ","
                data = data[:-1] + "\n"
        for c in setup["cables"]:
            data += ",".join(c[0] + c[1]) + "\n"
        data = data[:-1]
    except:
        pass
    with open(file + ".txt", 'w') as fo:
        fo.write(data)


def txt_to_data(file):
    global setup
    reset_setup()
    fo = open(file + ".txt", 'r')
    curr_cab = ""
    curr_dev = ""
    for line in fo.readlines():
        line = line.replace("\n", "")
        if line[0:2] == "##":
            data = line[2:]
            data = data.split(":")
            curr_dev = data[0]
            setup["cabinets"][curr_cab][curr_dev] = {}
            if len(data) == 1:
                continue
            data = data[1].split(",")
            for port in data:
                setup["cabinets"][curr_cab][curr_dev][port] = None
        elif line[0] == "#":
            curr_cab = line[1:]
            setup["cabinets"][curr_cab] = {}
        else:
            data = line.split(",")
            setup["cables"].append([[data[0], data[1], data[2]], [data[3], data[4], data[5]]])
    fo.close()

# ====================================================================================================


def get_setup_files():
    return [x[:-4] for x in os.listdir(os.getcwd()) if x[-4:] == ".txt"]


def get_children(parents):
    # Returns a list of children for specific parents
    cur_parent = setup["cabinets"]
    for parent in parents:
        cur_parent = cur_parent[parent]
    return cur_parent.keys()


def add_cabinet(name):
    setup["cabinets"][name] = {}


def add_device(cabinet, name):
    setup["cabinets"][cabinet][name] = {}


def add_port(cabinet, device, name):
    setup["cabinets"][cabinet][device][name] = {}


def del_item(c, d=None, p=None):
    if d is not None and p is not None:
        del setup["cabinets"][c][d][p]
    elif d is not None:
        del setup["cabinets"][c][d]
    else:
        del setup["cabinets"][c]

def ren_item(newname,c, d=None, p=None):
    if d is not None and p is not None:
        setup["cabinets"][c][d][newname] = setup["cabinets"][c][d][p]
        del setup["cabinets"][c][d][p]
        for i in range(len(setup["cables"])):
            if setup["cables"][i][0][2] == p and setup["cables"][i][0][1] == d and setup["cables"][i][0][0] == c:
                setup["cables"][i][0][2] = newname
            if setup["cables"][i][1][2] == p and setup["cables"][i][1][1] == d and setup["cables"][i][1][0] == c:
                setup["cables"][i][1][2] = newname
    elif d is not None:
        setup["cabinets"][c][newname] = setup["cabinets"][c][d]
        del setup["cabinets"][c][d]
        for i in range(len(setup["cables"])):
            if setup["cables"][i][0][1] == d and setup["cables"][i][0][0] == c:
                setup["cables"][i][0][1] = newname
            if setup["cables"][i][1][1] == d and setup["cables"][i][1][0] == c:
                setup["cables"][i][1][1] = newname
    else:
        setup["cabinets"][newname] = setup["cabinets"][c]
        del setup["cabinets"][c]
        for i in range(len(setup["cables"])):
            if setup["cables"][i][0][0] == c:
                setup["cables"][i][0][0] = newname
            if setup["cables"][i][1][0] == c:
                setup["cables"][i][1][0] = newname


def get_connections(c, d, p):
    connections = []
    for cable in setup["cables"]:
        if cable[0][0] == c and cable[0][1] == d and cable[0][2] == p:
            connections.append(cable[1])
        elif cable[1][0] == c and cable[1][1] == d and cable[1][2] == p:
            connections.append(cable[0])
    return connections

def del_connection(c, d, p):
    continue_deleting = True
    range_cables = len(setup["cables"])
    while continue_deleting:
        for i in range(range_cables):
            if tuple(setup["cables"][i][0]) == (c,d,p) or tuple(setup["cables"][i][1]) == (c,d,p):
                del setup["cables"][i]
                range_cables -= 1
                break
            if i + 1 == range_cables:
                continue_deleting = False

def set_connection(c1, d1, p1, c2, d2, p2):
    # for ci in range(len(setup["cables"])):
    #     cable = setup["cables"][ci]
    #     if cable[0] == [c1, d1, p1] or cable[1] == [c1, d1, p1] or cable[0] == [c2, d2, p2] or cable[1] == [c2, d2, p2]:
    #         del setup["cables"][ci]
    setup["cables"].append([[c1,d1,p1],[c2,d2,p2]])

def get_setup():
    return setup