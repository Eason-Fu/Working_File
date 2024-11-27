import pandas as pd

# 读取上市企业代码-工商统一社会信用代码对照表
input_file = "E:\\科研\\ResearchTrainingProject\\Incopat_data\\统一信用代码匹配\\USCC(done).xlsx"
df = pd.read_excel(input_file)

# 简化USCC函数：保留前三位和后三位，中间部分用 * 替代
def simplify_uscc(uscc):
    if isinstance(uscc, str) and len(uscc) > 5:  # 确保uscc是有效字符串并且长度大于5
        return uscc[:2] + '*' + uscc[-3:]  # 保留前三位和后三位（注意更新为后三位）
    return None  # 如果是无效值，返回None

# 应用简化USCC函数
df['simplified_uscc'] = df['uscc'].apply(simplify_uscc)

# 去除空值，并将所有简化版uscc连接成一条字符串
result_string = ' OR '.join(df['simplified_uscc'].dropna().unique())  # 使用unique()确保唯一性

# 打印结果字符串
print("连接后的简化USCC字符串：")
print(result_string)