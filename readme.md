#API 文档

# Hackday API
redis结构:
`(username, group, [timelist...])`

## 发起/填写
|URL|Method|
|---|---|
|/api/givetime/|POST|
**POSTDATA**
```
{
    "username":"String",
    "groupname":"String",
    "start_date":"String",
    "time":[0,1,0,1....]
    //总共7天，每天48个时间块.空闲为0,不空闲为1.
    //第一块为0:00,第二块为0:30这样
}
```
**RESPONSE**

**Group重复或用户名**返回状态码 403
**成功**返回状态码 200


## 获取团队时间
redis结构:
`((date,hour), member, member_number)`
|URL|Method|
|---|---|
|/api/gettime/|POST|
**POST DATA**
```
{
    "groupname":"String",
    "start_date":"String"
}
```

**RESPONSE DATA**
```
{
    "date1":{
        "hour1":{
            "member":{
                "name1",
                "name2",
                "name3"
            },
            "member_count":Int
        },
        "hour2":{
            "member":{
                "name1",
                "name2",
                "name3"
            },
            "member_count":Int
        },
        ......
        每天48个时间块
    },
    "date2":{
        "hour1":{
            "member":{
                "name1",
                "name2",
                "name3"
            },
            "member_count":Int
        },
        "hour2":{
            "member":{
                "name1",
                "name2",
                "name3"
            },
            "member_count":Int
        },
        ......
        每天48个时间块
    },
    ... ...
}
```
