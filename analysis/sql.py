import sqlite3
import pandas as pd

# 读取 CSV 文件
users = pd.read_csv('./users.csv')
events = pd.read_csv('./event.csv')

# 创建 SQLite 数据库连接
conn = sqlite3.connect('./mydb.db')
users.to_sql('users', conn, if_exists='replace', index=False)
events.to_sql('events', conn, if_exists='replace', index=False)

# 任务 1: 查询每天新注册用户数量（按 signup_date 分组）
query1 = """
SELECT signup_date, COUNT(user_id) AS new_users_count
FROM users
GROUP BY signup_date
ORDER BY signup_date;
"""

# 任务 2: 查询最近 7 天每天的活跃用户数（即当天有事件记录的 user_id 数量）
query2 = """
SELECT timestamp, COUNT(DISTINCT user_id) AS active_users_count
FROM events
WHERE timestamp >= (SELECT MAX(timestamp) - 6 FROM events)
GROUP BY timestamp
ORDER BY timestamp;
"""

# 任务 3: 查询每个用户的事件总数和最常见的事件类型
query3 = """
SELECT e.user_id, COUNT(e.event_type) AS event_count, 
       (SELECT event_type
        FROM events
        WHERE user_id = e.user_id
        GROUP BY event_type
        ORDER BY COUNT(*) DESC
        LIMIT 1) AS most_common_event_type
FROM events e
GROUP BY e.user_id;
"""

# 任务 4: 查询男性与女性用户的平均事件数是否有差异
query4 = """
SELECT u.gender, AVG(sub.event_count) AS average_event_count
FROM users u
JOIN (
    SELECT user_id, COUNT(event_type) AS event_count
    FROM events
    GROUP BY user_id
) sub ON u.user_id = sub.user_id
WHERE u.gender IN ('Male', 'Female')
GROUP BY u.gender;
"""

# 执行查询并将结果存储在 DataFrame 中
result1 = pd.read_sql(query1, conn)
result2 = pd.read_sql(query2, conn)
result3 = pd.read_sql(query3, conn)
result4 = pd.read_sql(query4, conn)

# 关闭数据库连接
conn.close()

# 输出结果
print('每天新注册用户数量：')
print(result1)
print('\n最近 7 天每天的活跃用户数：')
print(result2)
print('\n每个用户的事件总数和最常见的事件类型：')
print(result3)
print('\n男性与女性用户的平均事件数：')
print(result4)