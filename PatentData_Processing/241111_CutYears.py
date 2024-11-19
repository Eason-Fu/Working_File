import pandas as pd

# 读取原始数据
file_path = "E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\清洗版上市公司专利明细2005-2023.csv"
data = pd.read_csv(file_path)

# 按年份循环提取指定区间数据并保存为Excel
for start_year in range(2005, 2018):
    end_year = start_year + 5  # 每个区间的结束年份
    subset_data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]  # 筛选年份区间

    # 构建文件名
    output_path = f"E:\科研\ResearchTrainingProject\上市公司-专利明细数据（1988-2023年）\Patent_{start_year}_{end_year}.csv"
    # 保存数据到Excel文件
    subset_data.to_csv(output_path, index=False)

print("所有年份区间的数据提取完成并保存。")