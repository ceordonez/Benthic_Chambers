#######################################################
#
#  Author: Cesar Ordonez
#  Date: 07/02/2020
#  Config File to process benthic chambers
#
#######################################################


path = '/home/cesar/Dropbox/Cesar/PhD/Data/Experiments/Benthic_Chamber'
#path = '/home/cesar/Dropbox/Cesar/PhD/Data/Fieldwork/MultiLakeSurvey/Lakes'
saveFig = True      # Save figures
rwrite_xlsx = False # Rewrite excel file (delete old one)
exp = 'Comparison_AP_1h'

#Lakes = ('Baldegg', 'Chavonnes', 'Noir', 'Lioson', 'Soppen', 'Bretaye')
Lakes = ('AP_comparison',)
Cores = (('BC2C', 'BC1R', 'BC2B'),)
#Cores = (('Day','Night'),)

"""
Cores = (('BC1','BC2'),
         ('BC1','BC1.1','BC2','BC3'),
         ('BC-LitA', 'BC-LitB', 'BC3_A', 'BC2', 'BC3_B'),
         ('BC1', 'BC2', 'BC3'),
         ('BC1', 'BC2', 'BC3'),
         ('BC3.1', 'BC3.2'))
"""
kbounds = ((8, 1000), (8, 1000)) # (CH4, CO2) (m/d)


