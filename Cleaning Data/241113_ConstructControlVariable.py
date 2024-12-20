import pandas as pd
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 2000)
import numpy as np



input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\1_FirmBasicSituation.xlsx"
Base_file = pd.read_excel(input_file)
Base_file.drop(index=[0, 1], inplace=True)  # 删除前两行，注意变量名问题；替换原有的Dataframe
columns_to_keep = ['Symbol', 'EndDate', 'IndustryCode', 'RegisterAddress', 'RegisterLongitude', 'RegisterLatitude',
                   'EstablishDate', 'RegisterCapital', 'LISTINGDATE', 'PROVINCECODE', 'CITYCODE']
# 经纬度在此选取了注册地，该表中还包括了办公地经纬度；
# age1代表自注册日的年份，age2代表自上市日的年份。
new_column_names = {
    'Symbol': 'stock',
    'EndDate': 'year',
    'IndustryCode': 'industry',
    'RegisterAddress': 'Reg_address',
    'RegisterLongitude': 'lng',
    'RegisterLatitude': 'lat',
    'EstablishDate': 'age1',
    'RegisterCapital': 'reg_capital',
    'LISTINGDATE': 'age2',
    'PROVINCECODE': 'province',
    'CITYCODE' : 'city'
}
Base_file = Base_file[columns_to_keep].rename(columns=new_column_names)
Base_file['year'] = Base_file['year'].astype(str).str[:4].fillna(0).astype(int)  # 提取年份并转换为整数
Base_file['age1'] = Base_file['age1'].fillna(0).astype(str).str[:4].astype(int)
Base_file['age2'] = Base_file['age2'].fillna(0).astype(str).str[:4].astype(int)
columns_to_keep_as_is = ['industry', 'Reg_address']
for col in new_column_names.values():
    if col not in columns_to_keep_as_is:
        Base_file[col] = pd.to_numeric(Base_file[col], errors='coerce')

output_file1 = "E:\\科研\\自备资料\\控制变量面板数据生成\\1_FirmBasicSituation(done).xlsx"
Base_file.to_excel(output_file1, index=False)


########2222222222222######################################


input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\2_ProfitExcel.xlsx"
Profit_statement = pd.read_excel(input_file, skiprows=[0])
Profit_statement.drop(index=[0], inplace=True)
Profit_statement = Profit_statement[Profit_statement['报表类型'] == 'A']
columns_to_keep = ['证券代码', '统计截止日期', '营业总收入', '营业收入',
                   '营业总成本', '营业成本','管理费用', '研发费用','利润总额','净利润']
new_column_names = {
    '证券代码': 'stock',
    '统计截止日期': 'year',
    '营业总收入': 'T_revenue',
    '营业收入': 'revenue',
    '营业总成本': 'T_cost',
    '营业成本': 'cost',
    '管理费用': 'M_expenses',
    '研发费用': 'RD_expenses',
    '利润总额': 'T_profit',
    '净利润' : 'N_profit'
}
# revenue 和 T_revenue 往往是相同的，且revenue没有后者数据全，因此直接用T更全面，但其他花费等两者间并不等同。
Profit_statement = Profit_statement[columns_to_keep].rename(columns=new_column_names)
Profit_statement['year'] = Profit_statement['year'].astype(str).str[:4].fillna(0).astype(int)
for col in new_column_names.values():
        Profit_statement[col] = pd.to_numeric(Profit_statement[col], errors='coerce')
Profit_statement = Profit_statement.groupby(['stock', 'year']).agg(
    lambda x: x.sum() if not x.isna().all() else pd.NA).reset_index()
print(Profit_statement.head())
Profit_statement['growth'] = Profit_statement.groupby('stock')['T_revenue'].pct_change()

output_file2 = "E:\\科研\\自备资料\\控制变量面板数据生成\\2_ProfitExcel(done).xlsx"
Profit_statement.to_excel(output_file2, index=False)



#########33333333333333333##############################


input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\3_CashFlowTable.xlsx"
Cashflow_statement = pd.read_excel(input_file, skiprows=[0])
Cashflow_statement.drop(index=[0], inplace=True)
Cashflow_statement = Cashflow_statement[Cashflow_statement['报表类型'] == 'A']
columns_to_keep = ['证券代码', '统计截止日期', '经营活动产生的现金流量净额']
new_column_names = {
    '证券代码': 'stock',
    '统计截止日期': 'year',
    '经营活动产生的现金流量净额': 'NC_flow'
}
Cashflow_statement = Cashflow_statement[columns_to_keep].rename(columns=new_column_names)
Cashflow_statement['year'] = Cashflow_statement['year'].astype(str).str[:4].fillna(0).astype(int)
for col in new_column_names.values():
        Cashflow_statement[col] = pd.to_numeric(Cashflow_statement[col], errors='coerce')
Cashflow_statement = Cashflow_statement.groupby(['stock', 'year']).agg(
    lambda x: x.sum() if not x.isna().all() else pd.NA).reset_index()
output_file3 = "E:\\科研\\自备资料\\控制变量面板数据生成\\3_CashFlowTable(done).xlsx"
Cashflow_statement.to_excel(output_file3, index=False)
print(Cashflow_statement.head())


########4444444444444444###############################


input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\4_BalanceSheet.xlsx"
Balance_statement = pd.read_excel(input_file, skiprows=[0])
Balance_statement.drop(index=[0], inplace=True)
Balance_statement = Balance_statement[Balance_statement['报表类型'] == 'A']
columns_to_keep = ['证券代码', '统计截止日期', '其他应收款净额','资产总计', '负债合计', '所有者权益合计']
new_column_names = {
    '证券代码': 'stock',
    '统计截止日期': 'year',
    '其他应收款净额': 'NO_receive',
    '资产总计': 'T_assets',
    '负债合计': 'T_debt',
    '所有者权益合计': 'T_oequity'
}
Balance_statement = Balance_statement[columns_to_keep].rename(columns=new_column_names)
Balance_statement['year'] = Balance_statement['year'].astype(str).str[:4].fillna(0).astype(int)
for col in new_column_names.values():
        Balance_statement[col] = pd.to_numeric(Balance_statement[col], errors='coerce')
Cashflow_statement = Balance_statement.groupby(['stock', 'year']).agg(
    lambda x: x.sum() if not x.isna().all() else pd.NA).reset_index()
output_file4 = "E:\\科研\\自备资料\\控制变量面板数据生成\\4_BalanceSheet(done).xlsx"
Cashflow_statement.to_excel(output_file4, index=False)


#######55555555555555################################


input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\5_CG_ManagerShareSalary.xlsx"
Manage1_statement = pd.read_excel(input_file, skiprows=[0])
print(Manage1_statement.head())
Manage1_statement.drop(index=[0], inplace=True)
print(Manage1_statement.head())
Manage1_statement = Manage1_statement[Manage1_statement['统计口径'] == 1]
## 统计口径 == 1 意味着年末在职人员；2意味着本年度所有人员（包含离职、在职、退休等人员）;此处暂选1。
# 在初始清洗的过程中，一开始使['统计口径'] == '1'，每次结果dataframe都为空。 
# 百思不得解，福至心灵，想起原口径列可能为数值型，而筛选为文本型，故筛选后结果为空。
columns_to_keep = ['证券代码', '统计截止日期', '董事人数','其中：女性董事人数', '其中：独立董事人数', '董事会持股数量',
                   '监事会持股数量', '高级管理人员持股数量']
new_column_names = {
    '证券代码': 'stock',
    '统计截止日期': 'year',
    '董事人数': 'Num_board',
    '其中：女性董事人数': 'Num_Fboard',
    '其中：独立董事人数': 'Num_Iboard',
    '董事会持股数量': 'Num_B_shares',
    '监事会持股数量': 'Num_S_shares',
    '高级管理人员持股数量': 'Num_SM_shares'
}
print(Manage1_statement.columns)
Manage1_statement = Manage1_statement[columns_to_keep].rename(columns=new_column_names)
print(Manage1_statement.head())
Manage1_statement['year'] = Manage1_statement['year'].astype(str).str[:4].fillna(0).astype(int)
print(Manage1_statement.head())
for col in new_column_names.values():
        Manage1_statement[col] = pd.to_numeric(Manage1_statement[col], errors='coerce')
output_file5 = "E:\\科研\\自备资料\\控制变量面板数据生成\\5_CG_ManagerShareSalary(done).xlsx"
Manage1_statement.to_excel(output_file5, index=False)


#########66666666666666666##############################


input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\6_TotalShares.xlsx"
Manage2_statement = pd.read_excel(input_file, skiprows=[0])
Manage2_statement.drop(index=[0], inplace=True)
new_column_names = {
    '证券代码': 'stock',
    '统计截止日期': 'year',
    '总股数': 'T_shares'
}
Manage2_statement = Manage2_statement.rename(columns=new_column_names)
print(Manage2_statement.head())
Manage2_statement['year'] = Manage2_statement['year'].astype(str).str[:4].fillna(0).astype(int)
for col in new_column_names.values():
        Manage2_statement[col] = pd.to_numeric(Manage2_statement[col], errors='coerce')
output_file6 = "E:\\科研\\自备资料\\控制变量面板数据生成\\6_TotalShares(done).xlsx"
Manage2_statement.to_excel(output_file6, index=False)
print(Manage2_statement.head())


#########777777777777777##############################


input_file = "E:\\科研\\自备资料\\控制变量面板数据生成\\7_RelativeiValueIn.xlsx"
Relativeindex_statement = pd.read_excel(input_file, skiprows=[0])
Relativeindex_statement.drop(index=[0], inplace=True)

columns_to_keep = ['股票代码', '统计截止日期', '托宾Q值A', '托宾Q值B', '托宾Q值C',
                   '托宾Q值D', '账面市值比A', '账面市值比B']
new_column_names = {
    '股票代码': 'stock',
    '统计截止日期': 'year',
    '托宾Q值A': 'tobinq_A',
    '托宾Q值B': 'tobinq_B',
    '托宾Q值C': 'tobinq_C',
    '托宾Q值D': 'tobinq_D',
    '账面市值比A': 'BM_A',
    '账面市值比B': 'BM_B'
}
Relativeindex_statement = Relativeindex_statement[columns_to_keep].rename(columns=new_column_names)
Relativeindex_statement['year'] = Relativeindex_statement['year'].astype(str).str[:4].fillna(0).astype(int)
print(Relativeindex_statement.head())
for col in new_column_names.values():
        Relativeindex_statement[col] = pd.to_numeric(Relativeindex_statement[col], errors='coerce')
Relativeindex_statement = Relativeindex_statement.groupby(['stock', 'year']).agg(
    lambda x: x.mean() if not x.isna().all() else pd.NA).reset_index()
##原文中各年份基本是按照季度取TobinQ和BM值，这里以年份为单位取平均
output_file7 = "E:\\科研\\自备资料\\控制变量面板数据生成\\7_RelativeiValueIn(done).xlsx"
Relativeindex_statement.to_excel(output_file7, index=False)
print(Relativeindex_statement.head())


#########888888888888888##############################


input_file1 = "E:\\科研\\自备资料\\控制变量面板数据生成\\8_ShareHold_a.xlsx"
input_file2 = "E:\\科研\\自备资料\\控制变量面板数据生成\\8_ShareHold_b.xlsx"
input_file3 = "E:\\科研\\自备资料\\控制变量面板数据生成\\8_ShareHold_c.xlsx"
output_path = "E:\\科研\\自备资料\\控制变量面板数据生成\\8_ShareHold(done).xlsx"
df1 = pd.read_excel(input_file1, usecols=[0,1,3,4], skiprows=[0])
df2 = pd.read_excel(input_file2, usecols=[0,1,3,4], skiprows=[0])
df3 = pd.read_excel(input_file3, usecols=[0,1,3,4], skiprows=[0])
df1.drop(index=[0], inplace=True)
df2.drop(index=[0], inplace=True)
df3.drop(index=[0], inplace=True)
BoardBalance = pd.concat([df1, df2, df3], ignore_index=True)
print(BoardBalance.head())
columns_to_keep = ['证券代码', '统计截止日期', '持股排名', '持股比例(%)']
new_column_names = {
    '证券代码': 'stock',
    '统计截止日期': 'year',
    '持股排名': 'rank',
    '持股比例(%)': 'percent'
}
BoardBalance = BoardBalance[columns_to_keep].rename(columns=new_column_names)
BoardBalance['rank'] = BoardBalance['rank'].fillna(0).astype(int)
BoardBalance['percent'] = BoardBalance['percent'].fillna(0).astype(int)
BoardBalance = BoardBalance.sort_values(by=['stock', 'year', 'rank'])
# 计算股权制衡度
# 按照 'stock' 和 'year' 分组计算
def calculate_balance(group):
    top_5_shareholders = group[group['rank'].between(2, 5)]['percent'].sum()  # 第二到第五大股东的持股比例之和
    first_shareholder = group[group['rank'] == 1]['percent'].values[0]  # 第一大股东的持股比例
    balance = top_5_shareholders / first_shareholder if first_shareholder != 0 else 0  # 防止分母为0
    return pd.Series({'balance': balance})

# 应用分组计算
balance_data = BoardBalance.groupby(['stock', 'year']).apply(calculate_balance).reset_index()
# 将结果保存到新的文件
balance_data.to_excel(output_path, index=False)

balance_data['year'] = balance_data['year'].astype(str).str[:4].fillna(0).astype(int)
balance_data['stock'] = balance_data['stock'].astype(int)
balance_data = balance_data.groupby(['stock', 'year']).agg(
    lambda x: x.mean() if not x.isna().all() else pd.NA).reset_index()

balance_data.to_excel(output_path, index=False)
print(balance_data.head())


#########0000000000000000##############################


file_paths = [
    "E:\\科研\\自备资料\\控制变量面板数据生成\\1_FirmBasicSituation(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\2_ProfitExcel(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\3_CashFlowTable(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\4_BalanceSheet(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\5_CG_ManagerShareSalary(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\6_TotalShares(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\7_RelativeiValueIn(done).xlsx",
    "E:\\科研\\自备资料\\控制变量面板数据生成\\8_ShareHold(done).xlsx"
]

# 读取第一个文件作为基础范围
base_data = pd.read_excel(file_paths[0])
base_data['stock'] = base_data['stock'].astype(int)
base_data['year'] = base_data['year'].astype(int)

# 遍历剩余文件，逐步横向拼接
for file_path in file_paths[1:]:
    # 读取当前文件
    current_data = pd.read_excel(file_path)
    # 确保 stock 和 year 列存在，并转换为 int 类型
    if 'stock' in current_data.columns and 'year' in current_data.columns:
        current_data['stock'] = current_data['stock'].astype(int)
        current_data['year'] = current_data['year'].astype(int)
    else:
        raise ValueError(f"{file_path} 中缺少 'stock' 或 'year' 列")
    # 按照 'stock' 和 'year' 范围横向拼接，以 base_data 为主
    base_data = pd.merge(base_data, current_data, on=['stock', 'year'], how='left')

# 检查结果
print(base_data.head())
# 保存合并后的数据为 CSV 格式
output_path = "E:\\科研\\自备资料\\控制变量面板数据生成\\0_Merged_Data(done).csv"
base_data.to_csv(output_path, index=False)
print(f"所有文件已成功合并并保存到 {output_path}")
print(base_data.info)




Original_path = "E:\\科研\\自备资料\\控制变量面板数据生成\\0_Merged_Data(done).csv"
output_path = "E:\\科研\\自备资料\\控制变量面板数据生成\\A_Variable_Data.csv"
ControlV_path = "E:\\科研\\自备资料\\控制变量面板数据生成\\A_Variable_Data(done).csv"
data = pd.read_csv(Original_path)
print(data.info())
# 新增指标计算
data['企业年龄1'] =  np.log(data['year'] - data['age1'] + 1)
data['企业年龄2'] =  np.log(data['year'] - data['age2'] + 1)
data['股权制衡度'] = data['balance']
data['账面市值比A'] = data['BM_A']
data['账面市值比B'] = data['BM_B']
data['董事规模'] = np.log(data['Num_board'] + 1 )  # 董事会人数 +1 的自然对数
data['现金流状况'] = data['NC_flow'] / data['T_assets']  # 经营活动产生的现金流量净额/总资产
data['营业收入增长率'] = data['growth']  # 营业总收入的年度增长率
data['独立董事占比'] = data['Num_Iboard'] / data['Num_board']  # 独董人数/董事会人数
data['资产负债率'] = data['T_debt'] / data['T_assets']  # 总负债/总资产
data['管理层费用率'] = data['M_expenses'] / data['T_revenue']  # 管理费用/营业总收入
data['管理层持股比例'] = (data['Num_B_shares'] + data['Num_S_shares'] + data['Num_SM_shares']) / data['T_shares']  # 持股总数/总股数
data['大股东资金占用'] = data['NO_receive'] / data['T_assets']  # 其他应收款/总资产
data['总资产收益率'] = data['N_profit'] / data['T_assets']  # 净利润/总资产
data['净资产收益率'] = data['N_profit'] / data['T_oequity']  # 净利润/净资产(所有者权益)
data['公司规模'] = np.log(data['T_assets'])  # 总资产的自然对数
data['总资产周转率'] = data['T_revenue'] / data['T_assets']  # 营业总收入/总资产
data['托宾Q值A'] = data['tobinq_A']
data['托宾Q值B'] = data['tobinq_B']
data['托宾Q值C'] = data['tobinq_C']
data['托宾Q值D'] = data['tobinq_D']

# 替换除以零或计算失败的结果为NaN
data.replace([np.inf, -np.inf], np.nan, inplace=True)

data.to_csv(output_path, index=False)
# 将计算完的完整数据保存进一个完整的表格

columns_to_keep = [
    # 需要从大表中提取的变量（如有必要的话，其实大表也不错）
    'stock', 'year', 'industry', 'province', 'city',
    '企业年龄1', '企业年龄2', '股权制衡度', '账面市值比A', '账面市值比B',
    '董事规模', '现金流状况', '营业收入增长率', '独立董事占比',
    '资产负债率', '管理层费用率', '管理层持股比例', '大股东资金占用',
    '总资产收益率', '净资产收益率', '公司规模', '总资产周转率', '托宾Q值A',
    '托宾Q值B', '托宾Q值C', '托宾Q值D'
]

# 从原始数据框中筛选出这些列，并创建一个新的数据框
selected_data = data[columns_to_keep]
selected_data.to_csv(ControlV_path, index=False)
print(f"计算完成，结果已保存到 {ControlV_path}")
