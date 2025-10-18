
#  查询每天新注册用户数量（按 signup_date 分组）
SELECT signup_date, COUNT(user_id) AS new_users_count
FROM users
GROUP BY signup_date
ORDER BY signup_date;


#  查询最近 7 天每天的活跃用户数（即当天有事件记录的 user_id 数量）
SELECT timestamp, COUNT(DISTINCT user_id) AS active_users_count
FROM events
WHERE timestamp >= (SELECT MAX(timestamp) - 6 FROM events)
GROUP BY timestamp
ORDER BY timestamp;


#  查询每个用户的事件总数和最常见的事件类型
SELECT e.user_id, COUNT(e.event_type) AS event_count,
       (SELECT event_type
        FROM events
        WHERE user_id = e.user_id
        GROUP BY event_type
        ORDER BY COUNT(*) DESC
        LIMIT 1) AS most_common_event_type
FROM events e
GROUP BY e.user_id;

#查询男性与女性用户的平均事件数是否有差异
SELECT u.gender, AVG(sub.event_count) AS average_event_count
FROM users u
JOIN (
    SELECT user_id, COUNT(event_type) AS event_count
    FROM events
    GROUP BY user_id
) sub ON u.user_id = sub.user_id
WHERE u.gender IN ('Male', 'Female')
GROUP BY u.gender;
