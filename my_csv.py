from doctest import REPORT_UDIFF
import os
import csv
import chardet

class mycsv():
    def __init__(self, file_path=None, columns=None, create_file=False, encoding=None):
        self.columns = columns
        if file_path == None:
            file_path = os.getcwd()
        self.file_path = file_path
        self.encoding = encoding
        self.list = []
        if create_file == True:
            self.setup_file(file_name=file_path, encoding=encoding)
        elif create_file == False:
            pass

    def setup_file(self, file_path, encoding=None):
        self.file_path = file_path
        self.encoding = encoding
        self.list = []
        if os.path.exists(file_path):
            if self.columns != None:
                with open(file_path, mode='r',encoding=self.encoding) as f:
                    reader = csv.reader((line.replace('\0','') for line in f))
                    l = [row for row in reader]
                    if l == []:
                        self.export()
                    elif len(l) > 1: 
                        self.list = l[1:]
            else:# self.field_names == None
                with open(file_path, mode='r',encoding=self.encoding) as f:
                    reader = csv.reader((line.replace('\0','') for line in f))
                    l = [row for row in reader]
                    if len(l) > 0: 
                        self.field_names = l[0]
                        if len(l) > 1: self.list = l[1:]
                    else:
                        raise Exception("Error : Need to define columns before creating a vacant csv_file.")
        else:
            dirs_or_filename = file_path.split("/")
            wd = ""
            for i in range(0,len(dirs_or_filename)-1):
                wd += dirs_or_filename[i]+"/"
                if not(os.path.exists(wd)):
                    os.mkdir(wd)
            os.system("touch {}".format(file_path))
            if self.columns == None:
                raise Exception("Error : Need to define columns before creating a new csv_file.")
            self.export()

    def set_column_field(self,list=None):
        if list == None:
            with open(self.file_path, mode='r',encoding=self.encoding) as f:
                reader = csv.reader((line.replace('\0','') for line in f))
                l = [row for row in reader]
                self.columns = l[0]
        else:
            self.columns = list

    def change_column_field(self,col_old_item,col_new_item,export=False):
        col = self.get_column_id(col_old_item)
        if col == None:
            return None
        else:
            self.columns[col] = col_new_item
        if export == True:
            self.export()
        return True

    def set_charset(self, charset=None):
        if charset == None:
            with open(self.csv_file, 'rb') as f:  # バイナリファイルとしてファイルをオープン
                b = f.read()
            try:
                charset = chardet.detect(b)['encoding']
            except Exception as e:
                print("Error: manager set_charset error ")
                return False    
        self.encoding = charset
        return self.encoding

    def get_file_path(self):
        return self.file_path

    def get_charset(self):# Noneの場合もある(ファイルが存在しない時)
        return self.encoding
    
    def get_column_id(self, target):
        i = 0
        for name in self.columns:
            if name == target:
                return i
            i += 1
        return None
    
    def get_column_field(self):
        return self.columns

    def get_len(self, include_col_field=True):
        if include_col_field == True:
            return len(self.list)+1
        else:
            return len(self.list)

    def get_rows(self, include_name_field=True):
        if include_name_field == True:
            yield self.field_names
        if len(self.list)>0:
            for row in self.list:
                yield row

    def get_row(self,index):# ($index)行を取得する
        if type(index) == int and 0 == index:
            return self.columns
        if type(index) == int and 0 < index and index <= len(self.list):
            return self.list[index-1]
        else:
            return False
    
    def get_column(self,column,include_col_field=False): #($column_id)列を取得する
        if type(column) == str:
            column =  self.get_column_id(column)
        out_list = []
        if include_col_field == True:
            out_list += [self.columns[column]]
        out_list += self.list
        return out_list

    def get_item(self,index,column):# ($index)行($column_id)列成分を取得する
        if type(column) == str:
            column =  self.get_column_id(column)
        if type(index)==int and 0==index:
            return self.columns[column]
        elif type(index)==int and 0<index and index < self.get_len():
            return self.list[index-1][column]
        return False


    def is_include(self,column,target):
        # ($column)列を先頭から調べて、(target)に一致する行が見つかったらTrueを返す
        if type(column) == str:
            column =  self.get_column_id(column)
        data_array = [row[column] for row in self.list[1:]]
        return target in set(data_array)

    def get_index_if_include(self,target, column):
        # ($column)列を先頭から調べて、(target)に一致する行が見つかったらそこの行番号(idx)を返す
        data_array = [row[column] for row in self.list]
        index_position = None
        for idx in range(len(data_array)):
            if target == data_array[idx]:
                index_position = idx+1
                break
        return index_position

    def add_row(self, row, export=False):
        self.list.append(row)
        if export == True:
            self.export()

    def edit_row(self, row, index, export=False):
        # ($index)行を書き換える
        if index == 0:
            self.set_columns(row)
        elif 0 < index and index <= len(self.list):
            self.list[index-1]=row
        else:
            raise Exception("Error : edit_row() got a invalid index.")
        if export == True:
            self.export()

    def edit_item(self,index,column,new_data,export=False):
        if type(column) == str:
            column =  self.get_column_id(column)
        self.list[index-1][column] = new_data
        if export == True:
            self.export()

    def remove_row(self,index):
        if 1 <= index and index < self.get_len():
            self.list.pop(index-1)
            return True
        else:
            return False

    def exchange_column_by_column(self,column1,column2):
        if type(column1) == str:
            column1 =  self.get_column_id(column1)
        if type(column2) == str:
            column2 =  self.get_column_id(column2)
        if column1 == column2:
            return False
        buf = self.columns[column1]
        self.columns[column1]=self.columns[column2]
        self.columns[column2]=buf
        for index in range(0, self.get_len(include_col_field=False)):
            row = self.list[index]
            buf = row[column1]
            row[column1]=row[column2]
            row[column2]=buf
            self.list[index] = row
        return True


    def get_rows_sorted(self,column,reverse=False):
        if type(column) == str:
            column =  self.get_column_id(column)
        if column == 0:
            rows = sorted(self.list,reverse=reverse)
        else:
            self.exchange_column_by_column(0,column)
            rows = sorted(self.list,reverse=reverse)
            self.exchange_column_by_column(0,column)
        return rows


    def export(self,newline='',escapechar="\\",As=None):
        if As == None:
            out_file = self.file_path
        else:
            out_file = As
        with open(out_file, mode="w",newline=newline,encoding=self.encoding) as f:
            writer = csv.writer(f, escapechar=escapechar)
            l = []
            l.append(self.columns)
            for i in self.list:
                l.append(i)
            writer.writerows(l)

    def reset_file(self,export=False):
        self.list = []
        if export==True:
            self.export()
