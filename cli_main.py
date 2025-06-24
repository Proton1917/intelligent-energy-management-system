#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能能耗管理系统 - 命令行版本
适用于无图形界面的环境
"""

import os
import sys
from datetime import datetime
from energy_management_system import EnergyManagementSystem


class EnergyManagementCLI:
    """智能能耗管理系统命令行界面"""
    
    def __init__(self):
        self.ems = EnergyManagementSystem()
        self.running = True
    
    def show_banner(self):
        """显示系统横幅"""
        print("=" * 60)
        print("           智能能耗管理系统 v1.0")
        print("=" * 60)
        print("开发语言: Python")
        print("界面类型: 命令行界面")
        print("数据存储: JSON格式")
        print("=" * 60)
        print()
    
    def show_main_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 40)
        print("           主菜单")
        print("=" * 40)
        print("1. 设备管理")
        print("2. 用电监控")
        print("3. 能耗分析")
        print("4. 节能建议")
        print("5. 成本计算")
        print("6. 报表生成")
        print("7. 系统状态")
        print("8. 数据管理")
        print("0. 退出系统")
        print("=" * 40)
    
    def show_system_status(self):
        """显示系统状态"""
        print("\n" + "-" * 40)
        print("           系统状态")
        print("-" * 40)
        
        devices = self.ems.get_all_devices()
        alerts = self.ems.get_all_alerts('active')
        recommendations = self.ems.get_all_recommendations('pending')
        
        print(f"设备总数: {len(devices)}")
        print(f"活跃告警: {len(alerts)}")
        print(f"待处理建议: {len(recommendations)}")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)
    
    def device_management_menu(self):
        """设备管理菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      设备管理")
            print("-" * 30)
            print("1. 查看设备列表")
            print("2. 注册新设备")
            print("3. 设备详情")
            print("4. 设备维护")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.list_devices()
            elif choice == '2':
                self.register_device()
            elif choice == '3':
                self.show_device_details()
            elif choice == '4':
                self.schedule_maintenance()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def list_devices(self):
        """显示设备列表"""
        devices = self.ems.get_all_devices()
        
        if not devices:
            print("\n暂无设备记录")
            return
        
        print(f"\n设备列表 (共{len(devices)}台):")
        print("-" * 80)
        print(f"{'ID':<8} {'名称':<15} {'类型':<10} {'位置':<15} {'功率':<10} {'状态':<8}")
        print("-" * 80)
        
        for device in devices:
            print(f"{device['id']:<8} {device['name']:<15} {device['type']:<10} "
                  f"{device['location']:<15} {device['rated_power']:<10} {device['status']:<8}")
        print("-" * 80)
    
    def register_device(self):
        """注册新设备"""
        print("\n注册新设备:")
        print("-" * 20)
        
        try:
            name = input("设备名称: ").strip()
            if not name:
                print("设备名称不能为空")
                return
            
            device_type = input("设备类型 (HVAC/Lighting/Other): ").strip() or "Other"
            location = input("安装位置: ").strip() or "未指定"
            
            power_str = input("额定功率(W): ").strip()
            if not power_str:
                print("额定功率不能为空")
                return
            
            try:
                power = float(power_str)
            except ValueError:
                print("额定功率必须是数字")
                return
            
            efficiency = input("能效等级 (A++/A+/A/B/C) [A]: ").strip() or "A"
            manufacturer = input("制造商 [通用]: ").strip() or "通用"
            model = input("型号 [标准型]: ").strip() or "标准型"
            
            device_id, msg = self.ems.register_device(
                name, device_type, location, power, efficiency, manufacturer, model
            )
            
            if device_id:
                print(f"\n✓ {msg}")
            else:
                print(f"\n✗ {msg}")
                
        except KeyboardInterrupt:
            print("\n操作已取消")
        except Exception as e:
            print(f"\n✗ 注册设备失败: {e}")
    
    def show_device_details(self):
        """显示设备详情"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        device = self.ems.find_device_by_id(device_id)
        if not device:
            print("设备不存在")
            return
        
        print(f"\n设备详情:")
        print("-" * 30)
        print(f"ID: {device['id']}")
        print(f"名称: {device['name']}")
        print(f"类型: {device['type']}")
        print(f"位置: {device['location']}")
        print(f"额定功率: {device['rated_power']}W")
        print(f"能效等级: {device['energy_efficiency']}")
        print(f"制造商: {device['manufacturer']}")
        print(f"型号: {device['model']}")
        print(f"安装日期: {device['installation_date']}")
        print(f"最后维护: {device['last_maintenance']}")
        print(f"状态: {device['status']}")
        print("-" * 30)
    
    def schedule_maintenance(self):
        """安排设备维护"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        device = self.ems.find_device_by_id(device_id)
        if not device:
            print("设备不存在")
            return
        
        try:
            maintenance_type = input("维护类型 (preventive/corrective/routine) [preventive]: ").strip() or "preventive"
            scheduled_date = input("计划日期 (YYYY-MM-DD): ").strip()
            description = input("维护描述: ").strip()
            technician = input("技术员 [待分配]: ").strip() or "待分配"
            
            cost_str = input("预估费用 [0]: ").strip() or "0"
            try:
                cost = float(cost_str)
            except ValueError:
                cost = 0.0
            
            maint_id, msg = self.ems.schedule_maintenance(
                device_id, maintenance_type, scheduled_date, description, technician, cost
            )
            
            if maint_id:
                print(f"\n✓ {msg}")
            else:
                print(f"\n✗ {msg}")
                
        except KeyboardInterrupt:
            print("\n操作已取消")
        except Exception as e:
            print(f"\n✗ 安排维护失败: {e}")
    
    def energy_monitoring_menu(self):
        """用电监控菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      用电监控")
            print("-" * 30)
            print("1. 记录用电数据")
            print("2. 查看用电历史")
            print("3. 查看告警信息")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.record_energy_data()
            elif choice == '2':
                self.view_energy_history()
            elif choice == '3':
                self.view_alerts()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def record_energy_data(self):
        """记录用电数据"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        device = self.ems.find_device_by_id(device_id)
        if not device:
            print("设备不存在")
            return
        
        try:
            voltage = float(input("电压(V) [220]: ").strip() or "220")
            current = float(input("电流(A): ").strip())
            power = float(input("功率(W): ").strip())
            temperature = float(input("温度(°C) [25]: ").strip() or "25")
            humidity = float(input("湿度(%) [60]: ").strip() or "60")
            
            success, msg = self.ems.record_energy_reading(
                device_id, voltage, current, power, temperature, humidity
            )
            
            if success:
                print(f"\n✓ {msg}")
            else:
                print(f"\n✗ {msg}")
                
        except ValueError:
            print("\n✗ 请输入有效的数值")
        except KeyboardInterrupt:
            print("\n操作已取消")
        except Exception as e:
            print(f"\n✗ 记录数据失败: {e}")
    
    def view_energy_history(self):
        """查看用电历史"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        device = self.ems.find_device_by_id(device_id)
        if not device:
            print("设备不存在")
            return
        
        try:
            hours = int(input("查看最近多少小时的数据 [24]: ").strip() or "24")
            readings = self.ems.get_device_readings(device_id, hours)
            
            if not readings:
                print(f"\n{device['name']} 最近{hours}小时内无用电数据")
                return
            
            print(f"\n{device['name']} 最近{hours}小时用电数据:")
            print("-" * 80)
            print(f"{'时间':<20} {'电压':<8} {'电流':<8} {'功率':<8} {'能耗':<10} {'温度':<8}")
            print("-" * 80)
            
            for reading in readings[-10:]:  # 显示最近10条
                print(f"{reading['timestamp']:<20} {reading['voltage']:<8.1f} "
                      f"{reading['current']:<8.2f} {reading['power']:<8.0f} "
                      f"{reading['energy_consumed']:<10.3f} {reading['temperature']:<8.1f}")
            
            if len(readings) > 10:
                print(f"... (共{len(readings)}条记录，仅显示最近10条)")
            print("-" * 80)
            
        except ValueError:
            print("\n✗ 请输入有效的小时数")
        except Exception as e:
            print(f"\n✗ 查看历史数据失败: {e}")
    
    def view_alerts(self):
        """查看告警信息"""
        alerts = self.ems.get_all_alerts()
        
        if not alerts:
            print("\n暂无告警信息")
            return
        
        print(f"\n告警信息 (共{len(alerts)}条):")
        print("-" * 80)
        print(f"{'ID':<10} {'设备ID':<10} {'类型':<15} {'严重程度':<8} {'时间':<20}")
        print("-" * 80)
        
        for alert in alerts[-10:]:  # 显示最近10条
            print(f"{alert['id']:<10} {alert['device_id']:<10} {alert['type']:<15} "
                  f"{alert['severity']:<8} {alert['timestamp']:<20}")
        
        if len(alerts) > 10:
            print(f"... (共{len(alerts)}条记录，仅显示最近10条)")
        print("-" * 80)
    
    def energy_analysis_menu(self):
        """能耗分析菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      能耗分析")
            print("-" * 30)
            print("1. 基础能耗分析")
            print("2. 峰谷用电分析")
            print("3. 能耗预测")
            print("4. 设备效率评级")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.basic_energy_analysis()
            elif choice == '2':
                self.peak_valley_analysis()
            elif choice == '3':
                self.energy_prediction()
            elif choice == '4':
                self.efficiency_rating()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def basic_energy_analysis(self):
        """基础能耗分析"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        try:
            days = int(input("分析天数 [7]: ").strip() or "7")
            analysis, msg = self.ems.analyze_energy_consumption(device_id, days)
            
            if analysis:
                print(f"\n{analysis['device_name']} 能耗分析结果:")
                print("-" * 40)
                print(f"分析周期: {analysis['period_days']} 天")
                print(f"总能耗: {analysis['total_energy_kwh']} kWh")
                print(f"平均功率: {analysis['average_power_w']} W")
                print(f"峰值功率: {analysis['peak_power_w']} W")
                print(f"最低功率: {analysis['min_power_w']} W")
                print(f"运行效率: {analysis['efficiency_percentage']}%")
                print(f"数据点数: {analysis['readings_count']} 个")
                print("-" * 40)
                
                # 效率评估
                eff = analysis['efficiency_percentage']
                if eff >= 90:
                    print("✓ 设备运行效率优秀")
                elif eff >= 80:
                    print("○ 设备运行效率良好")
                elif eff >= 70:
                    print("△ 设备运行效率一般，建议优化")
                else:
                    print("✗ 设备运行效率较低，需要检查")
            else:
                print(f"\n✗ {msg}")
                
        except ValueError:
            print("\n✗ 请输入有效的天数")
        except Exception as e:
            print(f"\n✗ 分析失败: {e}")
    
    def peak_valley_analysis(self):
        """峰谷用电分析"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        try:
            days = int(input("分析天数 [7]: ").strip() or "7")
            analysis, msg = self.ems.analyze_peak_valley_consumption(device_id, days)
            
            if analysis:
                print(f"\n峰谷用电分析结果:")
                print("-" * 40)
                print(f"分析周期: {analysis['period_days']} 天")
                print(f"峰时用电: {analysis['peak_consumption_kwh']} kWh ({analysis['peak_ratio_percent']}%)")
                print(f"谷时用电: {analysis['valley_consumption_kwh']} kWh ({analysis['valley_ratio_percent']}%)")
                print(f"总用电量: {analysis['total_consumption_kwh']} kWh")
                print("-" * 40)
                
                # 用电模式分析
                peak_ratio = analysis['peak_ratio_percent']
                if peak_ratio > 80:
                    print("建议: 主要在峰时用电，建议优化用电时间安排")
                elif peak_ratio > 60:
                    print("建议: 峰时用电较多，可考虑部分负载转移到谷时")
                else:
                    print("建议: 用电时间分布较为合理")
            else:
                print(f"\n✗ {msg}")
                
        except ValueError:
            print("\n✗ 请输入有效的天数")
        except Exception as e:
            print(f"\n✗ 分析失败: {e}")
    
    def energy_prediction(self):
        """能耗预测"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        try:
            hours = int(input("预测小时数 [24]: ").strip() or "24")
            prediction, msg = self.ems.predict_energy_consumption(device_id, hours)
            
            if prediction:
                print(f"\n能耗预测结果:")
                print("-" * 40)
                print(f"预测时长: {prediction['prediction_hours']} 小时")
                print(f"预测能耗: {prediction['predicted_energy_kwh']} kWh")
                print(f"基准功率: {prediction['base_power_w']} W")
                print(f"置信度: {prediction['confidence']*100:.1f}%")
                print("-" * 40)
                
                # 成本预估
                avg_rate = 0.65  # 平均电价
                estimated_cost = prediction['predicted_energy_kwh'] * avg_rate
                print(f"预估电费: {estimated_cost:.2f} 元")
            else:
                print(f"\n✗ {msg}")
                
        except ValueError:
            print("\n✗ 请输入有效的小时数")
        except Exception as e:
            print(f"\n✗ 预测失败: {e}")
    
    def efficiency_rating(self):
        """设备效率评级"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        try:
            rating, msg = self.ems.get_device_efficiency_rating(device_id)
            
            if rating:
                print(f"\n设备效率评级结果:")
                print("-" * 40)
                print(f"设备ID: {rating['device_id']}")
                print(f"运行效率: {rating['efficiency_percentage']}%")
                print(f"评级: {rating['rating']} ({rating['description']})")
                print(f"评估日期: {rating['evaluation_date']}")
                print(f"建议: {rating['recommendation']}")
                print("-" * 40)
            else:
                print(f"\n✗ {msg}")
                
        except Exception as e:
            print(f"\n✗ 评级失败: {e}")
    
    def recommendations_menu(self):
        """节能建议菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      节能建议")
            print("-" * 30)
            print("1. 生成节能建议")
            print("2. 查看建议列表")
            print("3. 实施建议")
            print("4. 跟踪节能效果")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.generate_recommendations()
            elif choice == '2':
                self.list_recommendations()
            elif choice == '3':
                self.implement_recommendation()
            elif choice == '4':
                self.track_savings()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def generate_recommendations(self):
        """生成节能建议"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        try:
            recs, msg = self.ems.generate_energy_recommendations(device_id)
            
            if recs:
                print(f"\n✓ {msg}")
                print(f"生成了 {len(recs)} 条建议")
                
                # 显示生成的建议
                for rec_id in recs:
                    rec = self.ems.find_recommendation_by_id(rec_id)
                    if rec:
                        print(f"\n建议 {rec['id']}:")
                        print(f"  类型: {rec['type']}")
                        print(f"  优先级: {rec['priority']}")
                        print(f"  描述: {rec['description']}")
                        print(f"  预期节能: {rec['estimated_savings']}")
            else:
                print(f"\n✗ {msg}")
                
        except Exception as e:
            print(f"\n✗ 生成建议失败: {e}")
    
    def list_recommendations(self):
        """查看建议列表"""
        recommendations = self.ems.get_all_recommendations()
        
        if not recommendations:
            print("\n暂无节能建议")
            return
        
        print(f"\n节能建议列表 (共{len(recommendations)}条):")
        print("-" * 80)
        print(f"{'ID':<8} {'设备ID':<10} {'类型':<15} {'优先级':<8} {'状态':<10}")
        print("-" * 80)
        
        for rec in recommendations:
            print(f"{rec['id']:<8} {rec['device_id']:<10} {rec['type']:<15} "
                  f"{rec['priority']:<8} {rec['status']:<10}")
        print("-" * 80)
    
    def implement_recommendation(self):
        """实施建议"""
        rec_id = input("\n请输入建议ID: ").strip()
        if not rec_id:
            print("建议ID不能为空")
            return
        
        try:
            success, msg = self.ems.implement_recommendation(rec_id)
            
            if success:
                print(f"\n✓ {msg}")
            else:
                print(f"\n✗ {msg}")
                
        except Exception as e:
            print(f"\n✗ 实施建议失败: {e}")
    
    def track_savings(self):
        """跟踪节能效果"""
        rec_id = input("\n请输入建议ID: ").strip()
        if not rec_id:
            print("建议ID不能为空")
            return
        
        try:
            savings, msg = self.ems.track_savings_performance(rec_id)
            
            if savings:
                print(f"\n节能效果跟踪结果:")
                print("-" * 40)
                print(f"建议ID: {savings['recommendation_id']}")
                print(f"设备ID: {savings['device_id']}")
                print(f"基准日均能耗: {savings['baseline_daily_consumption']} kWh")
                print(f"当前日均能耗: {savings['current_daily_consumption']} kWh")
                print(f"日节能量: {savings['daily_energy_saved']} kWh")
                print(f"节能比例: {savings['savings_percentage']}%")
                print("-" * 40)
                
                # 效果评估
                savings_pct = savings['savings_percentage']
                if savings_pct > 10:
                    print("✓ 节能效果显著")
                elif savings_pct > 5:
                    print("○ 节能效果良好")
                elif savings_pct > 0:
                    print("△ 有一定节能效果")
                else:
                    print("✗ 暂未发现明显节能效果")
            else:
                print(f"\n✗ {msg}")
                
        except Exception as e:
            print(f"\n✗ 跟踪效果失败: {e}")
    
    def cost_calculation_menu(self):
        """成本计算菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      成本计算")
            print("-" * 30)
            print("1. 日电费计算")
            print("2. 月电费计算")
            print("3. 预算差异分析")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.daily_cost_calculation()
            elif choice == '2':
                self.monthly_cost_calculation()
            elif choice == '3':
                self.budget_variance_analysis()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def daily_cost_calculation(self):
        """日电费计算"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        date_str = input("计算日期 (YYYY-MM-DD) [今天]: ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            cost_analysis, msg = self.ems.calculate_electricity_cost(device_id, date_str)
            
            if cost_analysis:
                device = self.ems.find_device_by_id(device_id)
                device_name = device['name'] if device else device_id
                
                print(f"\n{device_name} 日电费计算结果:")
                print("-" * 40)
                print(f"计算日期: {date_str}")
                print(f"总用电量: {cost_analysis['total_energy_kwh']} kWh")
                print(f"总电费: {cost_analysis['total_cost']} 元")
                print(f"峰时电费: {cost_analysis['peak_cost']} 元")
                print(f"谷时电费: {cost_analysis['valley_cost']} 元")
                print(f"平均电价: {cost_analysis['average_rate']} 元/kWh")
                print("-" * 40)
                
                # 费用分析
                if cost_analysis['total_cost'] > 0:
                    peak_ratio = cost_analysis['peak_cost'] / cost_analysis['total_cost']
                    if peak_ratio > 0.8:
                        print("建议: 峰时用电比例较高，建议将部分用电转移到谷时")
                    elif peak_ratio > 0.6:
                        print("建议: 可考虑优化用电时间安排")
                    else:
                        print("建议: 用电时间安排较为合理")
            else:
                print(f"\n✗ {msg}")
                
        except Exception as e:
            print(f"\n✗ 计算失败: {e}")
    
    def monthly_cost_calculation(self):
        """月电费计算"""
        device_id = input("\n请输入设备ID: ").strip()
        if not device_id:
            print("设备ID不能为空")
            return
        
        year_month = input("计算年月 (YYYY-MM) [本月]: ").strip()
        if not year_month:
            year_month = datetime.now().strftime("%Y-%m")
        
        try:
            year, month = map(int, year_month.split('-'))
            monthly_cost, msg = self.ems.calculate_monthly_cost(device_id, year, month)
            
            if monthly_cost:
                device = self.ems.find_device_by_id(device_id)
                device_name = device['name'] if device else device_id
                
                print(f"\n{device_name} 月电费计算结果:")
                print("-" * 40)
                print(f"计算月份: {year}年{month}月")
                print(f"总用电量: {monthly_cost['total_energy_kwh']} kWh")
                print(f"总电费: {monthly_cost['total_cost']} 元")
                print(f"日均用电: {monthly_cost['average_daily_energy']} kWh")
                print(f"日均电费: {monthly_cost['average_daily_cost']} 元")
                print("-" * 40)
                
                # 预测下月费用
                next_month_cost = monthly_cost['total_cost'] * 1.05
                print(f"下月预计电费: {next_month_cost:.2f} 元 (考虑5%增长)")
            else:
                print(f"\n✗ {msg}")
                
        except ValueError:
            print("\n✗ 请输入正确的年月格式 (YYYY-MM)")
        except Exception as e:
            print(f"\n✗ 计算失败: {e}")
    
    def budget_variance_analysis(self):
        """预算差异分析"""
        print("\n预算差异分析功能开发中...")
        print("当前系统中的预算数据:")
        
        budgets = self.ems.data.get('energy_budgets', [])
        if budgets:
            for budget in budgets:
                print(f"\n部门: {budget['department']}")
                print(f"月度预算: {budget['monthly_budget']} 元")
                print(f"当前支出: {budget['current_spending']} 元")
                print(f"剩余预算: {budget['remaining_budget']} 元")
        else:
            print("暂无预算数据")
    
    def report_generation_menu(self):
        """报表生成菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      报表生成")
            print("-" * 30)
            print("1. 生成日报表")
            print("2. 生成月报表")
            print("3. 查看历史报表")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.generate_daily_report()
            elif choice == '2':
                self.generate_monthly_report()
            elif choice == '3':
                self.list_reports()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def generate_daily_report(self):
        """生成日报表"""
        date_str = input("\n报表日期 (YYYY-MM-DD) [今天]: ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            report_data, msg = self.ems.generate_daily_report(date_str)
            
            if report_data:
                print(f"\n✓ {msg}")
                print("\n" + "=" * 50)
                print(f"           {date_str} 日能耗报表")
                print("=" * 50)
                print(f"总用电量: {report_data['total_consumption']:.3f} kWh")
                print(f"总电费: {report_data['total_cost']:.2f} 元")
                print(f"活跃告警: {report_data['alerts_count']} 个")
                print(f"参与统计设备: {len(report_data['devices'])} 台")
                
                if 'efficiency_summary' in report_data and report_data['efficiency_summary']:
                    eff = report_data['efficiency_summary']
                    print(f"平均效率: {eff['average_efficiency']:.2f}%")
                
                print("\n设备明细:")
                print("-" * 50)
                for device in report_data['devices']:
                    print(f"{device['device_name']}: {device['energy_consumed']:.3f}kWh, "
                          f"{device['cost']:.2f}元, 效率{device['efficiency']:.1f}%")
                print("=" * 50)
            else:
                print(f"\n✗ {msg}")
                
        except Exception as e:
            print(f"\n✗ 生成报表失败: {e}")
    
    def generate_monthly_report(self):
        """生成月报表"""
        year_month = input("\n报表年月 (YYYY-MM) [本月]: ").strip()
        if not year_month:
            year_month = datetime.now().strftime("%Y-%m")
        
        try:
            year, month = map(int, year_month.split('-'))
            report_data, msg = self.ems.generate_monthly_report(year, month)
            
            if report_data:
                print(f"\n✓ {msg}")
                print("\n" + "=" * 50)
                print(f"         {year}年{month}月能耗月报")
                print("=" * 50)
                print(f"总用电量: {report_data['total_consumption']:.3f} kWh")
                print(f"总电费: {report_data['total_cost']:.2f} 元")
                print(f"参与统计设备: {len(report_data['devices'])} 台")
                
                print("\n设备明细:")
                print("-" * 50)
                for device in report_data['devices']:
                    print(f"{device['device_name']}: {device['monthly_consumption']:.3f}kWh, "
                          f"{device['monthly_cost']:.2f}元")
                print("=" * 50)
            else:
                print(f"\n✗ {msg}")
                
        except ValueError:
            print("\n✗ 请输入正确的年月格式 (YYYY-MM)")
        except Exception as e:
            print(f"\n✗ 生成报表失败: {e}")
    
    def list_reports(self):
        """查看历史报表"""
        reports = self.ems.data.get('reports', [])
        
        if not reports:
            print("\n暂无历史报表")
            return
        
        print(f"\n历史报表列表 (共{len(reports)}份):")
        print("-" * 80)
        print(f"{'ID':<8} {'名称':<25} {'类型':<8} {'开始日期':<12} {'结束日期':<12}")
        print("-" * 80)
        
        for report in reports:
            print(f"{report['id']:<8} {report['name']:<25} {report['type']:<8} "
                  f"{report['period_start']:<12} {report['period_end']:<12}")
        print("-" * 80)
    
    def data_management_menu(self):
        """数据管理菜单"""
        while True:
            print("\n" + "-" * 30)
            print("      数据管理")
            print("-" * 30)
            print("1. 数据备份")
            print("2. 数据统计")
            print("3. 清理数据")
            print("0. 返回主菜单")
            print("-" * 30)
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.backup_data()
            elif choice == '2':
                self.data_statistics()
            elif choice == '3':
                self.clean_data()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def backup_data(self):
        """数据备份"""
        try:
            backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = os.path.join(os.path.dirname(self.ems.data_file), backup_file)
            
            import shutil
            shutil.copy2(self.ems.data_file, backup_path)
            
            print(f"\n✓ 数据已备份到: {backup_path}")
            
        except Exception as e:
            print(f"\n✗ 备份失败: {e}")
    
    def data_statistics(self):
        """数据统计"""
        print("\n系统数据统计:")
        print("-" * 30)
        print(f"设备数量: {len(self.ems.data['devices'])}")
        print(f"用电记录: {len(self.ems.data['energy_readings'])}")
        print(f"能耗记录: {len(self.ems.data['energy_consumption'])}")
        print(f"成本分析: {len(self.ems.data['cost_analysis'])}")
        print(f"节能建议: {len(self.ems.data['recommendations'])}")
        print(f"告警信息: {len(self.ems.data['alerts'])}")
        print(f"维护计划: {len(self.ems.data['maintenance_schedule'])}")
        print(f"报表数量: {len(self.ems.data['reports'])}")
        print(f"预算记录: {len(self.ems.data['energy_budgets'])}")
        print("-" * 30)
        
        # 文件大小
        try:
            file_size = os.path.getsize(self.ems.data_file)
            print(f"数据文件大小: {file_size/1024:.2f} KB")
        except:
            print("数据文件大小: 未知")
    
    def clean_data(self):
        """清理数据"""
        print("\n数据清理选项:")
        print("1. 清理30天前的用电记录")
        print("2. 清理已处理的告警")
        print("3. 清理已完成的维护记录")
        print("0. 取消")
        
        choice = input("请选择清理选项: ").strip()
        
        if choice == '1':
            print("清理30天前的用电记录功能开发中...")
        elif choice == '2':
            print("清理已处理的告警功能开发中...")
        elif choice == '3':
            print("清理已完成的维护记录功能开发中...")
        elif choice == '0':
            print("已取消")
        else:
            print("无效选择")
    
    def run(self):
        """运行主程序"""
        self.show_banner()
        
        while self.running:
            try:
                self.show_system_status()
                self.show_main_menu()
                
                choice = input("\n请选择功能: ").strip()
                
                if choice == '1':
                    self.device_management_menu()
                elif choice == '2':
                    self.energy_monitoring_menu()
                elif choice == '3':
                    self.energy_analysis_menu()
                elif choice == '4':
                    self.recommendations_menu()
                elif choice == '5':
                    self.cost_calculation_menu()
                elif choice == '6':
                    self.report_generation_menu()
                elif choice == '7':
                    self.show_system_status()
                elif choice == '8':
                    self.data_management_menu()
                elif choice == '0':
                    print("\n感谢使用智能能耗管理系统！")
                    self.running = False
                else:
                    print("\n无效选择，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                self.running = False
            except Exception as e:
                print(f"\n程序运行出错: {e}")
                print("请重试或联系技术支持")


if __name__ == "__main__":
    cli = EnergyManagementCLI()
    cli.run()

