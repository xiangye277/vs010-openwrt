# VS010 刷机指南

## 方法一：Web API（已测试通过）

```bash
# 1. 登录获取 stok
PASSWD_B64=$(echo -n 'mzxgfwlpt00' | base64)
curl -s -D - -X POST http://192.168.2.1/api \
  -d "luci_username=user&luci_password=$PASSWD_B64"
# 从 Location 头提取 stok

# 2. 开启 Telnet（如果需要）
curl http://192.168.2.1/api/set/telnet

# 3. 上传固件
curl -F "size=文件大小" -F "file=@固件.img" \
  http://192.168.2.1/api/;stok=TOKEN/admin/advance/upgrade
```

## 方法二：U-Boot TTL（更安全，参考集客AP刷法）

```
硬件准备：
- USB-TTL 模块（3.3V）
- VS010 主板 UART 焊盘：GND, TX(gpio28), RX(gpio29)
- 波特率 115200

电脑准备：
- TFTP 服务器（如 tftpd64）
- 网线接路由器任意 LAN 口
- 电脑 IP 设为 10.1.1.2/24

U-Boot 命令：
setenv ipaddr 10.1.1.1          # 路由器 IP
setenv serverip 10.1.1.2         # TFTP 服务器 IP
tftpboot 0x44000000 firmware.img # 加载固件到内存
flash rootfs 0x44000000 0xSIZE   # 写入 rootfs 分区
reset                             # 重启
```

SIZE 从 tftpboot 返回值获取（如 0xde0000 = 14.5MB）。
