#######################################################
#
# Author: Cesar Ordonez
# Date: 07/02/2020
# File to configure benthic chambers cores
# meta = {Lake: {BC: (Start Time, End Time, Start Date, File, CH4start, CH4end,
#         CO2start, CO2end, Hw, Ha, P, Temp)}}
#######################################################

metadata = {'Lioson': {'BC1': ('18:10', '19:22', '2019-07-17', 'f0001', 0.03, 0.02,
                               21.60, 15.51, 44.5, 5, 820, 18),
                       'BC2': ('14:50', '16:05', '2019-07-18', 'f0001', 0.15, 0.04,
                               13.65, 15.59, 45, 4, 820, 17),
                       'BC3': ('19:35', '20:08', '2019-07-18', 'f0004', 0.06, 0.05,
                               14.61, 13.25, 41, 7, 820, 14)},
            'Bretaye':{'BC3.1': ('17:08', '17:30', '2019-07-21', 'f0002', 1.54, 3.72,
                                 27.98, 44.70, 41, 6, 820, 20),
                       'BC3.2': ('21:55', '23:20', '2019-07-21', 'f0004', 0.09, 0.38,
                                 20.45, 25.47, 41, 6, 820, 20)},
            'Noir':{'BC-LitA': ('18:36', '18:42', '2019-07-24', 'f0002', 1.3, 1.29,
                                18.65, 19.11, 46, 4.5, 825, 23),
                    'BC-LitB': ('19:05', '19:49', '2019-07-24', 'f0002', 0.18, 0.01,
                                18.39, 11.64, 46, 4.5, 825, 22),
                    'BC3_A': ('22:12', '22:40', '2019-07-24', 'f0003', 0.07, 0.06,
                              17.88, 19.59, 50.5, 4.5, 825, 20),
                    'BC2': ('23:56', '00:50', '2019-07-24', 'f0003', 0.08, 0.04,
                            18.70, 15.67, 46, 4, 825, 20),
                    'BC3_B': ('16:25', '17:25', '2019-07-25', 'f0002', 0.03, 0.02,
                              15.38, 14.22, 51.5, 4, 825, 25)},
            'Chavonnes':{'BC1': ('16:17', '17:30', '2019-07-23', 'f0002', 0.04, -99,
                                 16.21, -99, 66, 4, 837, 21),
                         'BC1.1': ('17:50', '18:44', '2019-07-23', 'f0002', 0.02, 0.02,
                                   12.80, 13.88, 64, 6, 837, 21),
                         'BC2': ('10:05', '11:00', '2019-07-25', 'f0000', 0.02, 0.01,
                                 13.29, 11.02, 50, 6, 837, 23),
                         'BC3': ('13:25', '14:30', '2019-07-25', 'f0001', 0.01, -99,
                                 10.58, -99, 55, 6, 837, 25)},
            'Soppen':{'BC1': ('16:58', '18:08', '2019-08-19', 'f0003', 0.5, 0.38,
                                 9.34, 9.12, 45, 5, 957, 18),
                      'BC2': ('19:46', '21:10', '2019-08-21', 'f0002', 1.97, 0.59,
                                 17.96, 31.3, 33, 5.5, 957, 15),
                      'BC3': ('20:49', '22:30', '2019-08-22', 'f0003', 0.68, 0.35,
                                 19.12, 23.76, 23, 5, 957, 15)},
            'Baldegg':{'BC1': ('11:03', '12:38', '2019-08-17', 'f0000', 0.13, 0.03,
                               22.86, 16.76, 45, 5.5, 964, 24),
                       'BC2': ('15:04', '16:35', '2019-08-17', 'f0001', 0.12, 0.04,
                               19.12, 23.76, 45, 5.5, 964, 24)},
            'AP_daynight':{'Day':('18:34','19:23','2020-03-12','f0002', 0.043, 0.019,
                                  25.18, 22.7, 36, 4, 962, 21),
                           'Night':('14:38', '15:21', '2020-03-12','f0001', 0.005, 0.004,
                                    21.40, 21.42, 36, 4, 962, 21)},
            'AP_comparison':{'BC2C':('10:25','11:20', '2019-11-12','f0000', 0.0047, 0.0046,
                                     20.11, 23.07, 35, 5, 962, 21),
                             'BC1R':('12:40', '13:40', '2019-11-12', 'f0000', 0.0033, 0.0040,
                                     19.92,24.20, 35, 5,962,21),
                             'BC2B':('15:30','16:30', '2019-11-12', 'f0000', 0.0035,0.0076,
                                     19.22,21.07, 35,5,962,21)}
            }

## Aurora Experiment
#meta = ('10:25','12:00', '2019-11-12','f0000', 0.0047, 0.0046, 23.07, 63.41,
#        35, 5, 962, 21, 'EXP', 'BC2C')
#meta = ('12:40','14:40', '2019-11-12','f0000', 0.0033, 0.0040, 23.07, 63.41,
#        35, 5, 962, 21, 'EXP', 'BC2C')

#meta = ('15:15','16:30', '2019-11-12','f0000', 0.0033, 0.0076, 23.07, 63.41,
#        35, 5, 962, 21, 'EXP', 'BC2C')
## Lake Bretaye
#meta = ('15:13','16:00', '2019-07-21', 'f0001', 3.00, -99, 30.41, -99,
#        41, 6, 820, 20, 'Bretaye', 'BC2') # No configuration core
