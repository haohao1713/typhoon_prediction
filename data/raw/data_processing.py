import pandas as pd
from sklearn.preprocessing import StandardScaler

# 使用原始字符串避免转义问题
file_path = '1945-2023.xlsx'
# 使用read_csv读取CSV文件
data = pd.read_excel(file_path)
data.head()
# 将台风起始时间和结束时间转换为日期时间格式
data['台风起始时间'] = pd.to_datetime(data['台风起始时间'], errors='coerce')
data['台风结束时间'] = pd.to_datetime(data['台风结束时间'], errors='coerce')
# 计算持续时间（以天为单位），并添加为新列
data['台风持续时间'] = (data['台风结束时间'] - data['台风起始时间']).dt.total_seconds() / (24 * 3600)
# 删除含有缺失值的行
data_cleaned = data.dropna()
data_cleaned
# 导出清理后的数据到新的Excel文件
output_path = '../processed/台风数据_清洗.xlsx'
data_cleaned.to_excel(output_path, index=False)
output_path
# 读取清理后的台风数据
file_path = '海洋温度.xlsx'
data = pd.read_excel(file_path)

# 将时间特征转换为datetime格式
# 显式指定时间格式
time_format = '%Y-%m-%d %H:%M:%S'  # 根据实际时间格式调整

# 转换时间列
data['台风起始时间'] = pd.to_datetime(data['台风起始时间'], format=time_format, errors='coerce')
data['台风结束时间'] = pd.to_datetime(data['台风结束时间'], format=time_format, errors='coerce')
data['当前台风时间'] = pd.to_datetime(data['当前台风时间'], format=time_format, errors='coerce')

# 对'台风强度'进行自定义编码,比如台风强度中的T,D,S,Y分别为1234，比如其组合的热带低压（TD）则编码为12，
def encode_typhoon_intensity(intensity):
    mapping = {'T': '1', 'D': '2', 'S': '3', 'Y': '4'}
    encoded = ''.join([mapping[char] for char in intensity if char in mapping])
    return int(encoded) if encoded else 0

data['台风强度'] = data['台风强度'].apply(lambda x: encode_typhoon_intensity(x) if pd.notna(x) else 0)

# 对'移动方向'进行自定义编码移动方向，在中文汉字数据里面的的“偏，东，南，
# 西，北”为0,1，2，3，4，则 '西北偏北'则为3404
def encode_movement_direction(direction):
    mapping = {'偏': '0', '东': '1', '南': '2', '西': '3', '北': '4'}
    encoded = ''.join([mapping[char] for char in direction if char in mapping])
    return int(encoded) if encoded else 0
data['移动方向'] = data['移动方向'].apply(lambda x: encode_movement_direction(x) if pd.notna(x) else 0)
# 导出处理后的数据到新的Excel文件
output_path = '../processed/海洋温度_清洗.xlsx'
data.to_excel(output_path, index=False)

output_path


# 读取台风数据
file_path = '台风强度移动方向数值.xlsx'
data = pd.read_excel(file_path)

# 提取与台风路径预测相关的特征
features = ['移动速度', '气压', '风速', '移动方向', '台风强度', '台风等级']
time_features = ['台风起始时间', '台风结束时间', '当前台风时间']
target = ['经度', '纬度']

# 过滤数据并去除缺失值和非数值型特征值
data_filtered = data.dropna(subset=features + target + time_features)

# 将时间特征提取为数值特征
for time_feature in time_features:
    data_filtered[time_feature] = pd.to_datetime(data_filtered[time_feature])

# 提取时间特征（小时、天差等）
data_filtered['当前时间_小时'] = data_filtered['当前台风时间'].dt.hour
data_filtered['当前时间_月份'] = data_filtered['当前台风时间'].dt.month
data_filtered['持续时间_天'] = (data_filtered['台风结束时间'] - data_filtered['台风起始时间']).dt.total_seconds() / (24 * 3600)
data_filtered['已持续时间_天'] = (data_filtered['当前台风时间'] - data_filtered['台风起始时间']).dt.total_seconds() / (24 * 3600)

# 将非数值型特征转换为数值类型（例如 '移动方向'）
for feature in features:
    if data_filtered[feature].dtype == 'object':
        data_filtered[feature] = pd.factorize(data_filtered[feature])[0]
# 导出处理后的数据到新的Excel文件
output_path = '台风强度移动方向数值编码后.xlsx'
data.to_excel(output_path, index=False)
# 读取台风数据
file_path = '台风强度移动方向数值编码后.xlsx'
data = pd.read_excel(file_path)

# 数据清洗：去除缺失值和异常值
# 去除包含空值的行
data_cleaned = data.dropna()

# 去除异常值（例如，风速或气压超出合理范围的情况）
data_cleaned = data_cleaned[(data_cleaned['风速'] > 0) & (data_cleaned['气压'] > 0)]

# 将清洗后的数据导出到新的 Excel 文件
output_path = '../processed/台风强度移动方向数值编码_清洗后.xlsx'
data_cleaned.to_excel(output_path, index=False)

# 返回输出文件路径
output_path


# 读取上传的 Excel 文件
# 文件路径
file_1945_2023_path = '1945-2023.xlsx'
file_q3_path = '降水量与台风中心距离.xlsx'

# 加载 Excel 文件数据到 DataFrame
# data_1945_2023 包含 1945-2023 年台风数据
# data_q3 包含需要风速数据加入的表格数据
data_1945_2023 = pd.read_excel(file_1945_2023_path)
data_q3 = pd.read_excel(file_q3_path)

# 合并两个数据集，依据 '台风编号'、'经度' 和 '纬度' 这三列
# 使用左连接 (how='left')，确保 data_q3 中的所有数据保留，并加入匹配的风速数据
merged_data = pd.merge(data_q3, data_1945_2023[['台风编号', '经度', '纬度', '风速']], on=['台风编号', '经度', '纬度'], how='left')

# 将合并后的数据保存到新的 Excel 文件中
output_merged_path = '../processed/降水量与台风中心距离_清洗.xlsx'
merged_data.to_excel(output_merged_path, index=False)

# 打印合并后的文件路径
print(output_merged_path)






