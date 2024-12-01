import pandas as pd
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 2000)
import os

input_file = "E:\\科研\\ResearchTrainingProject\\Incopat_data\\统一信用代码匹配\\USCC.xlsx"
output_file1 = "E:\\科研\\ResearchTrainingProject\\Incopat_data\\统一信用代码匹配\\USCC(done).xlsx"
# 导入并处理CSMAR的统一信用代码文件
uscc_file = pd.read_excel(input_file, skiprows=[0])
uscc_file.drop(index=[0], inplace=True)
columns_to_keep = ['股票代码','统计截止日期', '统一社会信用代码']
uscc_file = uscc_file[columns_to_keep].rename(
    columns={'股票代码':'stock','统计截止日期':'year', '统一社会信用代码':'uscc'})
uscc_file['year'] = uscc_file['year'].astype(str).str[:4].astype(int)  # 提取年份并转换为整数
uscc_file['uscc'] = uscc_file.groupby('stock')['uscc'].transform(lambda x: x.ffill().bfill())
# lambda x: 定义一个匿名函数，x 表示每个分组的 uscc 列。
# ffill()（向前填充）：将当前分组内的空值替换为它前面的第一个非空值。
# bfill()（向后填充）：将当前分组内的空值替换为它后面的第一个非空值。
# 结合 ffill() 和 bfill()：确保无论空值出现在分组的前面、中间还是后面，都能被填充上相同的值。
print(uscc_file.head())
uscc_file.to_excel(output_file1, index=False)

#################################################################
####################接下来直接抄取241122文件########################

# 加载A表数据，A表（即CSMAR给出的所有上市企业的信用代码数据）的变量名为uscc。
# 而B表们（即从 Incopat下载的171个检索条目结果文件，包含了上市公司和其他的企业/科研机构/学校，
# 其专利申请号变量名为“工商统一社会信用代码”
# 加载A表数据
df_a = pd.read_excel(output_file1)
df_a = df_a.dropna().drop_duplicates(subset="uscc", keep="first")
df_a.set_index("uscc", inplace=True)  # 设置索引以加快匹配速度

# B文件夹路径
folder_b = "E:\\科研\\ResearchTrainingProject\\Incopat_data"
output_file = "E:\\科研\\ResearchTrainingProject\\Processed_Incopat_data\\PatentData_withStock.xlsx"
# 创建一个空的DataFrame用于存储匹配结果
matched_data = pd.DataFrame()
# 遍历B文件夹中的每个Excel文件
for file_name in os.listdir(folder_b):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(folder_b, file_name)
        # 读取B表数据
        df_b = pd.read_excel(file_path)
        if "工商统一社会信用代码" not in df_b.columns:
            print(f"警告: 文件 '{file_name}' 缺少'工商统一社会信用代码'列，已跳过处理。")
            continue  # 跳过当前文件并处理下一个文件
        # 确保"工商统一社会信用代码"列为字符串类型，处理可能的缺失值
        df_b["工商统一社会信用代码"] = df_b["工商统一社会信用代码"].astype(str).fillna("")
        # 拆分多值USCC并匹配
        df_b["stock"] = df_b["工商统一社会信用代码"].apply(
            lambda x: [df_a.loc[uscc.strip(), "stock"] for uscc in x.split(";") if uscc.strip() in df_a.index]
        )
        # 只保留匹配到stock的行，并将多值stock拆分为多行
        df_b = df_b[df_b["stock"].apply(bool)]  # 过滤出stock非空的行
        df_b = df_b.explode("stock", ignore_index=True)  # 将多值stock拆分为多行
        # 将匹配结果添加到最终结果DataFrame中
        matched_data = pd.concat([matched_data, df_b], ignore_index=True)
        print(f"Processed {file_name}")

# 保存合并后的数据为Excel文件
matched_data.to_excel(output_file, index=False)
print(f"All files processed and merged into {output_file}")