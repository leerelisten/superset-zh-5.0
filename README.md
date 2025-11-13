# superset 汉化 5.0.0
## 1. 配置文件
``` bash
环境变量配置文件
./docker/.env

superset配置文件：
./docker/pythonpath_dev/superset_config_docker.py
```

## 2. 启动命令
``` bash
docker compose -f docker-compose-image-tag.yml up --build -d
```

## 3. 翻译优化
###  翻译流程

1. 汉化文件结构

* superset/translations/messages.pot，翻译配置文件，在文件中的才翻译
* superset/translations/zh/LC_MESSAGES/messages.po 后端翻译文件
* superset/translations/zh/LC_MESSAGES/messages.json 前端翻译配置文件
* superset/translations/zh/LC_MESSAGES/messages.mo 翻译二进制编译文件

2. 后续新增翻译流程

   1. 在messages.pot中新增（如没有）

   2. 在messages.po 和 messages.json中新增条项

   3. 编译翻译文件，生成messages.mo

      ``` bash
      cd ./superset
      pybabel compile -d translations
      ```

   4. 重启服务

