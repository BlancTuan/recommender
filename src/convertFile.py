import xlrd
import csv
from caserec.utils.process_data import ReadFile
from caserec.utils.process_data import WriteFile
from joblib.numpy_pickle_utils import xrange


out_train_file = "../data/jester-data-1/data_learn.data"
out_test_file = "../data/jester-data-1/data_test.data"


class convertFile():
    def __init__(self, out_reducts_file = None, data = None):
        self.out_file = out_reducts_file
        self.mode = 'w'
        self.sep = "\t"
        self.data = data
        self.check = 0
    def xls_to_csv(self):
        num_user = 0

        x =  xlrd.open_workbook('../data/jester-data-1/jester-data-1.xls')
        x1 = x.sheet_by_name('jester-data-1-new')

        list_item_seem_by_user_test = []
        list_item_seem_by_user_train = []
        for rownum in xrange(x1.nrows): #To determine the total rows.

            self.check = 0
            for idx, val in enumerate(x1.row_values(rownum)):
                if idx == 0 and val >= 50:
                    break
                #     Lấy so user tu idx = 1 va co danh gia (!=99)
                if idx != 0 and val != 99 and num_user <= 50:
                    list_item_seem_by_user_train.append([rownum , idx, val])
                    self.check = 1
                elif idx != 0 and val != 99:
                    list_item_seem_by_user_test.append([rownum, idx, val])

            if(self.check == 1):
                num_user +=1



        WriteFile(out_test_file, list_item_seem_by_user_test).write()
        WriteFile(out_train_file,list_item_seem_by_user_train).write()


    def WriteFile(self):
        with open(self.out_file, self.mode) as infile:
            for user in self.data:
                for pair in self.data[user]['cl']:
                    infile.write('%d%s' % (user, " CL:"))
                    for item in pair:
                        infile.write('%s%d' % (self.sep, item))
                    infile.write("\n")
                for pair in self.data[user]['dl']:
                    infile.write('%d%s' % (user, " DL:"))
                    for item in pair:
                        infile.write('%s%d' % (self.sep, item))
                    infile.write("\n")

# convertFile = convertFile()
# convertFile.xls_to_csv()