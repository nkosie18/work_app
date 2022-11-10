import numpy as np

class Kq_photons:
    def __init__(self, tpr2010 :float, ion_chamber:str):
        self.tpr2010 = tpr2010 
        self.ion_chamber = ion_chamber

    def kq_value(self)->float:
        trs_tpr2010 = [0.50, 0.53, 0.56, 0.59, 0.62, 0.65, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82, 0.84]
        table_vii = {"PTW 23331" : [1.004, 1.003, 1.000, 0.999, 0.997, 0.993, 0.990, 0.988, 0.985, 0.982, 0.978, 0.971, 0.964, 0.956, 0.945],
        "PTW 23332" : [1.004, 1.003, 1.001, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.976, 0.968, 0.961, 0.954, 0.943],
        "PTW 23333" : [1.004, 1.003, 1.001, 0.999, 0.997, 0.994, 0.990, 0.988, 0.985, 0.981, 0.976, 0.969, 0.962, 0.955, 0.943],
        "PTW 30001" : [1.004, 1.003, 1.001, 0.999, 0.997, 0.994, 0.990, 0.988, 0.985, 0.981, 0.976, 0.969, 0.962, 0.955, 0.943],
        "PTW 30010" : [1.004, 1.003, 1.001, 0.999, 0.997, 0.994, 0.990, 0.988, 0.985, 0.981, 0.976, 0.969, 0.962, 0.955, 0.943],
        "PTW 30002" : [1.006, 1.004, 1.001, 0.999, 0.997, 0.994, 0.992, 0.990, 0.987, 0.984, 0.980, 0.973, 0.967, 0.959, 0.948],
        "PTW 30011" : [1.006, 1.004, 1.001, 0.999, 0.997, 0.994, 0.992, 0.990, 0.987, 0.984, 0.980, 0.973, 0.967, 0.959, 0.948],
        "PTW 30004" : [1.006, 1.005, 1.002, 1.000, 0.999, 0.996, 0.994, 0.992, 0.989, 0.986, 0.982, 0.976, 0.969, 0.962, 0.950],
        "PTW 30012" : [1.006, 1.005, 1.002, 1.000, 0.999, 0.996, 0.994, 0.992, 0.989, 0.986, 0.982, 0.976, 0.969, 0.962, 0.950],
        "PTW 30006" : [1.002, 1.002, 1.000, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.975, 0.968, 0.960, 0.952, 0.940],
        "PTW 30013" : [1.002, 1.002, 1.000, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.975, 0.968, 0.960, 0.952, 0.940],
        "PTW 31002" : [1.003, 1.002, 1.000, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.975, 0.968, 0.960, 0.952, 0.940],
        "PTW 31010" : [1.003, 1.002, 1.000, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.975, 0.968, 0.960, 0.952, 0.940],
        "PTW 31003" : [1.003, 1.002, 1.000, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.975, 0.968, 0.960, 0.952, 0.940],
        "PTW 31013" : [1.003, 1.002, 1.000, 0.999, 0.997, 0.994, 0.990, 0.988, 0.984, 0.980, 0.975, 0.968, 0.960, 0.952, 0.940],
        "PTW 31014" : [1.004, 1.003, 1.001, 0.999, 0.998, 0.995, 0.992, 0.989, 0.985, 0.980, 0.975, 0.967, 0.959, 0.952, 0.941],
        "PTW 31015" : [1.004, 1.003, 1.001, 0.999, 0.998, 0.995, 0.992, 0.989, 0.985, 0.980, 0.975, 0.967, 0.959, 0.952, 0.941],
        "PTW 31016" : [1.004, 1.003, 1.001, 0.999, 0.998, 0.995, 0.992, 0.989, 0.985, 0.980, 0.975, 0.967, 0.959, 0.952, 0.941],
        "Scdx-Wellhfer CC01" : [1.002, 1.002, 1.002, 1.001, 1.000, 0.999, 0.996, 0.994, 0.991, 0.986, 0.981, 0.972, 0.964, 0.956, 0.944],
        "Scdx-Wellhfer CC04" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.992, 0.989, 0.984, 0.979, 0.970, 0.962, 0.953, 0.941],
        "Scdx-Wellhfer IC04" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.992, 0.989, 0.984, 0.979, 0.970, 0.962, 0.953, 0.941],
        "Scdx-Wellhfer CC08" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer IC05" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer IC06" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer CC13" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "CC13" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer IC10" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer IC15" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer CC25" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer IC25" : [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.989, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer FC23-CIC28" :  [1.001, 1.001, 1.001, 1.000, 0.999, 0.997, 0.995, 0.993, 0.990, 0.985, 0.980, 0.972, 0.964, 0.955, 0.943],
        "Scdx-Wellhfer FC65-P" : [1.003, 1.002, 1.001, 0.999, 0.998, 0.995, 0.993, 0.990, 0.986, 0.981, 0.976, 0.968, 0.960, 0.952, 0.940],
        "Scdx-Wellhfer IC69" : [1.003, 1.002, 1.001, 0.999, 0.998, 0.995, 0.993, 0.990, 0.986, 0.981, 0.976, 0.968, 0.960, 0.952, 0.940],
        "Scdx-Wellhfer FC65-G" : [1.005, 1.004, 1.002, 1.000, 0.998, 0.997, 0.995, 0.992, 0.989, 0.985, 0.981, 0.973, 0.966, 0.958, 0.947], 
        "Scdx-Wellhfer IC70" : [1.005, 1.004, 1.002, 1.000, 0.998, 0.997, 0.995, 0.992, 0.989, 0.985, 0.981, 0.973, 0.966, 0.958, 0.947],
        "Sun Nuclear 100700-0 Farmer" :  [1.005, 1.004, 1.001, 0.999, 0.998, 0.995, 0.992, 0.989, 0.986, 0.981, 0.976, 0.969, 0.962, 0.954, 0.943],
        "Sun Nuclear 100700-1 Farmer" : [1.007, 1.006, 1.003, 1.001, 0.999, 0.997, 0.995, 0.993, 0.990, 0.986, 0.983, 0.976, 0.969, 0.961, 0.951]
        }
        return round(np.interp(self.tpr2010, trs_tpr2010, table_vii[self.ion_chamber]),3)



class Kq_electrons:
    def __init__(self, r50 :float, ion_chamber :str):
        self.r50 = r50
        self.ion_chamber = ion_chamber

    def kq_value(self) -> float:
        trs_R50 = [1.0, 1.4, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 10.0, 13.0, 16.0, 20.0]
        table_7III = {'AttixRMI 449':[0.953, 0.943, 0.932, 0.925, 0.919, 0.913, 0.908, 0.904, 0.900, 0.896, 0.893, 0.886, 0.881, 0.871, 0.859, 0.849, 0.837],
        'Exradin P11':[0.958, 0.948, 0.937, 0.930, 0.923, 0.918, 0.913, 0.908, 0.904, 0.901, 0.897, 0.891, 0.885, 0.875, 0.863, 0.853, 0.841],
        'Holt (Memorial)':[0.971, 0.961, 0.950, 0.942, 0.936, 0.931, 0.926, 0.921, 0.917, 0.913, 0.910, 0.903, 0.897, 0.887, 0.875, 0.865, 0.853],
        'Roos':[0.965, 0.955, 0.944, 0.937, 0.931, 0.925, 0.920, 0.916, 0.912, 0.908, 0.904, 0.898, 0.892, 0.882, 0.870, 0.860, 0.848],
        'NACP / Calcam':[0.952, 0.942, 0.931, 0.924, 0.918, 0.912, 0.908, 0.903, 0.899, 0.895, 0.892, 0.886, 0.880, 0.870, 0.858, 0.848, 0.836],
        'PTW 34045':[0.966, 0.956 , 0.945 , 0.938 , 0.932 , 0.926 , 0.921 , 0.917 , 0.912 , 0.909 , 0.905 , 0.899 , 0.893 , 0.883 , 0.871 , 0.861 , 0.849 ],
        'Markus':[10000, 10000, 0.925, 0.920, 0.916, 0.913, 0.910, 0.907, 0.904, 0.901, 0.899, 0.894, 0.889, 0.881, 0.870, 0.860, 0.849],
        'CapintecPS-033':[10000, 10000, 0.921, 0.920, 0.919, 0.918, 0.917, 0.916, 0.915, 0.913, 0.912, 0.908, 0.905, 0.898, 0.887, 0.877, 0.866],
        'Capintec PR06C':[10000, 10000, 10000, 10000, 10000, 10000, 0.916, 0.914, 0.912, 0.911, 0.909, 0.906, 0.904, 0.899, 0.891, 0.884, 0.874],
        'Exradin A2':[10000, 10000, 10000, 10000, 10000, 10000, 0.914, 0.913, 0.913, 0.913, 0.912, 0.911, 0.910, 0.908, 0.903, 0.897, 0.888],
        'Exradin T2':[10000, 10000, 10000, 10000, 10000, 10000, 0.882, 0.881, 0.881, 0.881, 0.880, 0.879, 0.878, 0.876, 0.871, 0.865, 0.857],
        'Exradin A12':[10000, 10000, 10000, 10000, 10000, 10000, 0.921, 0.919, 0.918, 0.916, 0.914, 0.911, 0.909, 0.903, 0.896, 0.888, 0.878],
        'NE 2571':[10000, 10000, 10000, 10000, 10000, 10000, 0.918, 0.916, 0.915, 0.913, 0.911, 0.909, 0.906, 0.901, 0.893, 0.886, 0.876],
        'NE 2581':[10000, 10000, 10000, 10000, 10000, 10000, 0.899, 0.898, 0.896, 0.894, 0.893, 0.890, 0.888, 0.882, 0.875, 0.868, 0.859],
        'PTW 30001':[10000, 10000, 10000, 10000, 10000, 10000, 0.911, 0.909, 0.907, 0.905, 0.904, 0.901, 0.898, 0.893, 0.885, 0.877, 0.868],
        'PTW 30010':[10000, 10000, 10000, 10000, 10000, 10000, 0.911, 0.909, 0.907, 0.905, 0.904, 0.901, 0.898, 0.893, 0.885, 0.877, 0.868],
        'PTW 30002':[10000, 10000, 10000, 10000, 10000, 10000, 0.916, 0.914, 0.912, 0.910, 0.909, 0.906, 0.903, 0.897, 0.890, 0.882, 0.873],
        'PTW 30011':[10000, 10000, 10000, 10000, 10000, 10000, 0.916, 0.914, 0.912, 0.910, 0.909, 0.906, 0.903, 0.897, 0.890, 0.882, 0.873],
        'PTW 30004':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.916, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.887, 0.877],
        'PTW 30012':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.916, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.887, 0.877],
        'PTW 30006':[10000, 10000, 10000, 10000, 10000, 10000, 0.911, 0.909, 0.907, 0.906, 0.904, 0.901, 0.898, 0.893, 0.885, 0.878, 0.868],
        'PTW 30013':[10000, 10000, 10000, 10000, 10000, 10000, 0.911, 0.909, 0.907, 0.906, 0.904, 0.901, 0.898, 0.893, 0.885, 0.878, 0.868],
        'PTW 31002' : [10000, 10000, 10000, 10000, 10000, 10000,  0.912,  0.910,  0.908,  0.906,  0.905,  0.901,  0.898,  0.893,  0.885,  0.877,  0.867],
        'PTW 31003' : [10000, 10000, 10000, 10000, 10000, 10000,  0.912,  0.910,  0.908,  0.906,  0.905,  0.901,  0.898,  0.893,  0.885,  0.877,  0.867],
        'PTW 31006':[10000, 10000, 10000, 10000, 10000, 10000, 0.928, 0.924, 0.921, 0.918, 0.915, 0.910, 0.905, 0.896, 0.885, 0.876, 0.865],
        'PTW 31014':[10000, 10000, 10000, 10000, 10000, 10000, 0.929, 0.925, 0.922, 0.919, 0.916, 0.910, 0.905, 0.897, 0.886, 0.876, 0.865],
        'Scdx-Wellhöfer CC01':[10000, 10000, 10000, 10000, 10000, 10000, 0.942, 0.938, 0.935, 0.932, 0.929, 0.923, 0.918, 0.909, 0.898, 0.889, 0.878],
        'Scdx-Wellhöfer CC04':[10000, 10000, 10000, 10000, 10000, 10000, 0.928, 0.925, 0.922, 0.920, 0.918, 0.913, 0.910, 0.902, 0.893, 0.884, 0.874],
        'Scdx-Wellhöfer IC04':[10000, 10000, 10000, 10000, 10000, 10000, 0.928, 0.925, 0.922, 0.920, 0.918, 0.913, 0.910, 0.902, 0.893, 0.884, 0.874],
        'Scdx-Wellhöfer IC06':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer IC05':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer CC08':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer CC13':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer IC10':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer IC15':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer IC25':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer CC25':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.917, 0.915, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        
        'Scdx-Wellhöfer IC28':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.916, 0.914, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer FC23-C':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.916, 0.914, 0.913, 0.910, 0.907, 0.902, 0.894, 0.886, 0.877],
        'Scdx-Wellhöfer FC65-P':[10000, 10000, 10000, 10000, 10000, 10000, 0.914, 0.912, 0.911, 0.909, 0.907, 0.904, 0.902, 0.896, 0.889, 0.881, 0.872],
        'Scdx-Wellhöfer IC69':[10000, 10000, 10000, 10000, 10000, 10000, 0.914, 0.912, 0.911, 0.909, 0.907, 0.904, 0.902, 0.896, 0.889, 0.881, 0.872],
        'Scdx-Wellhöfer FC65-G':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.916, 0.914, 0.913, 0.910, 0.907, 0.902, 0.894, 0.887, 0.877],
        'Scdx-Wellhöfer IC70':[10000, 10000, 10000, 10000, 10000, 10000, 0.920, 0.918, 0.916, 0.914, 0.913, 0.910, 0.907, 0.902, 0.894, 0.887, 0.877],
        'Victoreen 30-348':[10000, 10000, 10000, 10000, 10000, 10000, 0.910, 0.908, 0.906, 0.903, 0.902, 0.898, 0.895, 0.888, 0.880, 0.872, 0.862],
        'Victoreen 30-351':[10000, 10000, 10000, 10000, 10000, 10000, 0.906, 0.904, 0.902, 0.901, 0.899, 0.896, 0.893, 0.888, 0.880, 0.873, 0.864],
        'Victoreen 30-349':[10000, 10000, 10000, 10000, 10000, 10000, 0.899, 0.898, 0.897, 0.896, 0.895, 0.893, 0.891, 0.888, 0.881, 0.875, 0.866]
        }


        k_value = round(np.interp(self.r50, trs_R50 ,table_7III[self.ion_chamber]),3)

        if k_value < 2:
            return k_value
        else:
            return 'The selected chamber (%s) is not usable in the electron beam quality selected (%s). Please select a different detector' %(self.ion_chamber, self.r50)
   