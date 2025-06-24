#!/bin/bash
# 智能能耗管理系统启动脚本

echo "============================================================"
echo "           智能能耗管理系统启动脚本"
echo "============================================================"
echo ""

# 检查Python版本
echo "检查Python环境..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✓ Python环境: $python_version"
else
    echo "✗ Python3未安装，请先安装Python 3.11或更高版本"
    exit 1
fi

# 检查依赖包
echo "检查依赖包..."
if python3 -c "import matplotlib" 2>/dev/null; then
    echo "✓ matplotlib已安装"
else
    echo "✗ matplotlib未安装，正在安装..."
    pip3 install matplotlib
fi

if python3 -c "import numpy" 2>/dev/null; then
    echo "✓ numpy已安装"
else
    echo "✗ numpy未安装，正在安装..."
    pip3 install numpy
fi

# 检查tkinter
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter已安装"
    GUI_AVAILABLE=true
else
    echo "⚠ tkinter未安装，将使用命令行界面"
    GUI_AVAILABLE=false
fi

echo ""
echo "============================================================"
echo "请选择启动方式:"
echo "1. 图形界面版本（推荐）"
echo "2. 命令行版本"
echo "3. 运行系统演示"
echo "4. 运行系统测试"
echo "5. 退出"
echo "============================================================"

read -p "请输入选择 (1-5): " choice

case $choice in
    1)
        if [ "$GUI_AVAILABLE" = true ]; then
            echo "启动图形界面版本..."
            cd src && python3 gui_main.py
        else
            echo "图形界面不可用，启动命令行版本..."
            cd src && python3 cli_main.py
        fi
        ;;
    2)
        echo "启动命令行版本..."
        cd src && python3 cli_main.py
        ;;
    3)
        echo "运行系统演示..."
        cd src && python3 demo.py
        ;;
    4)
        echo "运行系统测试..."
        cd src && python3 comprehensive_test.py
        ;;
    5)
        echo "退出启动脚本"
        exit 0
        ;;
    *)
        echo "无效选择，启动命令行版本..."
        cd src && python3 cli_main.py
        ;;
esac

