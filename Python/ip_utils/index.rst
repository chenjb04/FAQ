python ip格式验证
=================================

.. contents:: 目录

python验证ip格式，包含ipv4，ipv6格式，ip范围，ip段等验证

.. note::
    需要引用以下包
    import IPy
    from ipaddress import IPv4Address
    from ipaddress import IPv4Network
    from ipaddress import IPv6Address
    from ipaddress import IPv6Network
    from ipaddress import AddressValueError
    from ipaddress import NetmaskValueError


验证是否为ipv4地址
--------------------

.. code-block:: python


     def is_ipv4(address: str) -> bool:
      """
      判断一个字符串是否为ipv4地址
      :param address: 待认证的字符串
      :return: True or False
      Usage::
        >>> is_ipv4("10.14.10.10")
        True
        >>> is_ipv4("100.200.600.50")
        False
      """
      try:
          IPv4Address(address)
          return True
      except AddressValueError:
          return False


验证是否为ipv6地址
--------------------

.. code-block:: python


    def is_ipv6(address: str) -> bool:
      """
      判断一个字符串是否为ipv6地址
      :param address: 待认证的字符串
      :return: True or False
      Usage::
        >>> is_ipv6("10.14.10.10")
        False
        >>> is_ipv6("0:0:0:0:0:ffff:192.1.56.10")
        True
        >>> is_ipv6("ff06::c3")
        True
      """
      try:
          IPv6Address(address)
          return True
      except AddressValueError:
          return False
          

验证是否为ipv4段
--------------------

.. code-block:: python

   def is_ipv4_cidr(address: str) -> bool:
      """
      判断是否为ipv4段
      :param address: 待验证的字符串
      :return: True or False
      Usage::
        >>> is_ipv4_cidr("192.0.2.0/24")
        True
        >>> is_ipv4_cidr("192.0.2.0/255.255.255.0")
        True
        >>> is_ipv4_cidr("192.0.2.1/50")
        False
      """
      if "/" not in address:
          return False

      try:
          IPv4Network(address, strict=False)
          return True
      except (AddressValueError, NetmaskValueError):
          return False
          
验证是否为ipv6段
--------------------
.. code-block:: python
    
    
    def is_ipv6_cidr(address: str) -> bool:
        """
        判断是否为ipv6段
        :param address: 待验证的字符串
        :return: True or False
        Usage::
          >>> is_ipv6_cidr("2001:db8::/128")
          True
          >>> is_ipv6_cidr("2001:db8:0000:0000:0000:0000:0000:0000/128")
          True
          >>> is_ipv6_cidr("2001:db8::/256")
          False
        """
        if "/" not in address:
            return False

        try:
            IPv6Network(address, strict=False)
            return True
        except (AddressValueError, NetmaskValueError):
            return False


验证是否为ipv4范围
--------------------

.. note::
    
    此处需要引用is_ipv4函数

.. code-block:: python
    
    
    def is_ipv4_range(address: str) -> bool:
        """
        验证字符串是否为ipv4范围
        :param address: 待验证的字符串 格式为：10.10.10.10-10
        :return:
        Usage::
          >>> is_ipv4_range("10.10.10.10-60")
          True
          >>> is_ipv4_range("10.10.10.10-5")
          False
        """
        # 分割
        split_list = address.split('-')
        if len(split_list) != 2:
            return False

        # 判断第一部分是否为ip地址
        if not is_ipv4(split_list[0]):
            return False

        # 判断第二部分数字的范围是否在ip地址尾部数字到255之间
        try:
            number = int(split_list[1])
        except ValueError:
            return False

        return int(split_list[0].rsplit('.', 1)[-1]) < number <= 255


验证是否为ipv6范围
--------------------

.. note::
    
    此处需要引用is_ipv6函数

.. code-block:: python
    
    
    def is_ipv6_range(address: str) -> bool:
        """
        验证字符串是否为ipv6范围
        :param address: 待验证的字符串 格式为：2001:db8::-ffff
        :return:
        Usage::
          >>> is_ipv6_range("2001:db8:0000:0000:0000:0000:0000:0000-ffff")
          True
          >>> is_ipv6_range("2001:db8::-ffff")
          True
          >>> is_ipv4_range("2001:db8::ffff-ffff")
          False
        """
        # 分割
        split_list = address.split('-')
        if len(split_list) != 2:
            return False

        # 判断第一部分是否为ip地址
        if not is_ipv6(split_list[0]):
            return False

        # 判断第二部分数字的范围是否在ip地址尾部数字到65535之间
        try:
            number = int(split_list[1], 16)
        except ValueError:
            return False

        # 对于缩写的ipv6地址做转换 获取IP地址的longhand版本 2001:db8:: -> 2001:db8:0000:...:0000
        ipv6 = IPv6Address(split_list[0])
        return int(ipv6.exploded.rsplit(':', 1)[-1], 16) < number <= 65535


验证ip是否属于一个网段
--------------------
.. code-block:: python

    def ip_in_cidr(address: str, cidr: str) -> bool:
        """
        判断ip是否属于一个网段
        :param address: 待验证的ip地址
        :param cidr: 网断地址
        :return: True or False
        Example::
            a.b.c.0/24               2001:658:22a:cafe::/64
            a.b.c.0-a.b.c.255        2001:658:22a:cafe::-2001:658:22a:cafe:ffff:ffff:ffff:ffff
            a.b.c.d/255.255.255.0    not supported for IPv6
        Usage::
          >>> ip_in_cidr("10.10.10.10", "10.10.10.0/24")
          True
          >>> ip_in_cidr("192.168.1.0/24", "192.168.0.0/16")
          True
          >>> ip_in_cidr("192.168.1.0", "255.255.255.0")
          False
          >>> ip_in_cidr("::0", "::0/127")
          True
        """
        try:
            return address in IPy.IP(cidr)
        except ValueError:
            return False



验证ip是否为本地回环地址
--------------------
.. code-block:: python

    def is_loopback(address: str) -> bool:
        """
        判断ip是否为本地回环地址  在 127.0.0.0/8和::1属于本地回环地址
        :param address: 待验证的地址 ipv4 or ipv6
        :return: True or False
        Usages:
          >>> is_loopback("10.10.10.10")
          False
          >>> is_loopback("127.0.0.1")
          True
          >>> is_loopback("::1")
          True
        """
        # 判断ipv4
        if is_ipv4(address) and IPv4Address(address).is_loopback:
            return True

        # 判断ipv6
        if is_ipv6(address) and IPv6Address(address).is_loopback:
            return True

        return False
