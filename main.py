#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pdb
from scr.read_lgr import read_lgrdata
from scr.processing_BC import processing_BC
from scr.plots import plot_results
from scr.write import write_excel
from scr.logging_conf import logging_conf

from conf_exp import *
from conf_BC import metadata

def main():

    logging_conf()

    for i_lake in range(len(Lakes)):
        for i_core in range(len(Cores[i_lake])):
            logging.info('STEP 1: Reading LGR Data for core %s in lake %s',
                         Cores[i_lake][i_core], Lakes[i_lake])

            data = read_lgrdata(path, Lakes[i_lake],
                                metadata[Lakes[i_lake]][Cores[i_lake][i_core]])

            logging.info('STEP 2: Processing data')
            results, data_r = processing_BC(data, Cores[i_lake][i_core],
                              metadata[Lakes[i_lake]][Cores[i_lake][i_core]],
                                            kbounds)

            logging.info('STEP 3: Making Figures')
            plot_results(results, data_r, Lakes[i_lake], Cores[i_lake][i_core],
                         metadata[Lakes[i_lake]][Cores[i_lake][i_core]],
                         path, exp, saveFig)

            logging.info('STEP 4: Wrinting results in excel file')
            write_excel(path, results, Lakes[i_lake], Cores[i_lake][i_core],
                        metadata[Lakes[i_lake]][Cores[i_lake][i_core]], exp,
                        rwrite_xlsx)

if __name__ == '__main__':
    main()


