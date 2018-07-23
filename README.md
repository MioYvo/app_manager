# 应用管理 APP Manager

## 部署
```bash
docker run -it -e TZ=Asia/Shanghai -v /data/app_data:/app_manager/sanic_manager/uploads --link postgres:postgres -e DB_HOST=postgres -e APP_PORT=8888 -p 8888:8888 --name am -d app_manager
```

## API
### list items
* Login required
* URL `GET`  `/`
* Query parameters

    |parameter|意义|默认值|要求|
    |---|---|---|---|
    |name|项目名字|`""`(空，不传)|英文字符|
    |platform|平台|`""`(空，不传)|`iOS` \| `Android` \| `""`(空)， 大小写不敏感|
    |page|页数|1| page > 0|
    |items|每页个数|10|50 >= items > 0|
    
    示例：
    `http://localhost:8888/?platform=iOS&page=1&items=10`


* Return
    
    * status code: `200 OK`
    
        ```json
        {
            "total_pages": 1,
            "page": 1,
            "items": 10,
            "total_items": 2,
            "content": [
                {
                    "id": 1,
                    "name": "zhdj",
                    "version": 1,
                    "platform": "iOS",
                    "is_active": true,
                    "file": "/downloads/iOS.acpm",
                    "create_at": "2018-07-23T10:47:59"
                },
                {
                    "id": 3,
                    "name": "zz",
                    "version": 3,
                    "platform": "iOS",
                    "is_active": false,
                    "file": "/downloads/aaa",
                    "create_at": null
                }
            ]
        }
        ```
        
        * 字段意义
        
            |字段名|意义|json类型|
            |---|---|---|
            |total_pages|总页数|number|
            |page|当前页数|number|
            |total_items|总个数|number|
            |items|每页个数|number|
            |content|消息内容|list|
            |is_active|是否激活|boolean|
            |create_at|创建时间|string or null|

---
### upload app file
* Login required
* URL `POST`  `/`
* Form parameters

    |parameter|意义|form类型|默认值|要求|
    |---|---|---|---|---|
    |app|文件|File|无||
    |name|名字|Text|无|英文字符|
    |platform|平台|Text|无| `iOS` or `Android`, 大小写不敏感|
    |version|版本号|Text|无|number|

    
    * Request Content-Type: `form-data`
    * 会检查 `name-platform-version-app(文件名)` 的唯一性

* Return

    * status code `201 Created`

---
### download current app file
* URL `GET` `/current/<platform>/download`
* Query parameters

    |parameter|意义|默认值|可选范围|
    |---|---|---|---|
    |platform|平台|无|`iOS` \| `Android` 大小写不敏感|
    
    示例：`http://localhost:8888/current/android` `http:localhost:8888/current/ios`
    
* Return

    * status code `200 OK` 下载文件

    * Response headers

        ```
        Content-Disposition: attachment; filename="wallpaper020-1920x1080.jpg"
        Content-Type: application/octet-stream
        Keep-Alive: 5
        Transfer-Encoding: chunked
        ```

---
### get current version
* Login required
* URL `GET` `/current/<platform>`
* Query parameters

    |parameter|意义|默认值|要求|
    |---|---|---|---|
    |platform|平台|无|`iOS` \| `Android` 大小写不敏感|
    
    示例：`http://localhost:8888/current/android` `http:localhost:8888/current/ios`
    
* Return

    * status code `200 OK`
        
        ```
        {
            "version": 1,
            "file": "/a",
            "platform": "ios",
            "create_at": "2018-07-23T15:05:30+00:00"
        }
        ```
        
        * 字段意义
        
            |字段名|意义|json类型|
            |---|---|---|
            | version |当前版本号|number or **null**|
            |platform|平台, `iOS` \| `Android` 大小写不敏感|string|
            | file |文件地址|string or **null**|
            |create_at|创建时间|string or **null**|




---
### active new version
* URL `PUT` `/app/<app_id>/active`

---
### deactive version
* URL `PUT` `/app/<app_id>/deactive`


