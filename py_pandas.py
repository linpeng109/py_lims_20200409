from multiprocessing import Process

import pandas as pd
import winsound

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_path import Path


# from py_qrcode import QRcode


class DataFileParser():
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config

    def __getNewFilename(self, filename, type='default'):
        newpath = self.config.get(type, 'outpath')
        Path.outpathIsExist(newpath)
        fileinfo = Path.splitFullPathFileName(filename)
        newfilename = (newpath + fileinfo.get('sep') + fileinfo.get('main') + '_OK' + '.csv')
        return newfilename

    def startProcess1(self, event):
        file = event.src_path
        # winsound.Beep(500, 500)
        process = object
        try:
            if (Path.filenameIsContains(file, ['AAS.txt'])):
                process = Process(target=self.aasTxtWorker(file), args=(file,))
            elif (Path.filenameIsContains(file, ['AAS', '.xlsx'])):
                process = Process(target=self.aasExcelWorker(file), args=(file,))
            elif (Path.filenameIsContains(file, ['HCS', '.xls'])):
                process = Process(target=self.hcsExcelWorker(file), args=(file,))
            elif (Path.filenameIsContains(file, ['HCS.txt'])):
                process = Process(target=self.hcsTxtWorker(file), args=(file,))
            elif (Path.filenameIsContains(file, ['AFS', '.xlsx'])):
                process = Process(target=self.afsExcelWorker(file), args=(file,))
            process.start()
            # process.join(timeout=10000)
        except(ValueError):
            self.logger.debug('=====')
            self.logger.debug(ValueError)
            pass

    def hcsTxtWorker(self, hcsTextFileName):
        dict = {'sep': ' ', 'encoding': 'UTF-16', 'dtype': 'str', 'header': None}
        hcsDf = pd.read_csv(filepath_or_buffer=hcsTextFileName, **dict)
        # 删除表头
        hcsDf.drop(index=[0, 1], inplace=True)
        hcsDf.sort_index(0, ascending=False, inplace=True)
        # 删除空列
        hcsDf.dropna(axis=1, how='all', inplace=True)
        # 替换nan
        hcsDf.fillna('', inplace=True)
        self.logger.debug(hcsDf)
        newfilename = self.__getNewFilename(filename=hcsTextFileName, type='hcs')
        self.logger.debug(newfilename)
        encoding = self.config.get('hcs', 'encoding')
        hcsDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')

        return hcsDf

    def hcsExcelWorker(self, hcsExcelFileName):
        dict = {'sheet_name': 0, 'header': None}
        hcsDf = pd.read_excel(hcsExcelFileName, **dict)
        # 删除表标题
        hcsDf.drop(index=[0, 1], inplace=True)
        # 按照0列排列升序
        hcsDf.sort_index(0, ascending=False, inplace=True)
        hcsDf.fillna('', inplace=True)
        # 删除空列
        hcsDf.dropna(axis=1, how='any', inplace=True)
        self.logger.debug(hcsDf)
        newfilename = self.__getNewFilename(filename=hcsExcelFileName, type='hcs')
        encoding = self.config.get('hcs', 'encoding')
        hcsDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')

    def afsExcelWorker(self, afsExcelFileName):
        dict = {'sheet_name': '样品测量数据', 'header': None}
        afsDf = pd.read_excel(afsExcelFileName, **dict)
        afsDf.fillna('', inplace=True)
        afsDf.drop(index=[0, 1, 2], inplace=True)
        self.logger.debug(afsDf)
        newfilename = self.__getNewFilename(filename=afsExcelFileName, type='afs')
        encoding = self.config.get('afs', 'encoding')
        afsDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')

    def aasTxtWorker(self, aasTextFilename):
        dict = {'dtype': 'str', 'header': None}
        aasDf = pd.read_csv(filepath_or_buffer=aasTextFilename, encoding='gbk', **dict)
        aasDf.fillna('', inplace=True)
        self.logger.debug(aasDf)
        newfilename = self.__getNewFilename(filename=aasTextFilename, type='aas')
        encoding = self.config.get('aas', 'encoding')
        aasDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')
        return aasDf

    def aasExcelWorker(self, aasExcelFilename):
        dict = {'sheet_name': 0, 'header': None}
        aasDf = pd.read_excel(aasExcelFilename, **dict)
        # 删除表头
        aasDf.drop(axis=0, index=[0], inplace=True)
        aasDf.fillna('', inplace=True)
        self.logger.debug(aasDf)
        newfilename = self.__getNewFilename(filename=aasExcelFilename, type='aas')
        encoding = self.config.get('aas', 'encoding')
        aasDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')
        return aasDf


if __name__ == '__main__':
    config = ConfigFactory(config='py_lims.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    dataFileParser = DataFileParser(config=config, logger=logger)
    result = dataFileParser.hcsTxtWorker('e:/uipathdir/20191127HCS.txt')
    print('rows=%s' % result[0].shape[0])
    print('=========')
    print('df=%s' % result)
    # print('width=%s' % result[1][1])
    # print('heigh=%s' % result[2][1])
