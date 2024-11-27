# 正因为Incopat每天的下载额度有限，因此需要精细自己的检索命令，以精确范围，尽可能快的下载所需内容。
# 由于其他数据都不准确，只能继续借助统一社会信用代码来锁定上市企业范围。
# 进一步延伸,可以用上市企业的社会统一信用代码前三位+后四位锁定上市企业，以基本在平台上检索确定是否属于上市企业。如931*5518，或941*535Y等。
# 为了试验该方法，我首先需要将USCC代码表的代码简化为使用统义符表达的形式，并连接成一句完整的文本。
# 自己手动实现过于困难，因此简单的针对一个含有stock,year,uscc三个变量的“上市代码-社会统一信用代码参考表”进行简化和连接的程序可参考该文件。



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

print("连接后的简化USCC字符串：")
print(result_string)
