# 判断一个ip是否为ipv4

```python
from ipaddress import IPv4Address
from ipaddress import AddressValueError


def is_ipv4(address):
    try:
        IPv4Address(address)
        return True
    except AddressValueError:
        return False


print(is_ipv4("10.10.10.10"))  # True
```

# 判断一个ip是否为ipv6

```python
from ipaddress import IPv6Address
from ipaddress import AddressValueError


def is_ipv6(address):
    try:
        IPv6Address(address)
        return True
    except AddressValueError:
        return False


print(is_ipv6("ff06::c3"))  # True
```



