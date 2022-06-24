python时间相互转换
=================================

.. contents:: 目录

python时间戳、时间字符串、datetime类型相互转换


时间字符串转换为13位时间戳
--------------------

.. code-block:: python

     import typing as t
     import time
     import datetime


     def str_to_timestamp(str_time: str, time_format: str = "%Y-%m-%d %H:%M:%S") -> int:
        """
        时间字符串转换为13位时间戳
        :param str_time: 时间字符串
        :param time_format: 时间字符串格式 default： %Y-%m-%d %H:%M:%S
                example： %Y-%m-%d
        :return: 13位时间戳
        Usage::
          >>> str_to_timestamp("2022-10-10", "%Y-%m-%d")
          1665331200000
          >>> str_to_timestamp("2022-10-10 10:10:10")
          1665367810000
        """
        try:
            time_array = time.strptime(str_time, time_format)
            return int(time.mktime(time_array)) * 1000
        except ValueError:
            raise ValueError("Invalid time format!")
            
            
时间字符串转换为datetime
--------------------

.. code-block:: python

     import typing as t
     import time
     import datetime

     def str_to_datetime(str_time: str) -> datetime.datetime:
         """
         时间字符串转换为datetime
         :param str_time: 时间字符串 格式为"2022-10-10 10:10:10" 或 "2022-10-10"
         :return: datetime对象
         Usage::
           >>> str_to_datetime("2022-10-10 10:10:10")
           2022-10-10 10:10:10
           >>> str_to_datetime("2022-10-10")
           2022-10-10 00:00:00
         """
         try:
             if " " in str_time:
                 return datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
             else:
                 return datetime.datetime.strptime(str_time, "%Y-%m-%d")
         except ValueError:
             raise ValueError("Invalid time format!")

时间戳转换为时间字符串
--------------------

.. code-block:: python

     import typing as t
     import time
     import datetime

     def timestamp_to_str(timestamp: int, time_format: str = "%Y-%m-%d %H:%M:%S") -> str:
         """
         时间戳转换为时间字符串
         :param timestamp: 时间戳
         :param time_format: 时间字符串格式 default： %Y-%m-%d %H:%M:%S
         :return: 时间字符串
         Usage::
           >>> timestamp_to_str(1665331200000, "%Y-%m-%d")
           2022-10-10
           >>> timestamp_to_str(1665367810000)
           2022-10-10 10:10:10
         """
         try:
             datetime_type = datetime.datetime.fromtimestamp(timestamp // 1000)
             return datetime_type.strftime(time_format)
         except (TypeError, ValueError):
             raise ValueError("Invalid timestamp format!")
             
时间戳转换为datetime对象
--------------------

.. code-block:: python

     import typing as t
     import time
     import datetime

     def timestamp_to_datetime(timestamp: t.Union[int, float]) -> datetime.datetime:
         """
         时间戳转换为datetime对象
         :param timestamp: 时间戳
         :return: datetime对象
         Usage::
           >>> timestamp_to_datetime(1645513117000)
           2022-02-22 14:58:37
           >>> timestamp_to_datetime(1429417200.0)
           2015-04-19 12:20:00
         """
         try:
             # 13位时间戳 毫秒格式转换
             if len(str(int(timestamp))) == 13:
                 return datetime.datetime.fromtimestamp(timestamp // 1000)

             return datetime.datetime.fromtimestamp(timestamp)
         except ValueError:
             raise ValueError("Invalid time format!")
             
             
datetime对象转换为时间字符串
--------------------

.. code-block:: python

     import typing as t
     import time
     import datetime

     def datetime_to_str(datetime_obj: datetime.datetime) -> str:
         """
         datetime对象转换为时间字符串
         :param datetime_obj: datetime对象
         :return: 时间字符串
         Usage::
           >>> datetime_to_str(datetime.datetime.now()))
           2022-02-22 14:46:04
         """
         try:
             return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
         except AttributeError:
             raise ValueError("Invalid time format!")
             

datetime对象转换为13位时间戳
--------------------

.. code-block:: python

     import typing as t
     import time
     import datetime

     def datetime_to_timestamp(datetime_obj: datetime.datetime) -> int:
         """
         datetime对象转换为13位时间戳
         :param datetime_obj: datetime对象
         :return: 13位时间戳
         Usage::
           >>> datetime_to_timestamp(datetime.datetime.now()))
           1645513117000
         """
         try:
             return int(datetime_obj.timestamp()) * 1000
         except AttributeError:
             raise ValueError("Invalid time format!")
