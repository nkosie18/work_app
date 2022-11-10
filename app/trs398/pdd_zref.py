import numpy as np

class Pdd_data:
    def __init__(self, energy:str, depth:float, machine):
        self.energy = energy
        self.depth = depth
        self.machine = machine

    
    def pdd(self)->float:
        if self.machine == 'L1':
            pdd = {'4E' : round(-1.171878E-07*self.depth**6 + 8.124070E-06*self.depth**5 - 1.824109E-04*self.depth**4 + 0.001349*self.depth**3 - 0.003508*self.depth**2 + 0.035909*self.depth + 0.756930,3),
            '6E' : round(-1.822707E-08*self.depth**6 + 1.914095E-06*self.depth**5 - 6.874424E-05*self.depth**4 + 0.000966*self.depth**3 - 0.005879*self.depth**2 + 0.033386*self.depth + 0.782149,3),
            '9E' : round(-1.195334E-09*self.depth**6 + 2.189510E-07*self.depth**5 - 1.352203E-05*self.depth**4 + 0.000337*self.depth**3 - 0.003770*self.depth**2 + 0.026912*self.depth + 0.820354,3),
            '12E' : round(-5.0395964E-10*self.depth**6 + 1.09419978E-07*self.depth**5 - 8.501506064E-06*self.depth**4 + 0.00028532307*self.depth**3 - 0.0043819899*self.depth**2 + 0.03297705979*self.depth + 0.839776947,3),
            '15E' : round(-9.126155E-11*self.depth**6 + 2.646137E-08*self.depth**5 - 2.713825E-06*self.depth**4 + 0.000120*self.depth**3 - 0.002499*self.depth**2 + 0.025012*self.depth + 0.880000,3)
            }
            return pdd[self.energy]
        elif self.machine == 'L2':
            pdd = {'4E' : round(-8.00184E-08*self.depth**6 + 6.03265E-06*self.depth**5 - 0.000147847*self.depth**4 + 0.001191759*self.depth**3 - 0.002662508*self.depth**2 + 0.027845192*self.depth + 0.752671742,3),
            '6E' : round(-1.370161E-08*self.depth**6 + 1.546249E-06*self.depth**5 - 6.014537E-05*self.depth**4 + 0.000929*self.depth**3 - 0.006106*self.depth**2 + 0.032638*self.depth + 0.776819,3),
            '9E' : round(-2.014964E-09*self.depth**6 + 3.342287E-07*self.depth**5 - 1.956053E-05*self.depth**4 + 0.000480*self.depth**3 - 0.005272*self.depth**2 + 0.032672*self.depth + 0.807748,3),
            '12E' : round(-6.271387E-11*self.depth**6 + 3.061760E-08*self.depth**5 - 3.258097E-06*self.depth**4 + 0.000125*self.depth**3 - 0.002119*self.depth**2 + 0.020729*self.depth + 0.850788,3),
            '15E' : round(-2.742543E-11*self.depth**6 + 1.188901E-08*self.depth**5 - 1.480391E-06*self.depth**4 + 0.000072*self.depth**3 - 0.001645*self.depth**2 + 0.019073*self.depth + 0.887225,3)
            }
            return pdd[self.energy]

        elif self.machine == 'L3':
            pdd = {'4E' : round(-1.111642E-07*self.depth**6 + 6.931212E-06*self.depth**5 - 1.254129E-04*self.depth**4 + 0.000307*self.depth**3 + 0.004061*self.depth**2 + 0.012289*self.depth + 0.801066,3),
            '12E' : round(-2.478017E-10*self.depth**6 + 6.229042E-08*self.depth**5 - 5.180925E-06*self.depth**4 + 0.000174*self.depth**3 - 0.002613*self.depth**2 + 0.020867*self.depth + 0.874190,3),
            '15E' : round(-5.167734E-11*self.depth**6 + 1.727094E-08*self.depth**5 - 1.887382E-06*self.depth**4 + 0.000084*self.depth**3 - 0.001738*self.depth**2 + 0.017628*self.depth + 0.909073,3),
            '18E' : round(-2.93682E-11*self.depth**6 + 1.03398E-08*self.depth**5 - 1.27997E-06*self.depth**4 + 6.80016E-05*self.depth**3 - 1.67006E-03*self.depth**2 + 1.80238E-02*self.depth + 9.27578E-01,3),
            '20E' : round(1.1970E-11*self.depth**6 - 2.1705E-09*self.depth**5 + 8.2958E-08*self.depth**4 + 2.7749E-06*self.depth**3 - 2.8388E-04*self.depth**2 + 6.5538E-03*self.depth + 9.5320E-01,3)
            }
            return pdd[self.energy]


           

    