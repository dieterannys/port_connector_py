import math
import os
from pprint import pprint as pp


def draw(setup, canvas, file):
    drawdata = prep_drawings(setup)
    draw_canvas(drawdata, canvas, file)
    draw_svg(drawdata, file)


def prep_drawings(setup):
    # Returns a set of labels, lines and circles to be drawn later
    # 1) Determine position of the 'bounding circles' of each cabinet
    # Sizer of each circle (relative)
    data = []
    totals = 0
    for c in sorted(setup["cabinets"]):
        nodes = []
        cables = []
        cable_pos = -1
        for d in sorted(setup["cabinets"][c]):
            cable_pos += 1
            nodes.append("d_" + d)
            #cables.append(-1)
            cables.append([])
            for p in sorted(setup["cabinets"][c][d]):
                cable_pos += 1
                nodes.append("p_" + p)
                #cable_hit = -1
                cables.append([])
                for cable_id in range(len(setup["cables"])):
                    if setup["cables"][cable_id][0] == [c, d, p] or setup["cables"][cable_id][1] == [c, d, p]:
                        #cable_hit = cable_id
                        cables[cable_pos].append(cable_id)
                #cables.append(cable_hit)


        data.append({
            "size": len(nodes),
            "label": c,
            "nodes": nodes,
            "cables": cables
        })
        totals += len(nodes)
    for i in range(len(data)):
        data[i]["size"] += totals


    # ...
    def center_points(sizes):
        r = sum(sizes)
        size_sums = [(sizes[(i-1)  % len(sizes) ] + sizes[(i ) % len(sizes)]) for i in range(len(sizes))]
        angles = [0 for s in size_sums]
        i = 1
        while round(sum([math.degrees(a) for a in angles]), 1) != 360:
            angles = [2 * math.asin(s / (2 * r)) for s in size_sums]
            if sum(angles) < math.radians(360):
                i /= 2
                r -= r * i
            else:
                r += r * i
        # Go from relative to absolute angles

        # ...
        xylist = []
        sumangles = - angles[0]
        for a in angles:
            x = r * math.cos(a + sumangles)
            y = r * math.sin(a + sumangles)
            xylist.append([x, y])
            sumangles += a
        return xylist

    sizes = [data[i]["size"] for i in range(len(data))]
    if len(data) > 2:
        xylist = center_points(sizes)
    elif len(data) == 2:
        r = sum(sizes)
        xylist = [[-r, 0], [0, 0]]
    elif len(data) == 1:
        xylist = [[0, 0]]
    for i in range(len(data)):
        data[i]["x"], data[i]["y"] = xylist[i][0], xylist[i][1]

    return data


def draw_canvas(data, canvas, file):
    try:
        os.remove(file + ".svg")
    except:
        pass
    canvas.delete("all")

    svg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + str(canvas.winfo_width()) + '" height="' + str(canvas.winfo_height()) + '">'

    # Figure out the scaling and moving factors
    canvas_w = canvas.winfo_width() - 10
    canvas_h = canvas.winfo_height() - 10
    data_dim = [10000,0,10000,0]
    for c in data:
        data_dim[0] = min(data_dim[0],c["x"] - c["size"])
        data_dim[1] = max(data_dim[1],c["x"] + c["size"])
        data_dim[2] = min(data_dim[2],c["y"] - c["size"])
        data_dim[3] = max(data_dim[3],c["y"] + c["size"])
    data_w = data_dim[1] - data_dim[0]
    data_h = data_dim[3] - data_dim[2]
    scale_hor = canvas_w / data_w
    scale_vert = canvas_h / data_h
    if scale_vert > scale_hor:
        scale = scale_hor
        delta_x = -data_dim[0] + 5/scale
        delta_y = -data_dim[2] + 5/scale + (canvas_h/scale - data_h)/2
    else:
        scale = scale_vert
        delta_x = -data_dim[0] + 5/scale + (canvas_w/scale - data_w)/2
        delta_y = -data_dim[2] + 5/scale

    # Draw main circles & cabinet labels
    cable_xy = {}
    for c in data:
        x = (c["x"] + delta_x)*scale
        y = (c["y"] + delta_y)*scale
        r = c["size"]*scale - 20
        x1 = (x - r)
        y1 = (y - r)
        x2 = (x + r)
        y2 = (y + r)
        canvas.create_oval(x1,y1,x2,y2,width="3",outline="#BBB")
        svg += '<circle cx="'+str(int(x))+'" cy="'+str(int(y))+'" r="'+str(int(r))+'" fill="none" stroke="#BBB" stroke-width="1"/>'
        canvas.create_text(x,y,text=c["label"])
        svg += '<text x="'+str(int(x))+'" y="'+str(int(y))+'" text-anchor="middle" font-family="Verdana" font-size="16" fill="#BBB">'+c["label"]+'</text>'
        delta_a = math.radians(360) / len(c["nodes"])
        a = - delta_a
        device = ""
        device_a = 0
        cable_hit = -1
        for n in c["nodes"]:
            cable_hit += 1
            a += delta_a




            if n[:1] == "p":
                xm = x + math.cos(a)*r
                ym = y + math.sin(a)*r
                rm = 4
                x1 = (xm - rm)
                y1 = (ym - rm)
                x2 = (xm + rm)
                y2 = (ym + rm)
                text_angle = -(math.degrees(a))
                text_anchor = "e"
                if text_angle <= -90 and text_angle > -270:
                    text_angle += 180
                    text_anchor = "w"
                canvas.create_oval(x1,y1,x2,y2, fill="#FFF",outline="#BBB")
                svg += '<circle cx="'+str(int(xm))+'" cy="'+str(int(ym))+'" r="'+str(int(rm))+'" fill="white" stroke="#BBB" stroke-width="1"/>'
                canvas.create_text(xm,ym,text="   "+n[2:]+"   ",angle=text_angle, anchor=text_anchor)
                if text_anchor == "w":
                    text_anchor = "start"
                else:
                    text_anchor = "end"
                svg += '<text x="'+str(int(xm))+'" y="'+str(int(ym))+'" text-anchor="'+text_anchor+'" transform="rotate('+str(int(-text_angle))+','+str(int(xm))+','+str(int(ym))+')" font-family="Verdana" font-size="9" fill="black">'+"   "+n[2:]+"   "+'</text>'

                for cable in c["cables"][cable_hit]:
                    try:
                        cable_xy[cable].append(xm)
                        cable_xy[cable].append(ym)
                    except:
                        cable_xy[cable] = []
                        cable_xy[cable].append(xm)
                        cable_xy[cable].append(ym)
            elif n[:1] == "d":
                for shift_a in range(-4,+5):
                    xm = x + math.cos(a+shift_a*delta_a*0.1)*r
                    ym = y + math.sin(a+shift_a*delta_a*0.1)*r
                    rm = 15
                    x1 = (xm - rm)
                    y1 = (ym - rm)
                    x2 = (xm + rm)
                    y2 = (ym + rm)
                    canvas.create_oval(x1,y1,x2,y2,fill="#FFF",outline="#FFF")
                a_mid = (a + device_a)/2
                xd = x + math.cos(a_mid)*(r+8)
                yd = y + math.sin(a_mid)*(r+8)

                canvas.create_text(xd,yd,text=device, angle=(math.degrees(-a_mid)+90)%180,font=("Courier New", 12, "bold"))
                device = n[2:]
                device_a = a
        a += delta_a
        a_mid = (a + device_a)/2
        xd = x + math.cos(a_mid)*(r+8)
        yd = y + math.sin(a_mid)*(r+8)
        canvas.create_text(xd,yd,text=device, angle=(math.degrees(-a_mid)+90)%180,font=("Courier New", 12, "bold"))

    for c in cable_xy:
        x1 = cable_xy[c][0]
        y1 = cable_xy[c][1]
        x2 = cable_xy[c][2]
        y2 = cable_xy[c][3]
        canvas.create_line(x1,y1,x2,y2,fill=colorwheel(c,len(cable_xy)))
        canvas.create_oval(x1-5,y1-5,x1+5,y1+5, fill=colorwheel(c,len(cable_xy)))
        canvas.create_oval(x2-5,y2-5,x2+5,y2+5, fill=colorwheel(c,len(cable_xy)))

    svg += "</svg>"

    with open(str(file) + ".svg", "w") as svgfile:
        svgfile.write(svg)

def draw_svg(data, file):
    pass

def colorwheel(i, t):
        colord = 16 ** 3 * .85
        colora = (i / t) * 360
        colorr = hex(int(colord / 2 * math.cos(math.radians(colora + 0)) + colord / 2))
        colorg = hex(int(colord / 2 * math.cos(math.radians(colora + 120)) + colord / 2))
        colorb = hex(int(colord / 2 * math.cos(math.radians(colora + 240)) + colord / 2))
        colorr = str(colorr[2:])
        colorg = str(colorg[2:])
        colorb = str(colorb[2:])
        color = "#"
        for c in [colorr, colorg, colorb]:
            if len(c) == 2:
                c = "0" + c
            elif len(c) == 1:
                c = "00" + c
            color += c
        return color