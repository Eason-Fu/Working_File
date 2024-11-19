import pandas as pd
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 2000)

input_file = 'E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\上市公司-专利明细数据完整版（1988-2023年）.csv'
output_file = 'E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\清洗版上市公司专利明细2005-2023.csv'
# 设置分块大小
chunk_size = 100000  # 依据内存容量调整此值（每次读取10万行）
for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    print("当前块的前几行：")
    print(chunk.head())  # 展示所有列和数据
    # 仅展示第一个块的前几行
    break


# 定义要保留的列和新列名
columns_to_keep = ['code', '股票代码', '行业代码','专利名称','专利类型','IPC分类号','摘要','专利申请年份']  # 替换为实际需要的列名
new_column_names = {
    'code': 'code',
    '股票代码': 'stock',
    '行业代码': 'industry',
    '专利名称': 'title',
    '专利类型': 'type',
    'IPC分类号': 'IPC',
    '摘要': 'digest',
    '专利申请年份': 'year'
}

# 分块读取并处理
for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size)):
    # 删除含有NaN的行
    chunk = chunk.dropna(subset=['专利申请年份'])
    # 处理年份列，去除小数部分
    chunk['专利申请年份'] = chunk['专利申请年份'].astype(int)  # 转换为整数，去除小数部分
    # 筛选出2005年及以后的数据
    chunk = chunk[chunk['专利申请年份'] >= 2005]
    # 保留指定列并重命名
    selected_chunk = chunk[columns_to_keep].rename(columns=new_column_names)
    # 写入到新的CSV文件中，首块写入时包含表头，之后追加数据
    selected_chunk.to_csv(output_file, mode='w' if i == 0 else 'a', index=False, header=(i == 0))

print("文件已保存至", output_file)