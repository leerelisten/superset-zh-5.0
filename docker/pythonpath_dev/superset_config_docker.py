import os
import sys
import logging
from typing import Optional
from celery.schedules import crontab
from datetime import timedelta
from flask import session
from flask import Flask
from redis import Redis

APP_NAME = "乐学数据平台"

 # 确保PyMySQL兼容性（如果使用MySQL）
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

SECRET_KEY = os.getenv("SECRET_KEY")


DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")



SQLALCHEMY_DATABASE_URI = f'{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 设置默认语言
BABEL_DEFAULT_LOCALE = "zh"
BABEL_DEFAULT_FOLDER = "superset/translations"
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "zh": {"flag": "cn", "name": "中文"}
}

# 高级属性
FEATURE_FLAGS = {
    "KV_STORE": True,
    "SHARE_QUERIES_VIA_KV_STORE": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ALERT_REPORTS": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DRILL_TO_DETAIL": True,
    "DRILL_BY": True,
    "HORIZONTAL_FILTER_BAR": True,
    "ALLOW_FULL_CSV_EXPORT": True,
    # 允许即席子查询
    "ALLOW_ADHOC_SUBQUERY": True,
    # 优化SQL,只支持谓词下推
    "OPTIMIZE_SQL": True,    # 在导航栏中添加一个开关，以便在浅色和深色主题之间轻松切换。
    "THEME_ENABLE_DARK_THEME_SWITCH": True,
    "DATASET_FOLDERS": True,
    "DASHBOARD_RBAC": True,
    "DASHBOARD_VIRTUALIZATION": True,
}




CELERY_BEAT_SCHEDULER_EXPIRES = timedelta(weeks=1)

# 缓存
class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    worker_prefetch_multiplier = 5
    task_acks_late = False
    task_annotations = {
        "sql_lab.get_sql_results": {
            "rate_limit": "100/s",
        },
    }
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
            "options": {"expires": int(CELERY_BEAT_SCHEDULER_EXPIRES.total_seconds())},
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),
        },
    }
# 使用 Redis
from flask_caching.backends.rediscache import RedisCache
CELERY_BEAT_SCHEDULER_EXPIRES = timedelta(weeks=1)
RESULTS_BACKEND = RedisCache(
    host=f'{REDIS_HOST}', port=REDIS_PORT, key_prefix='superset_results')

CELERY_CONFIG: type[CeleryConfig] = CeleryConfig
# 使PyMySQL兼容MySQLdb
# 缓存
# 仪表盘过滤器状态
FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_cache',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
}

# 探索图表表单数据缓存
EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_form_data_cache',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
}
# 元数据缓存
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_metadata_cache',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
}

# 从数据集查询的图表数据
DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_data_cache',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
}


## 限制下载行数
ROW_LIMIT = 100000  # or higher, depending on your needs
# 没有服务器端分页（前端限制）允许的最大行数。
TABLE_VIZ_MAX_ROW_CLIENT = 100000
# 启用服务器端分页时允许的最大行数。
TABLE_VIZ_MAX_ROW_SERVER = 500000



# webdriver
WEBDRIVER_TYPE = "firefox"
WEBDRIVER_OPTION_ARGS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--lang=zh_CN.UTF-8",  # 设置浏览器语言环境为中文（中国），使用UTF-8编码
    "--accept-lang=zh-CN,zh"  # 可选：明确告知服务器优先接收简体中文内容
]

# 邮件功能
# smtp服务器配置
# smtp server configuration
SMTP_HOST = "smtp.exmail.qq.com"
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = "bigdata@tangdou.com"
SMTP_PORT = 25
SMTP_PASSWORD = "5bDF5G8JiGvWC2i4"
SMTP_MAIL_FROM = "bigdata@tangdou.com"
SMTP_SSL_SERVER_AUTH = False
ENABLE_CHUNK_ENCODING = False
EMAIL_REPORTS_SUBJECT_PREFIX = "[乐学数据平台] "
