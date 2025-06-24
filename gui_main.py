#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能能耗管理系统图形界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
from energy_management_system import EnergyManagementSystem

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class EnergyManagementGUI:
    """智能能耗管理系统图形界面"""
    
    def __init__(self):
        self.ems = EnergyManagementSystem()
        self.root = tk.Tk()
        self.root.title("智能能耗管理系统")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # 创建样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主菜单
        self.create_menu()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题
        title_label = ttk.Label(main_frame, text="智能能耗管理系统", 
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 创建功能按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 功能按钮
        buttons = [
            ("设备管理", self.open_device_management),
            ("用电监控", self.open_energy_monitoring),
            ("能耗分析", self.open_energy_analysis),
            ("节能建议", self.open_energy_recommendations),
            ("成本计算", self.open_cost_calculation),
            ("报表生成", self.open_report_generation)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, width=15)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='ew')
        
        # 配置列权重
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        
        # 创建状态显示区域
        self.create_status_area(main_frame)
        
        # 创建数据显示区域
        self.create_data_area(main_frame)
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导入数据", command=self.import_data)
        file_menu.add_command(label="导出数据", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="系统设置", command=self.open_settings)
        tools_menu.add_command(label="数据备份", command=self.backup_data)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_status_area(self, parent):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="系统状态", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 状态信息
        info_frame = ttk.Frame(status_frame)
        info_frame.pack(fill=tk.X)
        
        # 设备数量
        devices_count = len(self.ems.get_all_devices())
        ttk.Label(info_frame, text=f"设备总数: {devices_count}").grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        # 活跃告警
        alerts_count = len(self.ems.get_all_alerts('active'))
        ttk.Label(info_frame, text=f"活跃告警: {alerts_count}").grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        # 待处理建议
        recs_count = len(self.ems.get_all_recommendations('pending'))
        ttk.Label(info_frame, text=f"待处理建议: {recs_count}").grid(row=0, column=2, sticky='w', padx=(0, 20))
        
        # 当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ttk.Label(info_frame, text=f"当前时间: {current_time}").grid(row=0, column=3, sticky='w')
    
    def create_data_area(self, parent):
        """创建数据显示区域"""
        data_frame = ttk.LabelFrame(parent, text="数据概览", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Notebook用于多标签页
        notebook = ttk.Notebook(data_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 设备列表标签页
        self.create_devices_tab(notebook)
        
        # 告警列表标签页
        self.create_alerts_tab(notebook)
        
        # 图表显示标签页
        self.create_charts_tab(notebook)
    
    def create_devices_tab(self, notebook):
        """创建设备列表标签页"""
        devices_frame = ttk.Frame(notebook)
        notebook.add(devices_frame, text="设备列表")
        
        # 创建Treeview
        columns = ('ID', '名称', '类型', '位置', '额定功率', '状态')
        self.devices_tree = ttk.Treeview(devices_frame, columns=columns, show='headings', height=10)
        
        # 设置列标题
        for col in columns:
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(devices_frame, orient=tk.VERTICAL, command=self.devices_tree.yview)
        self.devices_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.devices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 加载设备数据
        self.refresh_devices_list()
    
    def create_alerts_tab(self, notebook):
        """创建告警列表标签页"""
        alerts_frame = ttk.Frame(notebook)
        notebook.add(alerts_frame, text="告警信息")
        
        # 创建Treeview
        columns = ('ID', '设备ID', '类型', '严重程度', '消息', '时间')
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=columns, show='headings', height=10)
        
        # 设置列标题
        for col in columns:
            self.alerts_tree.heading(col, text=col)
            self.alerts_tree.column(col, width=120)
        
        # 添加滚动条
        scrollbar2 = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, command=self.alerts_tree.yview)
        self.alerts_tree.configure(yscrollcommand=scrollbar2.set)
        
        # 布局
        self.alerts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 加载告警数据
        self.refresh_alerts_list()
    
    def create_charts_tab(self, notebook):
        """创建图表显示标签页"""
        charts_frame = ttk.Frame(notebook)
        notebook.add(charts_frame, text="数据图表")
        
        # 创建matplotlib图表
        fig = Figure(figsize=(10, 6), dpi=100)
        
        # 示例图表：设备能耗对比
        ax = fig.add_subplot(111)
        devices = self.ems.get_all_devices()
        if devices:
            device_names = [d['name'][:8] for d in devices[:5]]  # 取前5个设备，名称截断
            # 模拟能耗数据
            energy_data = [np.random.uniform(10, 100) for _ in device_names]
            
            bars = ax.bar(device_names, energy_data, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
            ax.set_title('设备能耗对比图', fontsize=14, fontweight='bold')
            ax.set_ylabel('能耗 (kWh)')
            ax.set_xlabel('设备名称')
            
            # 添加数值标签
            for bar, value in zip(bars, energy_data):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       f'{value:.1f}', ha='center', va='bottom')
        
        # 将图表嵌入到Tkinter
        canvas = FigureCanvasTkAgg(fig, charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def refresh_devices_list(self):
        """刷新设备列表"""
        # 清空现有数据
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        # 加载设备数据
        devices = self.ems.get_all_devices()
        for device in devices:
            self.devices_tree.insert('', tk.END, values=(
                device['id'],
                device['name'],
                device['type'],
                device['location'],
                f"{device['rated_power']}W",
                device['status']
            ))
    
    def refresh_alerts_list(self):
        """刷新告警列表"""
        # 清空现有数据
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        
        # 加载告警数据
        alerts = self.ems.get_all_alerts()
        for alert in alerts:
            self.alerts_tree.insert('', tk.END, values=(
                alert['id'],
                alert['device_id'],
                alert['type'],
                alert['severity'],
                alert['message'][:30] + '...' if len(alert['message']) > 30 else alert['message'],
                alert['timestamp']
            ))
    
    # ==================== 功能窗口 ====================
    
    def open_device_management(self):
        """打开设备管理窗口"""
        DeviceManagementWindow(self.root, self.ems, self.refresh_devices_list)
    
    def open_energy_monitoring(self):
        """打开用电监控窗口"""
        EnergyMonitoringWindow(self.root, self.ems)
    
    def open_energy_analysis(self):
        """打开能耗分析窗口"""
        EnergyAnalysisWindow(self.root, self.ems)
    
    def open_energy_recommendations(self):
        """打开节能建议窗口"""
        EnergyRecommendationsWindow(self.root, self.ems)
    
    def open_cost_calculation(self):
        """打开成本计算窗口"""
        CostCalculationWindow(self.root, self.ems)
    
    def open_report_generation(self):
        """打开报表生成窗口"""
        ReportGenerationWindow(self.root, self.ems)
    
    # ==================== 菜单功能 ====================
    
    def import_data(self):
        """导入数据"""
        filename = filedialog.askopenfilename(
            title="选择数据文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            messagebox.showinfo("提示", f"数据导入功能开发中\n选择的文件: {filename}")
    
    def export_data(self):
        """导出数据"""
        filename = filedialog.asksaveasfilename(
            title="保存数据文件",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            messagebox.showinfo("提示", f"数据导出功能开发中\n保存位置: {filename}")
    
    def open_settings(self):
        """打开系统设置"""
        messagebox.showinfo("系统设置", "系统设置功能开发中")
    
    def backup_data(self):
        """备份数据"""
        messagebox.showinfo("数据备份", "数据备份功能开发中")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
智能能耗管理系统使用说明

1. 设备管理：注册、查看和管理用电设备
2. 用电监控：实时监控设备用电情况
3. 能耗分析：分析设备能耗趋势和效率
4. 节能建议：获取智能节能建议
5. 成本计算：计算电费成本和预算分析
6. 报表生成：生成各类能耗报表

更多详细信息请参考用户手册。
        """
        messagebox.showinfo("使用说明", help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
智能能耗管理系统 v1.0

开发者：AI助手
技术栈：Python + Tkinter + Matplotlib
功能：用电监控、能耗分析、节能建议、成本计算、设备管理、报表生成

© 2024 智能能耗管理系统
        """
        messagebox.showinfo("关于", about_text)
    
    def run(self):
        """运行主程序"""
        self.root.mainloop()


# ==================== 子窗口类 ====================

class DeviceManagementWindow:
    """设备管理窗口"""
    
    def __init__(self, parent, ems, refresh_callback=None):
        self.ems = ems
        self.refresh_callback = refresh_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("设备管理")
        self.window.geometry("600x400")
        self.window.grab_set()  # 模态窗口
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(main_frame, text="设备管理", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 添加设备框架
        add_frame = ttk.LabelFrame(main_frame, text="添加新设备", padding=10)
        add_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 输入字段
        fields = [
            ("设备名称:", "name"),
            ("设备类型:", "type"),
            ("安装位置:", "location"),
            ("额定功率(W):", "power"),
            ("能效等级:", "efficiency"),
            ("制造商:", "manufacturer"),
            ("型号:", "model")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(add_frame, text=label).grid(row=i//2, column=(i%2)*2, sticky='w', padx=(0, 5), pady=2)
            entry = ttk.Entry(add_frame, width=20)
            entry.grid(row=i//2, column=(i%2)*2+1, sticky='ew', padx=(0, 20), pady=2)
            self.entries[key] = entry
        
        # 设置默认值
        self.entries['type'].insert(0, 'HVAC')
        self.entries['efficiency'].insert(0, 'A')
        self.entries['manufacturer'].insert(0, '通用')
        self.entries['model'].insert(0, '标准型')
        
        # 添加按钮
        ttk.Button(add_frame, text="添加设备", command=self.add_device).grid(row=4, column=0, columnspan=4, pady=10)
        
        # 配置列权重
        for i in range(4):
            add_frame.columnconfigure(i, weight=1)
        
        # 设备列表框架
        list_frame = ttk.LabelFrame(main_frame, text="设备列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 设备列表
        columns = ('ID', '名称', '类型', '位置', '功率', '状态')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="删除设备", command=self.delete_device).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="设备详情", command=self.show_device_details).pack(side=tk.LEFT)
        
        # 加载设备列表
        self.refresh_list()
    
    def add_device(self):
        """添加设备"""
        try:
            # 获取输入值
            name = self.entries['name'].get().strip()
            device_type = self.entries['type'].get().strip()
            location = self.entries['location'].get().strip()
            power = self.entries['power'].get().strip()
            efficiency = self.entries['efficiency'].get().strip()
            manufacturer = self.entries['manufacturer'].get().strip()
            model = self.entries['model'].get().strip()
            
            # 验证输入
            if not all([name, device_type, location, power]):
                messagebox.showerror("错误", "请填写所有必填字段")
                return
            
            try:
                power = float(power)
            except ValueError:
                messagebox.showerror("错误", "额定功率必须是数字")
                return
            
            # 添加设备
            device_id, msg = self.ems.register_device(
                name, device_type, location, power, efficiency, manufacturer, model
            )
            
            if device_id:
                messagebox.showinfo("成功", msg)
                # 清空输入框
                for entry in self.entries.values():
                    if entry != self.entries['type'] and entry != self.entries['efficiency'] and \
                       entry != self.entries['manufacturer'] and entry != self.entries['model']:
                        entry.delete(0, tk.END)
                
                # 刷新列表
                self.refresh_list()
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                messagebox.showerror("错误", msg)
                
        except Exception as e:
            messagebox.showerror("错误", f"添加设备失败: {e}")
    
    def refresh_list(self):
        """刷新设备列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 加载设备数据
        devices = self.ems.get_all_devices()
        for device in devices:
            self.tree.insert('', tk.END, values=(
                device['id'],
                device['name'],
                device['type'],
                device['location'],
                f"{device['rated_power']}W",
                device['status']
            ))
    
    def delete_device(self):
        """删除设备"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的设备")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的设备吗？"):
            messagebox.showinfo("提示", "删除功能开发中")
    
    def show_device_details(self):
        """显示设备详情"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要查看的设备")
            return
        
        item = self.tree.item(selection[0])
        device_id = item['values'][0]
        
        device = self.ems.find_device_by_id(device_id)
        if device:
            details = f"""
设备详情

ID: {device['id']}
名称: {device['name']}
类型: {device['type']}
位置: {device['location']}
额定功率: {device['rated_power']}W
能效等级: {device['energy_efficiency']}
制造商: {device['manufacturer']}
型号: {device['model']}
安装日期: {device['installation_date']}
最后维护: {device['last_maintenance']}
状态: {device['status']}
            """
            messagebox.showinfo("设备详情", details)


class EnergyMonitoringWindow:
    """用电监控窗口"""
    
    def __init__(self, parent, ems):
        self.ems = ems
        
        self.window = tk.Toplevel(parent)
        self.window.title("用电监控")
        self.window.geometry("800x600")
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="用电监控", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 设备选择
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(select_frame, text="选择设备:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(select_frame, textvariable=self.device_var, width=30)
        self.device_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 加载设备列表
        devices = self.ems.get_all_devices()
        device_list = [f"{d['id']} - {d['name']}" for d in devices]
        self.device_combo['values'] = device_list
        if device_list:
            self.device_combo.set(device_list[0])
        
        ttk.Button(select_frame, text="开始监控", command=self.start_monitoring).pack(side=tk.LEFT)
        
        # 数据输入框架
        input_frame = ttk.LabelFrame(main_frame, text="手动记录用电数据", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 输入字段
        input_fields = [
            ("电压(V):", "voltage", "220"),
            ("电流(A):", "current", "10"),
            ("功率(W):", "power", "2200"),
            ("温度(°C):", "temperature", "25"),
            ("湿度(%):", "humidity", "60")
        ]
        
        self.input_entries = {}
        for i, (label, key, default) in enumerate(input_fields):
            ttk.Label(input_frame, text=label).grid(row=i//3, column=(i%3)*2, sticky='w', padx=(0, 5), pady=5)
            entry = ttk.Entry(input_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i//3, column=(i%3)*2+1, sticky='ew', padx=(0, 20), pady=5)
            self.input_entries[key] = entry
        
        ttk.Button(input_frame, text="记录数据", command=self.record_data).grid(row=2, column=0, columnspan=6, pady=10)
        
        # 配置列权重
        for i in range(6):
            input_frame.columnconfigure(i, weight=1)
        
        # 数据显示区域
        display_frame = ttk.LabelFrame(main_frame, text="实时数据", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建数据表格
        columns = ('时间', '电压', '电流', '功率', '能耗', '温度')
        self.data_tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        self.data_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 刷新数据
        self.refresh_data()
    
    def start_monitoring(self):
        """开始监控"""
        if not self.device_var.get():
            messagebox.showwarning("警告", "请选择设备")
            return
        
        messagebox.showinfo("提示", "实时监控功能开发中\n当前显示历史数据")
        self.refresh_data()
    
    def record_data(self):
        """记录用电数据"""
        try:
            if not self.device_var.get():
                messagebox.showwarning("警告", "请选择设备")
                return
            
            device_id = self.device_var.get().split(' - ')[0]
            
            # 获取输入值
            voltage = float(self.input_entries['voltage'].get())
            current = float(self.input_entries['current'].get())
            power = float(self.input_entries['power'].get())
            temperature = float(self.input_entries['temperature'].get())
            humidity = float(self.input_entries['humidity'].get())
            
            # 记录数据
            success, msg = self.ems.record_energy_reading(
                device_id, voltage, current, power, temperature, humidity
            )
            
            if success:
                messagebox.showinfo("成功", msg)
                self.refresh_data()
            else:
                messagebox.showerror("错误", msg)
                
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
        except Exception as e:
            messagebox.showerror("错误", f"记录数据失败: {e}")
    
    def refresh_data(self):
        """刷新数据显示"""
        # 清空现有数据
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        if not self.device_var.get():
            return
        
        device_id = self.device_var.get().split(' - ')[0]
        
        # 获取最近的用电数据
        readings = self.ems.get_device_readings(device_id, hours=24)
        
        for reading in readings[-20:]:  # 显示最近20条记录
            self.data_tree.insert('', tk.END, values=(
                reading['timestamp'],
                f"{reading['voltage']:.1f}V",
                f"{reading['current']:.2f}A",
                f"{reading['power']:.0f}W",
                f"{reading['energy_consumed']:.3f}kWh",
                f"{reading['temperature']:.1f}°C"
            ))


class EnergyAnalysisWindow:
    """能耗分析窗口"""
    
    def __init__(self, parent, ems):
        self.ems = ems
        
        self.window = tk.Toplevel(parent)
        self.window.title("能耗分析")
        self.window.geometry("900x700")
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="能耗分析", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 分析参数框架
        param_frame = ttk.Frame(main_frame)
        param_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(param_frame, text="选择设备:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(param_frame, textvariable=self.device_var, width=30)
        self.device_combo.grid(row=0, column=1, padx=(0, 20))
        
        # 加载设备列表
        devices = self.ems.get_all_devices()
        device_list = [f"{d['id']} - {d['name']}" for d in devices]
        self.device_combo['values'] = device_list
        if device_list:
            self.device_combo.set(device_list[0])
        
        ttk.Label(param_frame, text="分析天数:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.days_var = tk.StringVar(value="7")
        days_combo = ttk.Combobox(param_frame, textvariable=self.days_var, width=10)
        days_combo['values'] = ['1', '7', '14', '30']
        days_combo.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Button(param_frame, text="开始分析", command=self.start_analysis).grid(row=0, column=4)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="分析结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Notebook
        notebook = ttk.Notebook(result_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 基础分析标签页
        self.create_basic_analysis_tab(notebook)
        
        # 峰谷分析标签页
        self.create_peak_valley_tab(notebook)
        
        # 预测分析标签页
        self.create_prediction_tab(notebook)
    
    def create_basic_analysis_tab(self, notebook):
        """创建基础分析标签页"""
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="基础分析")
        
        self.basic_text = tk.Text(basic_frame, height=15, width=60)
        scrollbar = ttk.Scrollbar(basic_frame, orient=tk.VERTICAL, command=self.basic_text.yview)
        self.basic_text.configure(yscrollcommand=scrollbar.set)
        
        self.basic_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_peak_valley_tab(self, notebook):
        """创建峰谷分析标签页"""
        pv_frame = ttk.Frame(notebook)
        notebook.add(pv_frame, text="峰谷分析")
        
        self.pv_text = tk.Text(pv_frame, height=15, width=60)
        scrollbar2 = ttk.Scrollbar(pv_frame, orient=tk.VERTICAL, command=self.pv_text.yview)
        self.pv_text.configure(yscrollcommand=scrollbar2.set)
        
        self.pv_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_prediction_tab(self, notebook):
        """创建预测分析标签页"""
        pred_frame = ttk.Frame(notebook)
        notebook.add(pred_frame, text="预测分析")
        
        self.pred_text = tk.Text(pred_frame, height=15, width=60)
        scrollbar3 = ttk.Scrollbar(pred_frame, orient=tk.VERTICAL, command=self.pred_text.yview)
        self.pred_text.configure(yscrollcommand=scrollbar3.set)
        
        self.pred_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_analysis(self):
        """开始分析"""
        if not self.device_var.get():
            messagebox.showwarning("警告", "请选择设备")
            return
        
        try:
            device_id = self.device_var.get().split(' - ')[0]
            days = int(self.days_var.get())
            
            # 基础分析
            analysis, msg = self.ems.analyze_energy_consumption(device_id, days)
            self.display_basic_analysis(analysis, msg)
            
            # 峰谷分析
            pv_analysis, pv_msg = self.ems.analyze_peak_valley_consumption(device_id, days)
            self.display_peak_valley_analysis(pv_analysis, pv_msg)
            
            # 预测分析
            prediction, pred_msg = self.ems.predict_energy_consumption(device_id, 24)
            self.display_prediction_analysis(prediction, pred_msg)
            
        except Exception as e:
            messagebox.showerror("错误", f"分析失败: {e}")
    
    def display_basic_analysis(self, analysis, msg):
        """显示基础分析结果"""
        self.basic_text.delete(1.0, tk.END)
        
        if analysis:
            result = f"""
基础能耗分析结果

设备ID: {analysis['device_id']}
设备名称: {analysis['device_name']}
分析周期: {analysis['period_days']} 天
分析日期: {analysis['analysis_date']}

=== 能耗统计 ===
总能耗: {analysis['total_energy_kwh']} kWh
平均功率: {analysis['average_power_w']} W
峰值功率: {analysis['peak_power_w']} W
最低功率: {analysis['min_power_w']} W
数据点数: {analysis['readings_count']} 个

=== 效率分析 ===
运行效率: {analysis['efficiency_percentage']}%

=== 评估结果 ===
"""
            if analysis['efficiency_percentage'] >= 90:
                result += "✓ 设备运行效率优秀\n"
            elif analysis['efficiency_percentage'] >= 80:
                result += "○ 设备运行效率良好\n"
            elif analysis['efficiency_percentage'] >= 70:
                result += "△ 设备运行效率一般，建议优化\n"
            else:
                result += "✗ 设备运行效率较低，需要检查\n"
            
            self.basic_text.insert(tk.END, result)
        else:
            self.basic_text.insert(tk.END, f"分析失败: {msg}")
    
    def display_peak_valley_analysis(self, analysis, msg):
        """显示峰谷分析结果"""
        self.pv_text.delete(1.0, tk.END)
        
        if analysis:
            result = f"""
峰谷用电分析结果

设备ID: {analysis['device_id']}
分析周期: {analysis['period_days']} 天
分析日期: {analysis['analysis_date']}

=== 峰谷用电统计 ===
峰时用电 (8:00-22:00): {analysis['peak_consumption_kwh']} kWh ({analysis['peak_ratio_percent']}%)
谷时用电 (22:00-8:00): {analysis['valley_consumption_kwh']} kWh ({analysis['valley_ratio_percent']}%)
总用电量: {analysis['total_consumption_kwh']} kWh

=== 用电模式分析 ===
"""
            if analysis['peak_ratio_percent'] > 80:
                result += "主要在峰时用电，建议优化用电时间安排\n"
            elif analysis['peak_ratio_percent'] > 60:
                result += "峰时用电较多，可考虑部分负载转移到谷时\n"
            else:
                result += "用电时间分布较为合理\n"
            
            result += f"""
=== 节能建议 ===
• 尽量将非紧急用电安排在谷时 (22:00-8:00)
• 峰时电价较高，合理安排用电可节省成本
• 当前峰谷比例: {analysis['peak_ratio_percent']:.1f}% : {analysis['valley_ratio_percent']:.1f}%
            """
            
            self.pv_text.insert(tk.END, result)
        else:
            self.pv_text.insert(tk.END, f"峰谷分析失败: {msg}")
    
    def display_prediction_analysis(self, prediction, msg):
        """显示预测分析结果"""
        self.pred_text.delete(1.0, tk.END)
        
        if prediction:
            result = f"""
能耗预测分析结果

设备ID: {prediction['device_id']}
预测时长: {prediction['prediction_hours']} 小时
预测日期: {prediction['prediction_date']}
预测置信度: {prediction['confidence']*100:.1f}%

=== 预测结果 ===
预测能耗: {prediction['predicted_energy_kwh']} kWh
基准功率: {prediction['base_power_w']} W

=== 预测说明 ===
• 基于最近的用电数据进行预测
• 考虑了工作时间和非工作时间的用电模式
• 预测结果仅供参考，实际用电可能受多种因素影响

=== 成本预估 ===
"""
            # 简单成本预估
            peak_rate = 0.85  # 峰时电价
            valley_rate = 0.45  # 谷时电价
            avg_rate = (peak_rate + valley_rate) / 2
            estimated_cost = prediction['predicted_energy_kwh'] * avg_rate
            
            result += f"预估电费: {estimated_cost:.2f} 元 (按平均电价 {avg_rate} 元/kWh 计算)\n"
            
            self.pred_text.insert(tk.END, result)
        else:
            self.pred_text.insert(tk.END, f"预测分析失败: {msg}")


class EnergyRecommendationsWindow:
    """节能建议窗口"""
    
    def __init__(self, parent, ems):
        self.ems = ems
        
        self.window = tk.Toplevel(parent)
        self.window.title("节能建议")
        self.window.geometry("800x600")
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="节能建议", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 设备选择框架
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(select_frame, text="选择设备:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(select_frame, textvariable=self.device_var, width=30)
        self.device_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 加载设备列表
        devices = self.ems.get_all_devices()
        device_list = [f"{d['id']} - {d['name']}" for d in devices]
        self.device_combo['values'] = device_list
        if device_list:
            self.device_combo.set(device_list[0])
        
        ttk.Button(select_frame, text="生成建议", command=self.generate_recommendations).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(select_frame, text="刷新列表", command=self.refresh_recommendations).pack(side=tk.LEFT)
        
        # 建议列表框架
        list_frame = ttk.LabelFrame(main_frame, text="节能建议列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建议列表
        columns = ('ID', '设备', '类型', '优先级', '描述', '预期节能', '状态')
        self.rec_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.rec_tree.heading(col, text=col)
            if col == '描述':
                self.rec_tree.column(col, width=200)
            else:
                self.rec_tree.column(col, width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.rec_tree.yview)
        self.rec_tree.configure(yscrollcommand=scrollbar.set)
        
        self.rec_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮框架
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="实施建议", command=self.implement_recommendation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="查看详情", command=self.show_recommendation_details).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="跟踪效果", command=self.track_savings).pack(side=tk.LEFT)
        
        # 加载建议列表
        self.refresh_recommendations()
    
    def generate_recommendations(self):
        """生成节能建议"""
        if not self.device_var.get():
            messagebox.showwarning("警告", "请选择设备")
            return
        
        try:
            device_id = self.device_var.get().split(' - ')[0]
            
            recs, msg = self.ems.generate_energy_recommendations(device_id)
            
            if recs:
                messagebox.showinfo("成功", f"{msg}\n生成了 {len(recs)} 条建议")
                self.refresh_recommendations()
            else:
                messagebox.showinfo("提示", msg)
                
        except Exception as e:
            messagebox.showerror("错误", f"生成建议失败: {e}")
    
    def refresh_recommendations(self):
        """刷新建议列表"""
        # 清空现有数据
        for item in self.rec_tree.get_children():
            self.rec_tree.delete(item)
        
        # 加载建议数据
        recommendations = self.ems.get_all_recommendations()
        for rec in recommendations:
            device = self.ems.find_device_by_id(rec['device_id'])
            device_name = device['name'] if device else rec['device_id']
            
            self.rec_tree.insert('', tk.END, values=(
                rec['id'],
                device_name,
                rec['type'],
                rec['priority'],
                rec['description'][:50] + '...' if len(rec['description']) > 50 else rec['description'],
                rec['estimated_savings'],
                rec['status']
            ))
    
    def implement_recommendation(self):
        """实施建议"""
        selection = self.rec_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要实施的建议")
            return
        
        item = self.rec_tree.item(selection[0])
        rec_id = item['values'][0]
        
        if messagebox.askyesno("确认", "确定要实施这条建议吗？"):
            try:
                success, msg = self.ems.implement_recommendation(rec_id)
                if success:
                    messagebox.showinfo("成功", msg)
                    self.refresh_recommendations()
                else:
                    messagebox.showerror("错误", msg)
            except Exception as e:
                messagebox.showerror("错误", f"实施建议失败: {e}")
    
    def show_recommendation_details(self):
        """显示建议详情"""
        selection = self.rec_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要查看的建议")
            return
        
        item = self.rec_tree.item(selection[0])
        rec_id = item['values'][0]
        
        rec = self.ems.find_recommendation_by_id(rec_id)
        if rec:
            device = self.ems.find_device_by_id(rec['device_id'])
            device_name = device['name'] if device else rec['device_id']
            
            details = f"""
节能建议详情

建议ID: {rec['id']}
设备: {device_name} ({rec['device_id']})
类型: {rec['type']}
优先级: {rec['priority']}

描述: {rec['description']}

预期节能效果: {rec['estimated_savings']}
实施成本: {rec['implementation_cost']} 元
回报周期: {rec['payback_period']}

状态: {rec['status']}
创建日期: {rec['created_date']}
            """
            
            if 'implementation_date' in rec:
                details += f"实施日期: {rec['implementation_date']}\n"
            
            messagebox.showinfo("建议详情", details)
    
    def track_savings(self):
        """跟踪节能效果"""
        selection = self.rec_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要跟踪的建议")
            return
        
        item = self.rec_tree.item(selection[0])
        rec_id = item['values'][0]
        
        try:
            savings, msg = self.ems.track_savings_performance(rec_id)
            
            if savings:
                result = f"""
节能效果跟踪结果

建议ID: {savings['recommendation_id']}
设备ID: {savings['device_id']}

=== 节能效果 ===
基准日均能耗: {savings['baseline_daily_consumption']} kWh
当前日均能耗: {savings['current_daily_consumption']} kWh
日节能量: {savings['daily_energy_saved']} kWh
节能比例: {savings['savings_percentage']}%

测量日期: {savings['measurement_date']}

=== 效果评估 ===
"""
                if savings['savings_percentage'] > 10:
                    result += "✓ 节能效果显著"
                elif savings['savings_percentage'] > 5:
                    result += "○ 节能效果良好"
                elif savings['savings_percentage'] > 0:
                    result += "△ 有一定节能效果"
                else:
                    result += "✗ 暂未发现明显节能效果"
                
                messagebox.showinfo("节能效果", result)
            else:
                messagebox.showinfo("提示", msg)
                
        except Exception as e:
            messagebox.showerror("错误", f"跟踪效果失败: {e}")


class CostCalculationWindow:
    """成本计算窗口"""
    
    def __init__(self, parent, ems):
        self.ems = ems
        
        self.window = tk.Toplevel(parent)
        self.window.title("成本计算")
        self.window.geometry("800x600")
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="成本计算", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 计算参数框架
        param_frame = ttk.LabelFrame(main_frame, text="计算参数", padding=10)
        param_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 设备选择
        ttk.Label(param_frame, text="选择设备:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(param_frame, textvariable=self.device_var, width=30)
        self.device_combo.grid(row=0, column=1, padx=(0, 20))
        
        # 加载设备列表
        devices = self.ems.get_all_devices()
        device_list = [f"{d['id']} - {d['name']}" for d in devices]
        self.device_combo['values'] = device_list
        if device_list:
            self.device_combo.set(device_list[0])
        
        # 计算类型
        ttk.Label(param_frame, text="计算类型:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.calc_type_var = tk.StringVar(value="daily")
        calc_type_combo = ttk.Combobox(param_frame, textvariable=self.calc_type_var, width=15)
        calc_type_combo['values'] = ['daily', 'monthly']
        calc_type_combo.grid(row=0, column=3, padx=(0, 20))
        
        # 日期选择
        ttk.Label(param_frame, text="日期:").grid(row=1, column=0, sticky='w', padx=(0, 10))
        
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(param_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=1, column=1, sticky='w', padx=(0, 20))
        
        # 月份选择（用于月度计算）
        ttk.Label(param_frame, text="年月:").grid(row=1, column=2, sticky='w', padx=(0, 10))
        
        self.month_var = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        month_entry = ttk.Entry(param_frame, textvariable=self.month_var, width=15)
        month_entry.grid(row=1, column=3, sticky='w', padx=(0, 20))
        
        # 计算按钮
        ttk.Button(param_frame, text="计算成本", command=self.calculate_cost).grid(row=2, column=0, columnspan=4, pady=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=20, width=80)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def calculate_cost(self):
        """计算成本"""
        if not self.device_var.get():
            messagebox.showwarning("警告", "请选择设备")
            return
        
        try:
            device_id = self.device_var.get().split(' - ')[0]
            calc_type = self.calc_type_var.get()
            
            self.result_text.delete(1.0, tk.END)
            
            if calc_type == "daily":
                # 日成本计算
                date_str = self.date_var.get()
                cost_analysis, msg = self.ems.calculate_electricity_cost(device_id, date_str)
                self.display_daily_cost(cost_analysis, msg, date_str)
                
            elif calc_type == "monthly":
                # 月成本计算
                year_month = self.month_var.get()
                year, month = map(int, year_month.split('-'))
                monthly_cost, msg = self.ems.calculate_monthly_cost(device_id, year, month)
                self.display_monthly_cost(monthly_cost, msg, year, month)
                
        except ValueError:
            messagebox.showerror("错误", "请输入正确的日期格式")
        except Exception as e:
            messagebox.showerror("错误", f"计算成本失败: {e}")
    
    def display_daily_cost(self, cost_analysis, msg, date_str):
        """显示日成本计算结果"""
        if cost_analysis:
            device = self.ems.find_device_by_id(cost_analysis['device_id'])
            device_name = device['name'] if device else cost_analysis['device_id']
            
            result = f"""
日电费成本计算结果

设备: {device_name} ({cost_analysis['device_id']})
计算日期: {date_str}

=== 用电统计 ===
总用电量: {cost_analysis['total_energy_kwh']} kWh
峰时用电: {cost_analysis['peak_energy_kwh']} kWh
谷时用电: {cost_analysis['valley_energy_kwh']} kWh

=== 费用明细 ===
总电费: {cost_analysis['total_cost']} 元
峰时电费: {cost_analysis['peak_cost']} 元
谷时电费: {cost_analysis['valley_cost']} 元
平均电价: {cost_analysis['average_rate']} 元/kWh

=== 费用分析 ===
峰时费用占比: {(cost_analysis['peak_cost']/cost_analysis['total_cost']*100):.1f}%
谷时费用占比: {(cost_analysis['valley_cost']/cost_analysis['total_cost']*100):.1f}%

=== 节费建议 ===
"""
            peak_ratio = cost_analysis['peak_cost'] / cost_analysis['total_cost'] if cost_analysis['total_cost'] > 0 else 0
            if peak_ratio > 0.8:
                result += "• 峰时用电比例较高，建议将部分用电转移到谷时\n"
                result += "• 谷时电价更优惠，可节省电费成本\n"
            elif peak_ratio > 0.6:
                result += "• 可考虑优化用电时间安排\n"
            else:
                result += "• 用电时间安排较为合理\n"
            
            # 计算潜在节费
            if cost_analysis['peak_energy_kwh'] > 0:
                potential_savings = cost_analysis['peak_energy_kwh'] * (0.85 - 0.45) * 0.3  # 假设30%峰时用电可转移
                result += f"• 如将30%峰时用电转移到谷时，可节省约 {potential_savings:.2f} 元\n"
            
            self.result_text.insert(tk.END, result)
        else:
            self.result_text.insert(tk.END, f"日成本计算失败: {msg}")
    
    def display_monthly_cost(self, monthly_cost, msg, year, month):
        """显示月成本计算结果"""
        if monthly_cost:
            device = self.ems.find_device_by_id(monthly_cost['device_id'])
            device_name = device['name'] if device else monthly_cost['device_id']
            
            result = f"""
月电费成本计算结果

设备: {device_name} ({monthly_cost['device_id']})
计算月份: {year}年{month}月

=== 月度统计 ===
总用电量: {monthly_cost['total_energy_kwh']} kWh
总电费: {monthly_cost['total_cost']} 元
日均用电: {monthly_cost['average_daily_energy']} kWh
日均电费: {monthly_cost['average_daily_cost']} 元

=== 趋势分析 ===
"""
            # 分析每日用电趋势
            if 'daily_breakdown' in monthly_cost and monthly_cost['daily_breakdown']:
                daily_costs = [d['cost'] for d in monthly_cost['daily_breakdown']]
                daily_energies = [d['energy'] for d in monthly_cost['daily_breakdown']]
                
                max_cost_day = max(monthly_cost['daily_breakdown'], key=lambda x: x['cost'])
                min_cost_day = min(monthly_cost['daily_breakdown'], key=lambda x: x['cost'])
                
                result += f"最高电费日: {max_cost_day['date']} ({max_cost_day['cost']:.2f}元)\n"
                result += f"最低电费日: {min_cost_day['date']} ({min_cost_day['cost']:.2f}元)\n"
                result += f"费用波动: {(max_cost_day['cost'] - min_cost_day['cost']):.2f}元\n\n"
            
            result += f"""
=== 成本预测 ===
按当前用电模式，下月预计电费: {monthly_cost['total_cost'] * 1.05:.2f} 元 (考虑5%增长)

=== 节费建议 ===
• 关注高电费日的用电情况，分析原因
• 制定月度用电预算，控制电费支出
• 定期检查设备运行状态，提高用电效率
            """
            
            self.result_text.insert(tk.END, result)
        else:
            self.result_text.insert(tk.END, f"月成本计算失败: {msg}")


class ReportGenerationWindow:
    """报表生成窗口"""
    
    def __init__(self, parent, ems):
        self.ems = ems
        
        self.window = tk.Toplevel(parent)
        self.window.title("报表生成")
        self.window.geometry("900x700")
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="报表生成", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 报表参数框架
        param_frame = ttk.LabelFrame(main_frame, text="报表参数", padding=10)
        param_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 报表类型
        ttk.Label(param_frame, text="报表类型:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.report_type_var = tk.StringVar(value="daily")
        report_type_combo = ttk.Combobox(param_frame, textvariable=self.report_type_var, width=15)
        report_type_combo['values'] = ['daily', 'monthly']
        report_type_combo.grid(row=0, column=1, padx=(0, 20))
        
        # 日期选择
        ttk.Label(param_frame, text="日期:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(param_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=0, column=3, padx=(0, 20))
        
        # 月份选择
        ttk.Label(param_frame, text="年月:").grid(row=1, column=0, sticky='w', padx=(0, 10))
        
        self.month_var = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        month_entry = ttk.Entry(param_frame, textvariable=self.month_var, width=15)
        month_entry.grid(row=1, column=1, padx=(0, 20))
        
        # 生成按钮
        ttk.Button(param_frame, text="生成报表", command=self.generate_report).grid(row=0, column=4, rowspan=2, padx=10)
        
        # 报表显示区域
        display_frame = ttk.LabelFrame(main_frame, text="报表内容", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Notebook
        notebook = ttk.Notebook(display_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 报表内容标签页
        self.create_report_content_tab(notebook)
        
        # 报表列表标签页
        self.create_report_list_tab(notebook)
    
    def create_report_content_tab(self, notebook):
        """创建报表内容标签页"""
        content_frame = ttk.Frame(notebook)
        notebook.add(content_frame, text="报表内容")
        
        self.content_text = tk.Text(content_frame, height=25, width=80)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=scrollbar.set)
        
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="导出报表", command=self.export_report).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="打印报表", command=self.print_report).pack(side=tk.LEFT)
    
    def create_report_list_tab(self, notebook):
        """创建报表列表标签页"""
        list_frame = ttk.Frame(notebook)
        notebook.add(list_frame, text="历史报表")
        
        # 报表列表
        columns = ('ID', '名称', '类型', '开始日期', '结束日期', '生成日期')
        self.report_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            if col == '名称':
                self.report_tree.column(col, width=200)
            else:
                self.report_tree.column(col, width=100)
        
        scrollbar2 = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮
        btn_frame2 = ttk.Frame(list_frame)
        btn_frame2.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame2, text="刷新列表", command=self.refresh_report_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame2, text="查看报表", command=self.view_report).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame2, text="删除报表", command=self.delete_report).pack(side=tk.LEFT)
        
        # 加载报表列表
        self.refresh_report_list()
    
    def generate_report(self):
        """生成报表"""
        try:
            report_type = self.report_type_var.get()
            
            self.content_text.delete(1.0, tk.END)
            
            if report_type == "daily":
                # 生成日报表
                date_str = self.date_var.get()
                report_data, msg = self.ems.generate_daily_report(date_str)
                self.display_daily_report(report_data, msg, date_str)
                
            elif report_type == "monthly":
                # 生成月报表
                year_month = self.month_var.get()
                year, month = map(int, year_month.split('-'))
                report_data, msg = self.ems.generate_monthly_report(year, month)
                self.display_monthly_report(report_data, msg, year, month)
            
            # 刷新报表列表
            self.refresh_report_list()
                
        except ValueError:
            messagebox.showerror("错误", "请输入正确的日期格式")
        except Exception as e:
            messagebox.showerror("错误", f"生成报表失败: {e}")
    
    def display_daily_report(self, report_data, msg, date_str):
        """显示日报表"""
        if report_data:
            report_content = f"""
═══════════════════════════════════════
            日能耗报表
═══════════════════════════════════════

报表日期: {date_str}
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

═══════════════════════════════════════
                总体概况
═══════════════════════════════════════

总用电量: {report_data['total_consumption']:.3f} kWh
总电费: {report_data['total_cost']:.2f} 元
活跃告警: {report_data['alerts_count']} 个
参与统计设备: {len(report_data['devices'])} 台

"""
            if 'efficiency_summary' in report_data and report_data['efficiency_summary']:
                eff = report_data['efficiency_summary']
                report_content += f"""
═══════════════════════════════════════
                效率概况
═══════════════════════════════════════

平均效率: {eff['average_efficiency']:.2f}%
最高效率: {eff['max_efficiency']:.2f}%
最低效率: {eff['min_efficiency']:.2f}%

"""
            
            report_content += """
═══════════════════════════════════════
                设备明细
═══════════════════════════════════════

"""
            
            for device in report_data['devices']:
                report_content += f"""
设备: {device['device_name']} ({device['device_id']})
类型: {device['device_type']}
用电量: {device['energy_consumed']:.3f} kWh
电费: {device['cost']:.2f} 元
效率: {device['efficiency']:.2f}%
状态: {device['status']}
{'─' * 50}
"""
            
            report_content += f"""

═══════════════════════════════════════
                分析建议
═══════════════════════════════════════

1. 能耗分析
   • 日均用电量: {report_data['total_consumption']:.3f} kWh
   • 日均电费: {report_data['total_cost']:.2f} 元
   
2. 效率评估
"""
            if 'efficiency_summary' in report_data and report_data['efficiency_summary']:
                avg_eff = report_data['efficiency_summary']['average_efficiency']
                if avg_eff >= 85:
                    report_content += "   • 整体运行效率良好\n"
                elif avg_eff >= 70:
                    report_content += "   • 整体运行效率一般，有优化空间\n"
                else:
                    report_content += "   • 整体运行效率较低，需要重点关注\n"
            
            report_content += """
3. 运维建议
   • 定期检查低效率设备
   • 关注异常告警信息
   • 优化设备运行时间安排

═══════════════════════════════════════
                报表结束
═══════════════════════════════════════
"""
            
            self.content_text.insert(tk.END, report_content)
            messagebox.showinfo("成功", msg)
        else:
            self.content_text.insert(tk.END, f"日报表生成失败: {msg}")
    
    def display_monthly_report(self, report_data, msg, year, month):
        """显示月报表"""
        if report_data:
            report_content = f"""
═══════════════════════════════════════
            月能耗报表
═══════════════════════════════════════

报表月份: {year}年{month}月
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

═══════════════════════════════════════
                总体概况
═══════════════════════════════════════

总用电量: {report_data['total_consumption']:.3f} kWh
总电费: {report_data['total_cost']:.2f} 元
参与统计设备: {len(report_data['devices'])} 台

═══════════════════════════════════════
                设备明细
═══════════════════════════════════════

"""
            
            for device in report_data['devices']:
                report_content += f"""
设备: {device['device_name']} ({device['device_id']})
类型: {device['device_type']}
月用电量: {device['monthly_consumption']:.3f} kWh
月电费: {device['monthly_cost']:.2f} 元
日均用电: {device['average_daily_consumption']:.3f} kWh
日均电费: {device['average_daily_cost']:.2f} 元
{'─' * 50}
"""
            
            # 计算一些统计信息
            if report_data['devices']:
                max_consumption_device = max(report_data['devices'], key=lambda x: x['monthly_consumption'])
                max_cost_device = max(report_data['devices'], key=lambda x: x['monthly_cost'])
                
                report_content += f"""

═══════════════════════════════════════
                统计分析
═══════════════════════════════════════

1. 用电量分析
   • 最高用电设备: {max_consumption_device['device_name']} ({max_consumption_device['monthly_consumption']:.3f} kWh)
   • 平均设备用电: {report_data['total_consumption']/len(report_data['devices']):.3f} kWh

2. 费用分析
   • 最高费用设备: {max_cost_device['device_name']} ({max_cost_device['monthly_cost']:.2f} 元)
   • 平均设备费用: {report_data['total_cost']/len(report_data['devices']):.2f} 元
   • 平均电价: {report_data['total_cost']/report_data['total_consumption']:.3f} 元/kWh

3. 趋势预测
   • 下月预计用电: {report_data['total_consumption'] * 1.05:.3f} kWh
   • 下月预计费用: {report_data['total_cost'] * 1.05:.2f} 元

═══════════════════════════════════════
                改进建议
═══════════════════════════════════════

1. 节能措施
   • 重点关注高耗能设备的运行优化
   • 制定设备维护计划，提高运行效率
   • 考虑更换老旧低效设备

2. 成本控制
   • 合理安排用电时间，利用峰谷电价
   • 设置月度用电预算，控制费用支出
   • 定期分析用电模式，发现节费机会

═══════════════════════════════════════
                报表结束
═══════════════════════════════════════
"""
            
            self.content_text.insert(tk.END, report_content)
            messagebox.showinfo("成功", msg)
        else:
            self.content_text.insert(tk.END, f"月报表生成失败: {msg}")
    
    def refresh_report_list(self):
        """刷新报表列表"""
        # 清空现有数据
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # 加载报表数据
        reports = self.ems.data.get('reports', [])
        for report in reports:
            self.report_tree.insert('', tk.END, values=(
                report['id'],
                report['name'],
                report['type'],
                report['period_start'],
                report['period_end'],
                report['generated_date']
            ))
    
    def view_report(self):
        """查看报表"""
        selection = self.report_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要查看的报表")
            return
        
        messagebox.showinfo("提示", "查看历史报表功能开发中")
    
    def delete_report(self):
        """删除报表"""
        selection = self.report_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的报表")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的报表吗？"):
            messagebox.showinfo("提示", "删除报表功能开发中")
    
    def export_report(self):
        """导出报表"""
        content = self.content_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有可导出的报表内容")
            return
        
        filename = filedialog.asksaveasfilename(
            title="导出报表",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"报表已导出到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def print_report(self):
        """打印报表"""
        messagebox.showinfo("提示", "打印功能开发中")


if __name__ == "__main__":
    app = EnergyManagementGUI()
    app.run()

