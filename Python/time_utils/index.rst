python时间相互转换
=================================

.. code-block:: python

    try:
        f = open('/path/to/file', 'r')
        print(f.read())
    finally:
        if f:
            f.close()

    with open('/path/to/file', 'r') as f:
        print(f.read())

    f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')


.. code-block:: python
     :linenos:
    
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



