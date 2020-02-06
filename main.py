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
def main():

    logging_conf()

    logging.info('STEP 1: Reading LGR Data')
    data = read_lgrdata(path, meta)

    logging.info('STEP 2: Processing data')
    results, data_r = processing_BC(data, meta)

    logging.info('STEP 3: Making Figures')
    plot_results(results, data_r, meta, path, False)

    logging.info('STEP4: Wrinting results in excel file')
    write_excel(path, results, meta)

if __name__ == '__main__':
    main()


