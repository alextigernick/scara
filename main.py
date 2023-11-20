from solid2 import set_global_fn
from solid2.extensions.bosl2 import *
from solid2.extensions.bosl2.turtle3d import *
from solid2.extensions.bosl2.nema_steppers import *
from solid2.extensions.bosl2.gears import *
import numpy as np
import matplotlib.pyplot as plt
import sympy
import sketch
fn = 50
debug = False
gt2_dims = {
    "pitch":2,
    "pld":0.254,
    "h":0.75,
    "b":0.4,
    "r1":0.15,
    "r2":1,
    "r3":0.555,
    "thickness":1,
}
def get_gt2_outline(fn = 100):
    circle1 = sketch.Circle(0, 0, gt2_dims["r3"])
    circle2 = sketch.Circle(gt2_dims["b"], -(gt2_dims["h"] - gt2_dims["r3"]), gt2_dims["r2"])
    circle3 = sketch.Circle(-gt2_dims["r2"] - gt2_dims["r1"] + gt2_dims["b"], (-gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"]) + gt2_dims["r1"], gt2_dims["r1"])
    circle1.theta1 = circle1.get_theta(circle1.find_intersection(circle2)[0])
    circle1.theta2 = np.pi / 2
    circle2.theta1 = circle2.get_theta(circle1.find_intersection(circle2)[0])
    circle2.theta2 = np.pi
    circle3.theta1 = 0
    circle3.theta2 = -np.pi / 2
    line1 = sketch.Line(-gt2_dims["pitch"] / 2, -gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"], circle3.x, -gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"])
    line2 = sketch.Line(circle3.x + gt2_dims["r1"], circle3.y, circle2.x - gt2_dims["r2"], circle2.y)
    line3 = sketch.Line(-gt2_dims["pitch"] / 2, -gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"]-gt2_dims["thickness"],-gt2_dims["pitch"] / 2, -gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"])
    line4 = sketch.Line(0, -gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"]-gt2_dims["thickness"],-gt2_dims["pitch"] / 2, -gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"]-gt2_dims["thickness"])
    drawing = [line4,line3, line1, circle3, line2, circle2, circle1]
    pts = list(sketch.get_pts(drawing,fn))
    pts[1] -= (-gt2_dims["h"] - gt2_dims["pld"] + gt2_dims["r3"])-gt2_dims["pld"] # offset so x axis is the gt2_dims["pitch"] line
    return sketch.mirror_pts_y(*pts)

def gt2_pulley(num_teeth,thickness,center_hole,do_plates=True):
    major_diameter = num_teeth*gt2_dims["pitch"]/np.pi
    if debug:
        a = get_gt2_outline(fn=3)
    else:
        a = get_gt2_outline(fn=20)
        
    a = [(x,y)for x,y in zip(*a)]
    tooth_poly = polygon(a)
    core = cylinder(h=thickness,d=major_diameter-gt2_dims["pld"]*2)
    tooth = linear_extrude(thickness+2)(tooth_poly).rotateZ(0).down(1)#+(cylinder(r=gt2_dims["r2"],h=thickness).right(b).back(h-gt2_dims["r3"])-cube_mask(thickness).rotateZ(90).back(b/2))+(cylinder(r=gt2_dims["r2"],h=thickness).left(b).back(h-gt2_dims["r3"])-cube_mask(thickness).rotateZ(0).back(b/2))
    teeth = [tooth.back(major_diameter/2).rotateZ(i*360/num_teeth) for i in range(num_teeth)]
    teeth = union()(*teeth) + (cylinder(d=major_diameter+20,h=thickness+2).down(1)-cylinder(d=major_diameter-gt2_dims["pld"]*2,h=thickness+4).down(2))
    plates = cylinder(h=1,d=major_diameter+4).down(1)+cylinder(h=1,d=major_diameter+4).up(thickness)
    hole = cylinder(d=center_hole,h=thickness+20).down(10)
    if not do_plates:
        plates = union()()
    if center_hole == 0:
        return (core-teeth)+plates
    return (core-teeth)+plates-hole
def gt2_gear(num_teeth,thickness,backing_thickness,circ_pitch,pressure_angle=20,):
    hole_diameter = num_teeth*gt2_dims["pitch"]/np.pi - gt2_dims["pld"]*2 - backing_thickness*2 
    print(hole_diameter)
    num_gear_teeth = np.floor(((hole_diameter*np.pi)/circ_pitch))-2
    print()
    pulley = gt2_pulley(num_teeth,thickness,hole_diameter,do_plates=False)
    gear = ring_gear(circ_pitch=circ_pitch, teeth=num_gear_teeth, thickness=thickness,pressure_angle=pressure_angle,backing=1)
    return pulley+gear.up(thickness/2)
cc = gt2_gear(50,8,2,2)
set_global_fn(fn)
cc.save_as_scad()
