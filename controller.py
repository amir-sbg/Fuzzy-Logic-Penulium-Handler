# -*- coding: utf-8 -*-
from random import randint
# python imports
from math import degrees

# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader

# manual fuzzification import
import fuzzification

# manual inference import
import inference


class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)


    def _make_input(self, world):
        return dict(
            cp = world.x,
            cv = world.v,
            pa = degrees(world.theta),
            pv = degrees(world.omega)
        )


    def _make_output(self):
        return dict(
            force = 0.
        )

    # def decide(self, world):
    #     output = self._make_output()
    #     self.system.calculate(self._make_input(world), output)
    #     return output['force']



    def decide(self, world, cp_range, cv_range, pa_range, pv_range, force_range,rules):
        print "------------------------------------------------------------------------------------------------------------------------"
        print "World: ",self._make_input(world)
        fuzzy_cp, fuzzy_cv, fuzzy_pa, fuzzy_pv=fuzzification.fuzzification_all(cp_range,cv_range,pa_range,pv_range,self._make_input(world))
        rules_results = inference.result_of_rules(rules,fuzzy_cp, fuzzy_cv, fuzzy_pa, fuzzy_pv)
        print (rules_results)
        print force_range




        # print "-----------------fuzzy_cp-------------------------------------------"
        # for i in fuzzy_cp.keys():
        #     print i," : ",fuzzy_cp[i]
        # print "------------------fuzzy_cv------------------------------------------"
        # for i in fuzzy_cv.keys():
        #     print i," : ",fuzzy_cv[i]
        # print "-------------------fuzzy_pa-----------------------------------------"
        # for i in fuzzy_pa.keys():
        #     print i," : ",fuzzy_pa[i]
        # print "-------------------fuzzy_pv-----------------------------------------"
        # for i in fuzzy_pv.keys():
        #     print i," : ",fuzzy_pv[i]


        output = self._make_output()
        self.system.calculate(self._make_input(world), output)
        return out
        # return output['force']


