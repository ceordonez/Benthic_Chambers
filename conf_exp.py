#######################################################
#
#  Author: Cesar Ordonez
#  Date: 07/02/2020
#  Config File to process benthic chambers
#
#######################################################


path = '/home/cesar/Dropbox/Cesar/PhD/Data/Fieldwork/MultiLakeSurvey/Lakes'
saveFig = True      # Save figures
rwrite_xlsx = False # Rewrite excel file (delete old one)
exp = 'Not_kboundary'

Lakes = ('Baldegg', 'Chavonnes', 'Noir', 'Lioson', 'Soppen', 'Bretaye')

Cores = (('BC1','BC2'),
         ('BC1','BC1.1','BC2','BC3'),
         ('BC-LitA', 'BC-LitB', 'BC3_A', 'BC2', 'BC3_B'),
         ('BC1', 'BC2', 'BC3'),
         ('BC1', 'BC2', 'BC3'),
         ('BC3.1', 'BC3.2'))

kbounds = ((0, 1000), (0, 1000)) # (CH4, CO2) (m/d)


