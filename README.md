# 智能能耗管理系统

一个基于Python开发的智能能源监控与管理系统，提供全面的用电设备监控、数据分析和能耗优化功能。

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ 特性

- 🖥️ **双界面支持**: GUI图形界面 + CLI命令行界面
- 📊 **实时监控**: 设备状态、功率消耗、能耗趋势实时显示
- 📈 **数据分析**: 历史数据统计、峰谷用电分析、成本计算
- 🔧 **设备管理**: 设备添加、删除、修改、状态控制
- 💾 **数据持久化**: 自动保存用户数据和系统配置
- 📱 **响应式设计**: 支持不同分辨率和操作系统
- 🚀 **高性能**: 优化的算法确保系统稳定高效运行

## 🚀 快速开始

### 安装要求

- Python 3.11 或更高版本
- tkinter (GUI界面需要)
- 至少 100MB 可用磁盘空间

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/Proton1917/intelligent-energy-management-system.git
   cd intelligent-energy-management-system
   ```

2. **运行应用**
   ```bash
   # 图形界面版本（推荐）
   python3 gui_main.py
   
   # 命令行版本
   python3 cli_main.py
   
   # 或使用启动脚本
   chmod +x start.sh
   ./start.sh
   ```

## 📖 使用说明

### GUI界面版本

启动图形界面后，你可以：

- **设备管理**: 在左侧面板添加、编辑和删除设备
- **实时监控**: 查看当前所有设备的状态和功耗
- **数据分析**: 查看历史用电数据和趋势图表
- **系统设置**: 配置用电价格、报警阈值等参数

### CLI命令行版本

命令行界面提供完整的功能访问：

```bash
# 查看所有设备
设备管理 -> 查看设备列表

# 添加新设备
设备管理 -> 添加设备

# 查看统计信息
数据分析 -> 查看统计信息
```

## 📁 项目结构

```
intelligent-energy-management-system/
├── energy_management_system.py    # 核心业务逻辑
├── gui_main.py                    # GUI主程序
├── cli_main.py                    # CLI主程序
├── demo.py                        # 演示程序
├── comprehensive_test.py          # 综合测试
├── start.sh                       # 启动脚本
├── .gitignore                     # Git忽略文件
├── README.md                      # 项目说明
├── 智能能耗管理系统使用说明.md      # 详细使用说明
└── 智能能耗管理系统项目总结报告.md   # 项目总结报告
```

## 🔧 核心功能

### 设备管理
- 支持多种设备类型（照明、空调、计算机等）
- 设备状态控制（开启/关闭）
- 功率和位置信息管理

### 数据监控
- 实时功耗监控
- 历史数据记录
- 用电趋势分析

### 成本计算
- 基于实际用电量的成本计算
- 峰谷电价支持
- 月度/年度成本统计

### 系统优化
- 智能节能建议
- 设备使用效率分析
- 能耗报警功能

## 🧪 测试

运行综合测试：

```bash
python3 comprehensive_test.py
```

运行演示程序：

```bash
python3 demo.py
```

## 📚 文档

- [详细使用说明](智能能耗管理系统使用说明.md)
- [项目总结报告](智能能耗管理系统项目总结报告.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 这个项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **Proton1917** - *初始工作* - [Proton1917](https://github.com/Proton1917)

## 🙏 致谢

感谢所有为这个项目做出贡献的人们！

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
