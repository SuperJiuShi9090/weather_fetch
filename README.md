# QWEA_API - 天气查询工具

[![wakatime](https://wakatime.com/badge/user/007f3683-8bf2-46f8-a321-bd01d3ae784a.svg)](https://wakatime.com/@007f3683-8bf2-46f8-a321-bd01d3ae784a)

这是一款基于[和风天气API](https://qweather.com)的控制台异步天气查询工具。当然，您也可以直接调用api.py和GEO_API.py的函数来完成更多更高质量的项目  
~~写的比较简单，请见谅xwx~~

### 功能介绍：
1. 实时天气预报
2. 逐小时天气预报
3. 7日天气预报
4. 实时空气质量预报
5. 逐小时空气质量预报
6. 3日空气质量预报
7. 实时天气预警
8. 更实用的天气预报

### 环境要求：
 - python 3.8+  
 - [和风天气API](https://dev.qweather.com)

## 安装
安装依赖：
```powershell
pip install -r requirements.txt
```

本项目使用 [和风天气 API](https://qweather.com) 获取数据，[点此注册API](<https://id.qweather.com/%23/register>)。

版本号：<u>v1.7.0</u>

### 更新说明：
1. 新增了预警图片生成功能，便于用户更方便地获取预警信息。
2. 更新了即将失效的城市天气预报API接口并相应修改了json解析部分
3. 修复了其他已知bug，修改了json解析的逻辑，优化了部分输出结果。

关于API的详细文档请参阅[和风天气开发者文档](https://dev.qweather.com/docs/start/)。
