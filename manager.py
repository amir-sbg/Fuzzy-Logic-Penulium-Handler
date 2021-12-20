# -*- coding: utf-8 -*-

# python imports
from copy import deepcopy
from time import time, sleep

# manual fuzzification and defuzzification imports
import inference
import defuzzification
import fuzzification

# project imports
from simulator import Simulator
from gui import GUI


class Manager:

    def __init__(self, world, controller, dt=0.1, fps=60, monitor_width=1200, monitor_height=300):
        self.dt = dt
        self.fps = fps
        self.controller = controller

        self.simulator = Simulator(deepcopy(world))
        self.gui = GUI(monitor_width, monitor_height)

    def run(self):
        cp_range, cv_range, pa_range, pv_range, force_range = fuzzification.read_fuzzy_map_data()
        rules = inference.read_fuzzy_rules_data()

        # for i in cp_range.keys():
        #     print i," : ",cp_range[i]
        # print "------------------------------------------------------------"
        # for i in cv_range.keys():
        #     print i," : ",cv_range[i]
        # print "------------------------------------------------------------"
        # for i in pa_range.keys():
        #     print i," : ",pa_range[i]
        # print "------------------------------------------------------------"
        # for i in pv_range.keys():
        #     print i," : ",pv_range[i]
        # print "------------------------------------------------------------"
        # for i in force_range.keys():
        #     print i," : ",force_range[i]
        # print "------------------------------------------------------------"

        while True:
            now = time()

            # force = self.controller.decide(self.simulator.world)
            force = self.controller.decide(self.simulator.world, cp_range, cv_range, pa_range, pv_range, force_range,rules)
            print 'force:', force

            self.simulator.apply_force(force)
            self.simulator.tick(self.dt)

            self.gui.draw(self.simulator.world)
            sleep(max((1. / self.fps) - (time() - now), 0))
