import pandas as pd
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 2000)
import os

'''
# 借241111_InitialProcessing 文件一用，首先预清洗原4.98G上市企业专利数据明细为
# 仅包含股票代码、专利申请号的版本

input_file = 'E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\上市公司-专利明细数据完整版（1988-2023年）.csv'
output_file = 'E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\清洗版上市公司专利明细2005-2023.csv'
chunk_size = 100000  # 依据内存容量调整此值（每次读取10万行）
for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    print("当前块的前几行：")
    print(chunk.head())  # 展示所有列和数据
    # 仅展示第一个块的前几行
    break
columns_to_keep = ['code', '股票代码', '专利申请号','专利申请年份']  # 替换为实际需要的列名
new_column_names = {
    'code': 'code',
    '股票代码': 'stock',
    '专利申请号': 'Application',
    '专利申请年份': 'year'
}
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
'''
# 加载A表数据，请注意，A表（即马克数据网给出的所有上市企业的专利数据）的专利申请号变量名为Application。
# 而B表们（即从 Incopat下载的171个检索条目结果文件，包含了上市公司和其他的企业/科研机构/学校，
# 其专利申请号变量名为“申请号”
file_a = "E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\清洗版上市公司专利明细2005-2023.csv"
df_a = pd.read_csv(file_a, usecols=["code", "Application"])
df_a = df_a.drop_duplicates(subset="Application", keep="first")
df_a.set_index("Application", inplace=True)  # 将申请号设置为索引，加快匹配速度

# 处理B文件夹
folder_b = "E:\科研\ResearchTrainingProject\Incopat_data"
output_file = "E:\科研\ResearchTrainingProject\Processed_Incopat_data\merged_stock_data.xlsx"  # 指定输出文件夹

# 创建一个空列表用于存储匹配结果
matched_data = []
# 遍历B文件夹中的每个xlsx文件
for file_name in os.listdir(folder_b):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(folder_b, file_name)
        # 读取B表数据
        df_b = pd.read_excel(file_path)
        # 匹配A表中的上市公司信息
        df_b["stock"] = df_b["申请号"].map(df_a["code"])  # 进行匹配
        # 筛选出匹配成功的记录（非空stock）
        df_matched = df_b[df_b["stock"].notna()]
        matched_data.append(df_matched)  # 添加到结果列表
        print(f"Processed {file_name}")

# 合并所有匹配到的数据
result_df = pd.concat(matched_data, ignore_index=True)
# 保存合并后的数据为Excel文件
result_df.to_excel(output_file, index=False)
print(f"All files processed and merged into {output_file}")
