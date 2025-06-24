#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能能耗管理系统演示脚本
"""

import time
import random
from datetime import datetime, timedelta
from energy_management_system import EnergyManagementSystem


class SystemDemo:
    """系统演示类"""
    
    def __init__(self):
        self.ems = EnergyManagementSystem()
    
    def print_banner(self):
        """打印横幅"""
        print("=" * 60)
        print("           智能能耗管理系统演示")
        print("=" * 60)
        print("本演示将展示系统的主要功能和特性")
        print("=" * 60)
        print()
    
    def demo_device_management(self):
        """演示设备管理功能"""
        print("🔧 演示：设备管理功能")
        print("-" * 30)
        
        # 显示现有设备
        devices = self.ems.get_all_devices()
        print(f"当前系统中有 {len(devices)} 台设备:")
        for device in devices:
            print(f"  • {device['name']} ({device['id']}) - {device['type']} - {device['status']}")
        
        # 注册新设备
        print("\n正在注册新的演示设备...")
        device_id, msg = self.ems.register_device(
            "演示空调设备", "HVAC", "演示办公室", 3000, "A+", "演示厂商", "DEMO-AC-001"
        )
        
        if device_id:
            print(f"✓ {msg}")
            
            # 安排维护
            maint_id, msg = self.ems.schedule_maintenance(
                device_id, "preventive", "2024-12-31", "年度保养", "张技术员", 500
            )
            print(f"✓ 已安排维护计划: {msg}")
        
        print()
        time.sleep(2)
    
    def demo_energy_monitoring(self):
        """演示用电监控功能"""
        print("⚡ 演示：用电监控功能")
        print("-" * 30)
        
        devices = self.ems.get_all_devices()
        if not devices:
            print("没有可用设备进行演示")
            return
        
        device = devices[0]
        print(f"正在监控设备: {device['name']} ({device['id']})")
        
        # 模拟实时数据记录
        print("模拟实时用电数据记录...")
        for i in range(5):
            voltage = 220 + random.uniform(-5, 5)
            current = 10 + random.uniform(-2, 2)
            power = voltage * current
            temperature = 25 + random.uniform(-3, 3)
            humidity = 60 + random.uniform(-10, 10)
            
            success, msg = self.ems.record_energy_reading(
                device['id'], voltage, current, power, temperature, humidity
            )
            
            if success:
                print(f"  记录 {i+1}: {voltage:.1f}V, {current:.2f}A, {power:.0f}W, {temperature:.1f}°C")
            
            time.sleep(0.5)
        
        # 查看告警
        alerts = self.ems.get_all_alerts('active')
        if alerts:
            print(f"\n⚠️  检测到 {len(alerts)} 个活跃告警:")
            for alert in alerts[-3:]:  # 显示最近3个
                print(f"  • {alert['type']}: {alert['message']}")
        else:
            print("\n✓ 当前无活跃告警")
        
        print()
        time.sleep(2)
    
    def demo_energy_analysis(self):
        """演示能耗分析功能"""
        print("📊 演示：能耗分析功能")
        print("-" * 30)
        
        devices = self.ems.get_all_devices()
        if not devices:
            print("没有可用设备进行演示")
            return
        
        device = devices[0]
        print(f"分析设备: {device['name']} ({device['id']})")
        
        # 基础能耗分析
        analysis, msg = self.ems.analyze_energy_consumption(device['id'], 7)
        if analysis:
            print(f"\n📈 7天能耗分析结果:")
            print(f"  • 总能耗: {analysis['total_energy_kwh']} kWh")
            print(f"  • 平均功率: {analysis['average_power_w']} W")
            print(f"  • 运行效率: {analysis['efficiency_percentage']}%")
            
            # 效率评估
            eff = analysis['efficiency_percentage']
            if eff >= 90:
                print(f"  • 评估: ✓ 运行效率优秀")
            elif eff >= 80:
                print(f"  • 评估: ○ 运行效率良好")
            else:
                print(f"  • 评估: △ 有优化空间")
        
        # 峰谷分析
        pv_analysis, msg = self.ems.analyze_peak_valley_consumption(device['id'], 7)
        if pv_analysis:
            print(f"\n🌅 峰谷用电分析:")
            print(f"  • 峰时用电: {pv_analysis['peak_consumption_kwh']} kWh ({pv_analysis['peak_ratio_percent']}%)")
            print(f"  • 谷时用电: {pv_analysis['valley_consumption_kwh']} kWh ({pv_analysis['valley_ratio_percent']}%)")
        
        # 效率评级
        rating, msg = self.ems.get_device_efficiency_rating(device['id'])
        if rating:
            print(f"\n🏆 设备效率评级:")
            print(f"  • 评级: {rating['rating']} ({rating['description']})")
            print(f"  • 建议: {rating['recommendation']}")
        
        print()
        time.sleep(2)
    
    def demo_recommendations(self):
        """演示节能建议功能"""
        print("💡 演示：节能建议功能")
        print("-" * 30)
        
        devices = self.ems.get_all_devices()
        if not devices:
            print("没有可用设备进行演示")
            return
        
        device = devices[0]
        print(f"为设备生成节能建议: {device['name']}")
        
        # 生成建议
        recs, msg = self.ems.generate_energy_recommendations(device['id'])
        if recs:
            print(f"✓ {msg}")
            print(f"生成了 {len(recs)} 条建议:")
            
            for rec_id in recs[:3]:  # 显示前3条
                rec = self.ems.find_recommendation_by_id(rec_id)
                if rec:
                    print(f"\n  建议 {rec['id']}:")
                    print(f"    类型: {rec['type']}")
                    print(f"    优先级: {rec['priority']}")
                    print(f"    描述: {rec['description']}")
                    print(f"    预期节能: {rec['estimated_savings']}")
            
            # 实施第一条建议
            if recs:
                rec_id = recs[0]
                success, msg = self.ems.implement_recommendation(rec_id)
                if success:
                    print(f"\n✓ 已实施建议 {rec_id}")
                    
                    # 跟踪效果
                    savings, msg = self.ems.track_savings_performance(rec_id)
                    if savings:
                        print(f"📊 节能效果: {savings['savings_percentage']}%")
        
        print()
        time.sleep(2)
    
    def demo_cost_calculation(self):
        """演示成本计算功能"""
        print("💰 演示：成本计算功能")
        print("-" * 30)
        
        devices = self.ems.get_all_devices()
        if not devices:
            print("没有可用设备进行演示")
            return
        
        device = devices[0]
        today = datetime.now().strftime("%Y-%m-%d")
        
        print(f"计算设备电费: {device['name']}")
        
        # 日成本计算
        cost_analysis, msg = self.ems.calculate_electricity_cost(device['id'], today)
        if cost_analysis:
            print(f"\n📅 {today} 电费明细:")
            print(f"  • 总用电量: {cost_analysis['total_energy_kwh']} kWh")
            print(f"  • 总电费: {cost_analysis['total_cost']} 元")
            print(f"  • 峰时电费: {cost_analysis['peak_cost']} 元")
            print(f"  • 谷时电费: {cost_analysis['valley_cost']} 元")
            print(f"  • 平均电价: {cost_analysis['average_rate']} 元/kWh")
        
        # 月成本计算
        now = datetime.now()
        monthly_cost, msg = self.ems.calculate_monthly_cost(device['id'], now.year, now.month)
        if monthly_cost:
            print(f"\n📊 {now.year}年{now.month}月费用统计:")
            print(f"  • 月度总电费: {monthly_cost['total_cost']} 元")
            print(f"  • 日均电费: {monthly_cost['average_daily_cost']} 元")
            print(f"  • 月度用电量: {monthly_cost['total_energy_kwh']} kWh")
        
        print()
        time.sleep(2)
    
    def demo_report_generation(self):
        """演示报表生成功能"""
        print("📋 演示：报表生成功能")
        print("-" * 30)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 生成日报表
        print(f"生成 {today} 日报表...")
        report_data, msg = self.ems.generate_daily_report(today)
        
        if report_data:
            print(f"✓ {msg}")
            print(f"\n📊 日报表摘要:")
            print(f"  • 总用电量: {report_data['total_consumption']:.3f} kWh")
            print(f"  • 总电费: {report_data['total_cost']:.2f} 元")
            print(f"  • 参与统计设备: {len(report_data['devices'])} 台")
            print(f"  • 活跃告警: {report_data['alerts_count']} 个")
            
            if 'efficiency_summary' in report_data and report_data['efficiency_summary']:
                eff = report_data['efficiency_summary']
                print(f"  • 平均效率: {eff['average_efficiency']:.1f}%")
        
        # 生成月报表
        now = datetime.now()
        print(f"\n生成 {now.year}年{now.month}月 月报表...")
        monthly_report, msg = self.ems.generate_monthly_report(now.year, now.month)
        
        if monthly_report:
            print(f"✓ {msg}")
            print(f"\n📊 月报表摘要:")
            print(f"  • 月度总用电: {monthly_report['total_consumption']:.3f} kWh")
            print(f"  • 月度总费用: {monthly_report['total_cost']:.2f} 元")
            print(f"  • 参与统计设备: {len(monthly_report['devices'])} 台")
        
        print()
        time.sleep(2)
    
    def demo_system_status(self):
        """演示系统状态"""
        print("🖥️  演示：系统状态总览")
        print("-" * 30)
        
        devices = self.ems.get_all_devices()
        alerts = self.ems.get_all_alerts()
        recommendations = self.ems.get_all_recommendations()
        reports = self.ems.data.get('reports', [])
        
        print(f"📊 系统统计:")
        print(f"  • 注册设备: {len(devices)} 台")
        print(f"  • 历史告警: {len(alerts)} 条")
        print(f"  • 节能建议: {len(recommendations)} 条")
        print(f"  • 生成报表: {len(reports)} 份")
        
        # 设备状态分布
        status_count = {}
        for device in devices:
            status = device['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        print(f"\n🔧 设备状态分布:")
        for status, count in status_count.items():
            print(f"  • {status}: {count} 台")
        
        # 告警严重程度分布
        if alerts:
            severity_count = {}
            for alert in alerts:
                severity = alert['severity']
                severity_count[severity] = severity_count.get(severity, 0) + 1
            
            print(f"\n⚠️  告警严重程度分布:")
            for severity, count in severity_count.items():
                print(f"  • {severity}: {count} 条")
        
        print()
        time.sleep(2)
    
    def run_demo(self):
        """运行完整演示"""
        self.print_banner()
        
        print("演示即将开始，请稍候...")
        time.sleep(2)
        
        # 依次演示各个功能模块
        self.demo_device_management()
        self.demo_energy_monitoring()
        self.demo_energy_analysis()
        self.demo_recommendations()
        self.demo_cost_calculation()
        self.demo_report_generation()
        self.demo_system_status()
        
        print("=" * 60)
        print("           演示完成")
        print("=" * 60)
        print("感谢观看智能能耗管理系统演示！")
        print("系统具备完整的设备管理、用电监控、能耗分析、")
        print("节能建议、成本计算和报表生成功能。")
        print("=" * 60)


if __name__ == "__main__":
    demo = SystemDemo()
    demo.run_demo()

