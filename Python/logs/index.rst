python logging模块使用
=================================

.. contents:: 目录

python logging模块二次封装 支持按日期分割日志、按天分割日志,支持多进程安全

.. code-block:: python
    import logging
    import os
    import sys
    import typing as t
    from logging.handlers import RotatingFileHandler
    from logging.handlers import TimedRotatingFileHandler

    # Windows系统使用concurrent_log_handler pip install concurrent_log_handler
    # linux 系统使用 cloghandler pip install ConcurrentLogHandler
    if sys.platform.startswith('win'):
        from concurrent_log_handler import ConcurrentRotatingFileHandler
    else:
        from cloghandler import ConcurrentRotatingFileHandler


    class Log:
        """
        logging 二次封装 支持按日期分割日志、按天分割日志,支持多进程安全
        log 四个核心处理器
            logger 记录器 用来交互使用
            handler 处理器 主要使用
            formatter 格式器 用来格式化日志输出格式
            filter 过滤器 用来过滤日志
        """
        # 滚动方式
        ROTATING_MODE = ['file_mode', "time_mode"]
        # 日志等级
        LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        def __init__(self, filename: str, log_dir: str, level: str,
                     rotate_mode: str, max_bytes: int = 100 * 1024 * 1024,
                     backup_count: int = 10, log_name: str = None,
                     is_multi_process: bool = False,
                     is_output_console: bool = True):
            """
            :param filename: 文件名称
            :param log_dir: 日志目录
            :param level: 日志级别
            :param rotate_mode: 滚动方式 按大小或者按时间
            :param max_bytes: 日志最大大小 默认100M
            :param backup_count: 备份文件数量 默认10
            :param log_name: 日志名称 默认使用None
            :param is_multi_process: 是否多进程
            :param is_output_console: 日志是否打印到终端
            """
            self.filename = filename
            self.log_dir = log_dir
            self.level = level.upper()
            self.rotate_mode = rotate_mode
            self.max_bytes = max_bytes
            self.backup_count = backup_count
            self.log_name = log_name
            self.is_multi_process = is_multi_process
            self.is_output_console = is_output_console
            self.__logger = logging.getLogger(self.log_name)
            # 判断日志是否存在 不存在创建
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir, exist_ok=True)

            # 处理一下日志文件名
            self.handle_log_filename()

        def handle_log_filename(self) -> t.NoReturn:
            """
            处理日志名称
            :return: no return
            """
            # 日志文件名处理成.log结尾
            if not self.filename.endswith(".log"):
                self.filename = '{}.log'.format(self.filename)

            self.filename = os.path.join(self.log_dir, self.filename)

        def __init_handler(self) -> t.Tuple[t.Union[
                                                TimedRotatingFileHandler,
                                                ConcurrentRotatingFileHandler,
                                                RotatingFileHandler],
                                            logging.StreamHandler]:
            """
            初始化handler
            :return: 返回handler对象元组
            """
            # 默认使用RotatingFileHandler 按照文件大小滚动
            handler_class = RotatingFileHandler

            # 如果是多进程 使用ConcurrentRotatingFileHandler处理
            if self.is_multi_process:
                handler_class = ConcurrentRotatingFileHandler

            handler = handler_class(
                filename=self.filename,
                mode='a',
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )

            if self.rotate_mode == self.ROTATING_MODE[1]:
                handler = TimedRotatingFileHandler(
                    filename=self.filename,
                    when='D',
                    interval=1,
                    backupCount=180,
                    encoding='utf-8'
                )

            if self.is_output_console:
                console_handler = logging.StreamHandler()
                return handler, console_handler

            return (handler,)

        def __set_handler(self, handler):
            """
            设置handler
            :return:
            """
            # handler.setLevel(self.level)
            self.__logger.addHandler(handler)
            self.__logger.setLevel(self.level)

        def __set_formatter(self, handler):
            """
            设置日志输出格式
            :return:
            """
            fmt = "[%(asctime)s-%(pathname)s-[line:%(lineno)d]-%(levelname)s-[日志信息->>>]: %(message)s]"
            if self.is_multi_process:
                fmt = "[%(asctime)s-%(pathname)s-(进程: %(process)d)-[line:%(lineno)d]-%(levelname)s-[日志信息]: %(" \
                      "message)s] "
            formatter = logging.Formatter(fmt)
            handler.setFormatter(formatter)

        def logger(self):
            """
            构建日志收集器
            :return:
            """
            handlers = self.__init_handler()
            for handler in handlers:
                self.__set_formatter(handler)
                self.__set_handler(handler)

            return self.__logger

        def __setattr__(self, key, value):
            if key == 'rotate_mode':
                if value not in self.ROTATING_MODE:
                    raise ValueError("Rotate mode must be one of 'file_mode', "
                                     "'time_mode'")
            if key == 'level':
                if value not in self.LEVELS:
                    raise ValueError("Level  must be one of {}".format(self.LEVELS))

            object.__setattr__(self, key, value)


    log = Log(filename="1.log",
              log_dir="./",
              level="INFO",
              rotate_mode="file_mode"
              )
    logger = log.logger()
