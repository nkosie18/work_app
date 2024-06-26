import numpy as np
import math

class MuCalc:
    def __init__(self, depth:float, field_size:float):
        self.depth = depth
        self.field_size = field_size

    def Ph_6MV(self):
        field_sizes = [3, 4, 5,	6, 7, 8, 10, 12, 15, 20, 25, 30, 35, 40]
        mu_per_gy_table = {1.5 : [107.00, 104.40, 102.30, 100.80, 99.50, 98.60, 97.10, 95.70, 94.10, 91.70, 90.30, 89.20, 88.60, 88.30],
            2.0 : [106.30, 103.80, 101.80, 100.40, 99.10, 98.40, 96.90, 95.50, 93.90, 91.70, 90.30, 89.30, 88.70, 88.40],
            2.5 : [107.40, 104.80, 102.70, 101.30, 99.90, 99.00, 97.50, 96.20, 94.80, 92.40, 91.00, 89.90, 89.20, 89.00],
            3.0 : [109.10, 106.40, 104.20, 102.70, 101.30, 100.40, 98.70, 97.30, 95.60, 93.30, 91.90, 90.80, 90.10, 89.70],
            3.5 : [111.10, 108.20, 105.90, 104.30, 102.70, 101.80, 99.90, 98.40, 96.70, 94.20, 92.60, 91.50, 90.80, 90.50],
            4.0 : [112.80, 109.90, 107.50, 105.80, 104.20, 103.20, 101.20, 99.60, 97.70, 95.20, 93.60, 92.30, 91.60, 91.20],
            4.5 : [115.00, 111.90, 109.40, 107.60, 105.90, 104.80, 102.60, 100.90, 98.90, 96.20, 94.50, 93.30, 92.60, 92.20],
            5.0 : [115.00, 111.90, 109.40, 107.60, 105.90, 104.80, 102.60, 100.90, 98.90, 96.20, 94.50, 93.30, 92.60, 92.20],
            5.5 : [119.50, 116.20, 113.40, 111.40, 109.40, 108.10, 105.60, 103.60, 101.40, 98.50, 96.60, 95.30, 94.50, 94.00],
            6.0 : [122.10, 118.50, 115.60, 113.40, 111.30, 109.80, 107.00, 105.00, 102.70, 99.70, 97.70, 96.30, 95.50, 94.90],
            6.5 : [124.50, 120.80, 117.70, 115.40, 113.20, 111.60, 108.60, 106.60, 104.20, 101.00, 98.90, 97.30, 96.40, 95.80],
            7.0 : [126.90, 123.00, 119.80, 117.40, 115.10, 113.40, 110.30, 108.20, 105.60, 102.20, 100.00, 98.50, 97.50, 96.80],
            7.5 : [129.50, 125.50, 122.10, 119.60, 117.20, 115.40, 112.10, 109.80, 107.00, 103.50, 101.20, 99.60, 98.60, 97.90],
            8.0 : [132.40, 128.20, 124.60, 122.00, 119.40, 117.60, 114.00, 111.60, 108.60, 104.90, 102.40, 100.70, 99.60, 98.90],
            8.5 : [135.10, 130.70, 127.10, 124.20, 121.60, 119.60, 115.80, 113.20, 110.10, 106.30, 103.70, 101.90, 100.80, 100.00],
            9.0 : [137.80, 133.20, 129.40, 126.50, 123.70, 121.70, 117.70, 115.10, 111.80, 107.80, 105.10, 103.30, 102.00, 101.20],
            9.5 : [140.80, 136.00, 132.00, 128.90, 126.00, 123.80, 119.60, 116.80, 113.40, 109.30, 106.50, 104.60, 103.20, 102.20],
            10.0 : [143.80, 138.90, 134.80, 131.60, 128.50, 126.20, 121.80, 118.80, 115.10, 110.90, 108.00, 105.90, 104.50, 103.40],
            10.5 : [146.90, 141.80, 137.50, 134.10, 130.90, 128.50, 123.90, 120.80, 116.90, 112.50, 109.30, 107.20, 105.80, 104.80],
            11.0 : [150.10, 144.70, 140.20, 136.70, 133.30, 130.70, 125.90, 122.70, 118.70, 114.10, 110.70, 108.60, 107.10, 106.00],
            11.5 : [153.50, 147.90, 143.20, 139.50, 136.00, 133.20, 128.10, 124.80, 120.60, 115.80, 112.30, 110.10, 108.50, 107.40],
            12.0 : [156.70, 150.90, 146.00, 142.20, 138.50, 135.70, 130.40, 126.80, 122.40, 117.40, 113.80, 111.50, 109.90, 108.70],
            12.5 : [160.00, 154.00, 148.90, 144.90, 141.10, 138.20, 132.60, 129.00, 124.30, 119.10, 115.30, 113.00, 111.40, 110.10],
            13.0 : [163.40, 157.20, 152.00, 147.90, 143.90, 140.90, 135.10, 131.30, 126.40, 121.00, 117.00, 114.60, 113.00, 111.70],
            13.5 : [167.10, 160.70, 155.30, 150.90, 146.80, 143.60, 137.60, 133.60, 128.40, 122.90, 118.70, 116.20, 114.40, 113.00],
            14.0 : [170.40, 163.90, 158.30, 153.80, 149.60, 146.30, 140.10, 135.90, 130.40, 124.70, 120.50, 117.80, 115.80, 114.20],
            14.5 : [174.00, 167.20, 161.50, 156.90, 152.60, 149.20, 142.80, 138.30, 132.60, 126.60, 122.20, 119.40, 117.30, 115.60],
            15.0 : [178.20, 171.10, 165.00, 160.20, 155.60, 152.00, 145.30, 140.70, 134.90, 128.60, 123.90, 121.10, 119.00, 117.40],
            15.5 : [182.60, 175.10, 168.70, 163.60, 158.80, 154.90, 147.70, 143.10, 137.10, 130.60, 125.80, 122.80, 120.60, 118.90],
            16.0 : [186.00, 178.40, 171.90, 166.70, 161.80, 158.00, 150.70, 145.70, 139.40, 132.70, 127.60, 124.60, 122.30, 120.50],
            16.5 : [190.20, 182.30, 175.50, 170.10, 164.90, 160.80, 153.20, 148.20, 141.90, 134.80, 129.50, 126.30, 123.90, 122.00],
            17.0 : [194.10, 185.90, 179.00, 173.40, 168.10, 163.90, 156.00, 150.90, 144.30, 137.10, 131.60, 128.30, 125.70, 123.60],
            17.5 : [198.40, 190.00, 182.80, 177.00, 171.50, 167.20, 159.00, 153.60, 146.80, 139.30, 133.60, 130.20, 127.50, 125.50],
            18.0 : [202.70, 194.10, 186.70, 180.70, 175.10, 170.60, 162.20, 156.50, 149.20, 141.40, 135.50, 132.00, 129.40, 127.20],
            18.5 : [207.30, 198.30, 190.60, 184.40, 178.50, 173.80, 165.10, 159.20, 151.70, 143.70, 137.70, 134.10, 131.40, 129.20],
            19.0 : [211.60, 202.30, 194.30, 187.90, 181.90, 177.10, 168.00, 162.10, 154.40, 146.10, 139.80, 136.00, 133.10, 130.80],
            19.5 : [216.20, 206.60, 198.50, 191.90, 185.70, 180.60, 171.30, 165.10, 157.20, 148.60, 141.90, 138.10, 135.10, 132.60],
            20.0 : [221.40, 211.40, 202.90, 196.00, 189.50, 184.20, 174.50, 168.10, 159.80, 151.00, 144.30, 140.20, 137.00, 134.40],
            20.5 : [225.70, 215.50, 206.80, 199.80, 193.10, 187.80, 177.80, 171.10, 162.50, 153.40, 146.40, 142.20, 139.00, 136.40],
        }
        if self.depth == round(self.depth * 2)/2 : 
            return round(np.interp(self.field_size, field_sizes, mu_per_gy_table[round(self.depth * 2)/2]),2)

        else:
            if round(self.depth) > self.depth:
                a = ((round(self.depth) - 0.5), np.interp(self.field_size, field_sizes, mu_per_gy_table[round(self.depth) - 0.5]))
                b = (round(self.depth), np.interp(self.field_size, field_sizes, mu_per_gy_table[round(self.depth)]))
                c = (self.depth, a[1]  + (((self.depth - a[0])/(b[0] - a[0]))*(b[1] - a[1])))
                return c[1]
            else:
                a = ((round(self.depth)), np.interp(self.field_size, field_sizes, mu_per_gy_table[round(self.depth)])) 
                b = ((round(self.depth) + 0.5), np.interp(self.field_size, field_sizes, mu_per_gy_table[round(self.depth) + 0.5]))
                c = (self.depth, a[1]  + (((self.depth - a[0])/(b[0] - a[0]))*(b[1] - a[1])))
                return c[1]

    

