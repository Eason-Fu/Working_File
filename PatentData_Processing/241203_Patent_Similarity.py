import os
os.environ["HF_ENDPOINT"]= 'https://hf-mirror.com'
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer,util
import time

'''
# 首先预处理之前已经匹配完的专利数据
# 仅保留为计算专利相似度而需要的变量
###############################################
input_file = "E:\科研\ResearchTrainingProject\Processed_Incopat_data\PatentData_withStock.xlsx"
output_file = "E:\科研\ResearchTrainingProject\Processed_Incopat_data\PatentData_withStock(done).xlsx"

file = pd.read_excel(input_file)
columns_to_keep = ['标题 (中文)', '摘要 (中文)', '申请日','专利类型','stock']  # 替换为实际需要的列名
new_column_names = {
    '标题 (中文)': 'title',
    '摘要 (中文)': 'abstract',
    '申请日': 'year',
    '专利类型': 'type',
    'stock': 'stock'
}
file = file[columns_to_keep].rename(columns=new_column_names)
file['year'] = file['year'].astype(str).str[:4].fillna(0).astype(int)
valid_types = ['发明申请', '实用新型', '外观设计']
file = file[file['type'].isin(valid_types)]
file.to_excel(output_file, index=False)
'''

'''
# 参考241111，对匹配数据进行分组——每6年为一个周期
# 分组后再求取 Embedding，计算相似度
###############################################
input_file2 = "E:\科研\ResearchTrainingProject\Processed_Incopat_data\PatentData_withStock(done).xlsx"
data = pd.read_excel(input_file2)
for start_year in range(2018, 2020):
    end_year = start_year + 5  # 每个区间的结束年份
    subset_data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]  # 筛选年份区间
    subset_data = subset_data.sort_values(by=['year', 'stock'])
    output_path = f"E:\科研\ResearchTrainingProject\Processed_Incopat_data\Patent_{start_year}_{end_year}.csv"
    subset_data.to_csv(output_path, index=False)
print("所有年份区间的数据提取完成并保存。")
'''


# 针对已经完成切割的年份分组数据，
# 修改导入文件名，目标结果年份名和输出结果名。以得到结果。
###############################################
def measure_and_reset_time(start_time):
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"计算耗时: {elapsed_time:.6f} 秒")
    return time.perf_counter()

start_time = time.perf_counter()

file_path = "E:\科研\ResearchTrainingProject\Processed_Incopat_data\Patent_2018_2023.csv"
data = pd.read_csv(file_path)

model = SentenceTransformer('BAAI/bge-large-zh-v1.5', trust_remote_code=True, device='cuda')
abstracts = data['abstract'].tolist()
embeddings = model.encode(abstracts, show_progress_bar=True)
data['embedding'] = list(embeddings)

start_time = measure_and_reset_time(start_time)############我是时间测量仪############

# 将嵌入向量转换为 NumPy 数组
embeddings = np.array(data['embedding'].tolist())
# 保存为压缩文件
np.savez_compressed('E:\科研\ResearchTrainingProject\Processed_Incopat_data\(18_23)embeddings.npz', embeddings=embeddings)
# 如果需要读取本次计算的 embedding，可以采用
# loaded_data = np.load('E:\科研\ResearchTrainingProject\Processed_Incopat_data\embeddings.npz')
# embeddings = loaded_data['embeddings']

# 仅保留目标年的专利数据进行相似度计算
target_year = 2023
current_data = data[data['year'] == target_year]
# 提取前五年的数据
past_data = data[(data['year'] >= target_year - 5) & (data['year'] < target_year)]
past_embeddings = np.array(past_data['embedding'].tolist()) if not past_data.empty else None
# 计算目标年每条专利的平均相似度
current_similarities = []
for embedding in current_data['embedding']:
    current_embedding = np.array(embedding).reshape(1, -1)
    if past_embeddings is not None:
        similarities = cosine_similarity(current_embedding, past_embeddings)
        current_similarities.append(np.mean(similarities))
    else:
        current_similarities.append(None)
# 更新数据的 'Sim' 列
current_data.loc[:, 'Sim'] = current_similarities

start_time = measure_and_reset_time(start_time)

# 保存结果
current_data.drop(columns=['embedding'], inplace=True)
outfile_path = 'E:\\科研\\ResearchTrainingProject\\Processed_Incopat_data\\(23)PatentData_withSim.xlsx'
current_data.to_excel(outfile_path, index=False)