# VS010 OpenWrt 固件编译

联通 VS010 (AX3000 WiFi 6) 路由器 OpenWrt 固件。

## 硬件规格

| 组件 | 型号 |
|------|------|
| SoC | Qualcomm IPQ5018 (IPQ5000) 双核 1GHz |
| RAM | 256MB DDR3L (集成在 SoC) |
| Flash | 128MB SPI NAND (F5D01G41LB) |
| 2.4G WiFi | IPQ5018 内置 (574Mbps) |
| 5G WiFi | QCN6102 2×2 (2402Mbps) |
| 交换机 | QCA8337-AL3C |
| 网口 | 1 WAN + 3 LAN (千兆) |

## 编译

使用 GitHub Actions 自动编译:

1. Fork 本仓库
2. 进入 Actions 页面
3. 手动触发 `Build VS010 OpenWrt` workflow
4. 等待 2-4 小时编译完成
5. 下载 artifact 得到固件

## 刷入方法

1. 登录 VS010 管理页面 (http://192.168.2.1)
2. 密码需要 base64 编码后提交到 `/api`
3. 获取 stok token
4. POST multipart 上传固件到 `/api/;stok=TOKEN/admin/advance/upgrade`
   - 字段: `file` (固件文件) + `size` (文件大小)
   - 文件格式: `.img`

## ⚠️ 警告

此固件基于 CMCC PZ-L8 设备树改编，GPIO 配置可能与实际 VS010 有差异。
首次刷入有砖风险，建议准备好 TTL 串口线用于救砖。

## 文件说明

- `vs010.dts` - 设备树源文件
- `.github/workflows/build.yml` - GitHub Actions 编译配置
