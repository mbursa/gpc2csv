#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import sys
import csv
from datetime import datetime
import locale

# set czech locale for float number formating
locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')

GPC_TYPE_REPORT = '074'
GPC_TYPE_ITEM   = '075'
INPUT_ENCODING = 'windows-1250'

if (sys.version_info < (3,0)):
    print("The script needs to run under Python3")
    print("Usage: python3 %s input_file [output_file]" % sys.argv[0])
    sys.exit(1)


class GPC_Reader:

    def parse_gpc_record(self, line):
        rec_type = line[0:3]
        result = {
            'type': rec_type
        }
        
        if rec_type == GPC_TYPE_REPORT:
            #print line
            result['account_number'] = line[3:19]
            result['account_name'] = line[19:39].strip()
            result['old_balance_date'] = datetime.strptime(line[39:45],'%d%m%y').strftime('%d.%m.%Y')
            result['old_balance_value'] = int(line[59:60] + line[45:59])/100.0
            result['new_balance_value'] = int(line[74:75] + line[60:74])/100.0
            result['debit_value'] = int(line[89:90] + line[75:89])/100.0
            result['credit_value'] = int(line[104:105] + line[90:104])/100.0
            result['statement_number'] = line[105:108]
            result['date'] = datetime.strptime(line[108:114],'%d%m%y').strftime('%d.%m.%Y')
        elif rec_type == GPC_TYPE_ITEM:
            #print line
            result['own_account'] = line[3:19]
            result['external_account'] = line[19:35] + '/' + line[73:77]
            result['record_number'] = line[35:48]
            result['value'] = int(line[48:60])/100.0
            result['value_code'] = int(line[60:61])
            result['variable_symbol'] = int(line[61:71])
            result['constant_symbol'] = line[77:81]
            result['specific_symbol'] = int(line[81:91])
            result['client_name'] = line[97:117].strip()
            result['currency_code'] = line[117:122]
            result['due_date'] = datetime.strptime(line[122:128],'%d%m%y').strftime('%d.%m.%Y')
            if ((result['value_code']==1) or (result['value_code']==4)): result['value'] = -result['value']

            # convert value to string            
            result['value'] = locale.format_string("%.2f", result['value'])
        else:
            raise Exception('Invalid GPC record type (%s)' % (rec_type))
            
        return result
    #end def
    
    
    def csv_output(self, output_file):
        # czech names for the gpc fields
        field_names_cz = {
            'type': 'typ záznamu',
            'own_account': 'vlastní účet',
            'external_account': 'účet protistrany',
            'record_number': 'pořadové číslo',
            'value': 'částka',
            'value_code': 'kód účtování',
            'variable_symbol': 'VS',
            'constant_symbol': 'KS',
            'specific_symbol': 'SS',
            'client_name': 'název účtu prostistrany',
            'currency_code': 'kód měny',
            'due_date': 'datum zaúčtování'
        }

        # fields to export
        fields = list(self.gpc_data[0].keys())
        fields.remove('type')
        
        # czech translation of export fields
        fields_cz = [field_names_cz.get(n,n) for n in fields]

        fp = open(output_file, 'w') if (output_file) else sys.stdout
        w = csv.DictWriter(fp, fieldnames=fields, extrasaction='ignore', dialect='excel')
        w.writerow(field_names_cz) #print header with translated field names
        w.writerows(self.gpc_data)
        if (output_file): fp.close()
    #end def
    
    
    def read(self, filename):
        self.gpc_data = []
        with open(filename, 'r', encoding=INPUT_ENCODING) as fp:  
            for line in fp:
                r = self.parse_gpc_record(line)
                # only include transaction records to the output
                if (r['type'] == GPC_TYPE_ITEM): self.gpc_data.append(r)
    #end def

#end class


if (len(sys.argv) <= 1):
    print("Missing input file argument.")
    print("Usage: python3 %s input_file [output_file]" % sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2] if (len(sys.argv) >= 3) else None

if (not os.path.isfile(input_file)):
    print("Input file does not exits.")
    print("Usage: python3 %s input_file [output_file]" % sys.argv[0])
    sys.exit(1)
    
gpc = GPC_Reader()
gpc.read(sys.argv[1])
gpc.csv_output(output_file)


