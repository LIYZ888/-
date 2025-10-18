import pandas as pd
import matplotlib.pyplot as plt

# 加载数据
users = pd.read_csv('./users.csv')
events = pd.read_csv('./event.csv')

print('用户基本信息数据基本信息：')
users.info()

# 查看用户基本信息数据集行数和列数
users_rows, users_columns = users.shape

if users_rows < 100 and users_columns < 20:
    # 短表数据（行数少于100且列数少于20）查看全量数据信息
    print('用户基本信息数据全部内容信息：')
    print(users.to_csv(sep='\t', na_rep='nan'))
else:
    # 长表数据查看数据前几行信息
    print('用户基本信息数据前几行内容信息：')
    print(users.head().to_csv(sep='\t', na_rep='nan'))

print('用户行为日志数据基本信息：')
events.info()

# 查看用户行为日志数据集行数和列数
events_rows, events_columns = events.shape

if events_rows < 100 and events_columns < 20:
    # 短表数据（行数少于100且列数少于20）查看全量数据信息
    print('用户行为日志数据全部内容信息：')
    print(events.to_csv(sep='\t', na_rep='nan'))
else:
    # 长表数据查看数据前几行信息
    print('用户行为日志数据前几行内容信息：')
    print(events.head().to_csv(sep='\t', na_rep='nan'))
plt.rcParams['figure.dpi'] = 300

# 将 signup_date 列转换为日期格式
users['signup_date'] = pd.to_datetime(users['signup_date'])

# 将 timestamp 列转换为日期时间格式
events['timestamp'] = pd.to_datetime(events['timestamp'], format='%Y/%m/%d %H:%M')

# 统计注册用户的性别分布
gender_distribution = users['gender'].value_counts()

# 创建一个 1 行 2 列的子图布局
fig, axes = plt.subplots(1, 2, figsize=(5, 3))

# 绘制用户年龄直方图
axes[0].hist(users['age'], bins=10, edgecolor='black')
axes[0].set_title('Histogram')
axes[0].set_xlabel('age')
axes[0].set_ylabel('Frequency')

# 统计注册用户按日期的数量
signup_trend = users['signup_date'].value_counts().sort_index()

# 绘制注册用户按日期统计的时间趋势图
axes[1].plot(signup_trend.index, signup_trend.values)
axes[1].set_title('datetime')
axes[1].set_xlabel('Registration Date')
axes[1].set_ylabel(' Number of Users')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

print('注册用户的性别分布：\n', gender_distribution)