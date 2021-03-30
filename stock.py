import pandas as pd
import json
from datetime import datetime
from operator import itemgetter
from itertools import groupby

def ParseChipCSV():
    # set stockcode
    stockCode = '1904'
    # date = datetime.now()
    # date_format = date.strftime('%Y%m%d')
    date_format = '20201029'

    original_df = pd.read_csv(r'./ChipData/csv/' + stockCode + '/'+ stockCode +'_' + date_format + '.csv',
                        encoding='big5hkscs',
                        delimiter='\t',
                        skiprows=[0, 1, 2],
                        header=None,
                        names=['head'])
    middle_df = original_df['head'].str.split(',', expand=True)
    middle_df.columns = ['序號1', '券商1', '價格1', '買進股數1', '賣出股數1', '', '序號2', '券商2', '價格2', '買進股數2', '賣出股數2']
    df1 = middle_df[['序號1', '券商1', '價格1', '買進股數1', '賣出股數1']]
    df2 = middle_df[['序號2', '券商2', '價格2', '買進股數2', '賣出股數2']]
    df1.columns = ['序號', '券商', '價格', '買進股數', '賣出股數']
    df2.columns = ['序號', '券商', '價格', '買進股數', '賣出股數']
    df = pd.concat([df1, df2])
    
    sliceEnd = len(df.index)
    output_df = df[0: sliceEnd-1]

    # convert data type
    output_df['序號'] = output_df['序號'].astype('int')
    output_df['價格'] = output_df['價格'].astype('float')
    output_df['買進股數'] = output_df['買進股數'].astype('int')
    output_df['賣出股數'] = output_df['賣出股數'].astype('int')
    
    # sort data
    output_df = output_df.sort_values('序號')

    # print(output_df)

    # output json
    out_json_str = output_df.to_json(orient='records', force_ascii=False)
    out_dict = json.loads(out_json_str)
    # print(type(out_dict))
    
    # groupby by 券商
    # out_dict.sort(key=itemgetter('券商'))
    # out_dict_g = groupby(out_dict, itemgetter('券商'))

    # for key, group in out_dict_g:
    #     for g in group:
    #         print(key, g)
    
    # generate list
    # out_obj = []
    # for key, group in out_dict_g:
    #     out_obj.append({'name': key, 'records': list(group)})
    # out_json = json.dumps(out_obj)

    return out_dict

# groupby by 券商
def GroupByBroker():
    originalData = ParseChipCSV()
    originalData.sort(key=itemgetter('券商'))
    out_dict_g = groupby(originalData, itemgetter('券商'))
    
    # generate list
    out_obj = []
    for key, group in out_dict_g:
        out_obj.append({'name': key, 'records': list(group)})
    out_json = json.dumps(out_obj)

    return out_json

# groupby by 價格
def GroupByPrice():
    originalData = ParseChipCSV()
    originalData.sort(key=itemgetter('價格'), reverse=True)
    out_dict_g = groupby(originalData, itemgetter('價格'))
    
    # generate list
    out_obj = []
    for key, group in out_dict_g:
        out_obj.append({'price': key, 'records': list(group)})
    out_json = json.dumps(out_obj)

    return out_json