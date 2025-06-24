#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能能耗管理系统
作者：AI助手
版本：1.0
描述：实现用电监控、能耗分析、节能建议、成本计算、设备管理、报表生成等功能
"""

import json
import os
import math
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class EnergyManagementSystem:
    """智能能耗管理系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.data_file = os.path.join(os.path.dirname(__file__), "../data/energy_data.json")
        self.data = {}
        self.load_data()
        
    def load_data(self):
        """从JSON文件加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print("数据加载成功")
        except FileNotFoundError:
            print("数据文件不存在，创建默认数据")
            self.init_default_data()
        except json.JSONDecodeError:
            print("数据文件格式错误，创建默认数据")
            self.init_default_data()
    
    def save_data(self):
        """保存数据到JSON文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print("数据保存成功")
            return True
        except Exception as e:
            print(f"数据保存失败: {e}")
            return False
    
    def init_default_data(self):
        """初始化默认数据"""
        self.data = {
            "devices": [],
            "energy_readings": [],
            "energy_consumption": [],
            "tariff_rates": [
                {
                    "id": "TARIFF001",
                    "name": "峰时电价",
                    "time_start": "08:00:00",
                    "time_end": "22:00:00",
                    "rate_per_kwh": 0.85,
                    "season": "夏季",
                    "effective_date": "2024-01-01"
                },
                {
                    "id": "TARIFF002",
                    "name": "谷时电价",
                    "time_start": "22:00:00",
                    "time_end": "08:00:00",
                    "rate_per_kwh": 0.45,
                    "season": "夏季",
                    "effective_date": "2024-01-01"
                }
            ],
            "cost_analysis": [],
            "energy_savings": [],
            "recommendations": [],
            "alerts": [],
            "maintenance_schedule": [],
            "reports": [],
            "energy_budgets": [],
            "system_settings": {
                "monitoring_interval": 15,
                "alert_thresholds": {
                    "high_consumption": 1.2,
                    "low_efficiency": 0.8,
                    "cost_overrun": 1.1
                },
                "report_generation": {
                    "auto_generate": True,
                    "frequency": "monthly",
                    "recipients": []
                },
                "energy_targets": {
                    "monthly_reduction": 10.0,
                    "efficiency_improvement": 5.0,
                    "cost_reduction": 8.0
                }
            }
        }
        self.save_data()
    
    # ==================== 辅助方法 ====================
    
    def generate_id(self, prefix, collection_name):
        """生成唯一ID"""
        count = len(self.data[collection_name]) + 1
        return f"{prefix}{count:03d}"
    
    def find_device_by_id(self, device_id):
        """根据ID查找设备"""
        for device in self.data['devices']:
            if device['id'] == device_id:
                return device
        return None
    
    def find_recommendation_by_id(self, rec_id):
        """根据ID查找建议"""
        for rec in self.data['recommendations']:
            if rec['id'] == rec_id:
                return rec
        return None
    
    def get_current_timestamp(self):
        """获取当前时间戳"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_current_date(self):
        """获取当前日期"""
        return datetime.now().strftime("%Y-%m-%d")
    
    # ==================== 1. 用电监控系统 ====================
    
    def record_energy_reading(self, device_id, voltage, current, power, temperature=None, humidity=None):
        """记录实时用电数据"""
        try:
            device = self.find_device_by_id(device_id)
            if not device:
                return False, "设备不存在"
            
            reading_id = self.generate_id("READ", "energy_readings")
            reading = {
                "id": reading_id,
                "device_id": device_id,
                "timestamp": self.get_current_timestamp(),
                "voltage": float(voltage),
                "current": float(current),
                "power": float(power),
                "energy_consumed": round(float(power) / 1000, 3),  # 转换为kWh
                "power_factor": round(float(power) / (float(voltage) * float(current)), 3) if voltage and current else 0.95,
                "frequency": 50.0,
                "temperature": float(temperature) if temperature else 22.0,
                "humidity": float(humidity) if humidity else 65.0
            }
            
            self.data['energy_readings'].append(reading)
            
            # 检查异常
            self.check_energy_anomalies(reading)
            
            self.save_data()
            return True, f"用电数据记录成功，ID: {reading_id}"
            
        except Exception as e:
            return False, f"记录用电数据失败: {e}"
    
    def check_energy_anomalies(self, reading):
        """检查用电异常"""
        try:
            device = self.find_device_by_id(reading['device_id'])
            if not device:
                return
            
            # 检查功率是否超过额定功率的20%
            if reading['power'] > device['rated_power'] * 1.2:
                self.create_alert(
                    reading['device_id'], 
                    "high_consumption", 
                    "medium",
                    f"功率消耗超出正常范围: {reading['power']}W",
                    device['rated_power'], 
                    reading['power']
                )
            
            # 检查电压异常
            if reading['voltage'] < 200 or reading['voltage'] > 240:
                self.create_alert(
                    reading['device_id'], 
                    "voltage_abnormal", 
                    "high",
                    f"电压异常: {reading['voltage']}V",
                    220, 
                    reading['voltage']
                )
                
        except Exception as e:
            print(f"异常检查失败: {e}")
    
    def create_alert(self, device_id, alert_type, severity, message, threshold_value, actual_value):
        """创建告警"""
        try:
            alert_id = self.generate_id("ALERT", "alerts")
            alert = {
                "id": alert_id,
                "device_id": device_id,
                "type": alert_type,
                "severity": severity,
                "message": message,
                "threshold_value": threshold_value,
                "actual_value": actual_value,
                "timestamp": self.get_current_timestamp(),
                "status": "active",
                "acknowledged": False
            }
            
            self.data['alerts'].append(alert)
            return alert_id
            
        except Exception as e:
            print(f"创建告警失败: {e}")
            return None
    
    def get_device_readings(self, device_id, hours=24):
        """获取设备的用电读数"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        readings = []
        for reading in self.data['energy_readings']:
            if reading['device_id'] == device_id:
                reading_time = datetime.strptime(reading['timestamp'], "%Y-%m-%d %H:%M:%S")
                if start_time <= reading_time <= end_time:
                    readings.append(reading)
        
        return sorted(readings, key=lambda x: x['timestamp'])
    
    # ==================== 2. 能耗分析系统 ====================
    
    def analyze_energy_consumption(self, device_id, days=7):
        """分析设备能耗"""
        try:
            readings = self.get_device_readings(device_id, days * 24)
            if not readings:
                return None, "没有可用的数据进行分析"
            
            device = self.find_device_by_id(device_id)
            if not device:
                return None, "设备不存在"
            
            # 计算统计数据
            total_energy = sum(r['energy_consumed'] for r in readings)
            avg_power = sum(r['power'] for r in readings) / len(readings)
            peak_power = max(r['power'] for r in readings)
            min_power = min(r['power'] for r in readings)
            
            # 计算效率
            efficiency = (avg_power / device['rated_power']) * 100 if device['rated_power'] > 0 else 0
            
            analysis = {
                'device_id': device_id,
                'device_name': device['name'],
                'period_days': days,
                'total_energy_kwh': round(total_energy, 3),
                'average_power_w': round(avg_power, 2),
                'peak_power_w': peak_power,
                'min_power_w': min_power,
                'efficiency_percentage': round(efficiency, 2),
                'readings_count': len(readings),
                'analysis_date': self.get_current_date()
            }
            
            return analysis, "能耗分析完成"
            
        except Exception as e:
            return None, f"能耗分析失败: {e}"
    
    def predict_energy_consumption(self, device_id, hours=24):
        """预测未来能耗"""
        try:
            recent_readings = self.get_device_readings(device_id, hours=48)
            if len(recent_readings) < 10:
                return None, "数据不足，无法进行预测"
            
            # 简单移动平均预测
            recent_powers = [r['power'] for r in recent_readings[-10:]]
            avg_power = sum(recent_powers) / len(recent_powers)
            predicted_energy = (avg_power * hours) / 1000  # 转换为kWh
            
            # 考虑时间模式（简单的周期性调整）
            current_hour = datetime.now().hour
            if 8 <= current_hour <= 18:  # 工作时间
                predicted_energy *= 1.2
            else:  # 非工作时间
                predicted_energy *= 0.8
            
            prediction = {
                'device_id': device_id,
                'prediction_hours': hours,
                'predicted_energy_kwh': round(predicted_energy, 3),
                'confidence': 0.75,
                'prediction_date': self.get_current_timestamp(),
                'base_power_w': round(avg_power, 2)
            }
            
            return prediction, "能耗预测完成"
            
        except Exception as e:
            return None, f"能耗预测失败: {e}"
    
    def analyze_peak_valley_consumption(self, device_id, days=7):
        """分析峰谷用电"""
        try:
            readings = self.get_device_readings(device_id, days * 24)
            if not readings:
                return None, "没有可用的数据进行分析"
            
            peak_consumption = 0  # 8:00-22:00
            valley_consumption = 0  # 22:00-8:00
            
            for reading in readings:
                timestamp = datetime.strptime(reading['timestamp'], "%Y-%m-%d %H:%M:%S")
                hour = timestamp.hour
                
                if 8 <= hour < 22:
                    peak_consumption += reading['energy_consumed']
                else:
                    valley_consumption += reading['energy_consumed']
            
            total_consumption = peak_consumption + valley_consumption
            peak_ratio = (peak_consumption / total_consumption * 100) if total_consumption > 0 else 0
            valley_ratio = (valley_consumption / total_consumption * 100) if total_consumption > 0 else 0
            
            analysis = {
                'device_id': device_id,
                'period_days': days,
                'peak_consumption_kwh': round(peak_consumption, 3),
                'valley_consumption_kwh': round(valley_consumption, 3),
                'total_consumption_kwh': round(total_consumption, 3),
                'peak_ratio_percent': round(peak_ratio, 2),
                'valley_ratio_percent': round(valley_ratio, 2),
                'analysis_date': self.get_current_date()
            }
            
            return analysis, "峰谷用电分析完成"
            
        except Exception as e:
            return None, f"峰谷用电分析失败: {e}"
    
    # ==================== 3. 节能建议系统 ====================
    
    def generate_energy_recommendations(self, device_id):
        """生成节能建议"""
        try:
            device = self.find_device_by_id(device_id)
            if not device:
                return [], "设备不存在"
            
            recommendations = []
            
            # 分析近期能耗
            analysis, _ = self.analyze_energy_consumption(device_id, days=7)
            if not analysis:
                return [], "数据不足，无法生成建议"
            
            # 根据设备类型和能耗情况生成建议
            if device['type'] == 'HVAC':
                # 空调设备建议
                if analysis['efficiency_percentage'] > 90:
                    rec_id = self.create_recommendation(
                        device_id, "temperature_adjustment", "medium",
                        "建议将空调温度调高2度，可节能15%",
                        "15%节能效果", 0.0, "立即生效"
                    )
                    recommendations.append(rec_id)
                
                if analysis['average_power_w'] > device['rated_power'] * 0.8:
                    rec_id = self.create_recommendation(
                        device_id, "schedule_optimization", "high",
                        "建议在非工作时间关闭空调或调至节能模式",
                        "25%节能效果", 0.0, "立即生效"
                    )
                    recommendations.append(rec_id)
            
            elif device['type'] == 'Lighting':
                # 照明设备建议
                rec_id = self.create_recommendation(
                    device_id, "schedule_optimization", "low",
                    "建议在午休时间减少照明亮度",
                    "8%节能效果", 0.0, "立即生效"
                )
                recommendations.append(rec_id)
            
            # 通用建议
            if analysis['efficiency_percentage'] < 70:
                rec_id = self.create_recommendation(
                    device_id, "maintenance_check", "high",
                    "设备效率较低，建议进行维护检查",
                    "10-20%效率提升", 200.0, "1-2周"
                )
                recommendations.append(rec_id)
            
            return recommendations, "节能建议生成成功"
            
        except Exception as e:
            return [], f"生成节能建议失败: {e}"
    
    def create_recommendation(self, device_id, rec_type, priority, description, 
                            estimated_savings, implementation_cost, payback_period):
        """创建节能建议"""
        try:
            rec_id = self.generate_id("REC", "recommendations")
            recommendation = {
                "id": rec_id,
                "device_id": device_id,
                "type": rec_type,
                "priority": priority,
                "description": description,
                "estimated_savings": estimated_savings,
                "implementation_cost": implementation_cost,
                "payback_period": payback_period,
                "status": "pending",
                "created_date": self.get_current_date()
            }
            
            self.data['recommendations'].append(recommendation)
            return rec_id
            
        except Exception as e:
            print(f"创建建议失败: {e}")
            return None
    
    def implement_recommendation(self, rec_id):
        """实施节能建议"""
        try:
            rec = self.find_recommendation_by_id(rec_id)
            if not rec:
                return False, "建议不存在"
            
            rec['status'] = 'implemented'
            rec['implementation_date'] = self.get_current_date()
            
            self.save_data()
            return True, "建议已标记为已实施"
            
        except Exception as e:
            return False, f"实施建议失败: {e}"
    
    def track_savings_performance(self, rec_id):
        """跟踪节能效果"""
        try:
            rec = self.find_recommendation_by_id(rec_id)
            if not rec:
                return None, "建议不存在"
            
            if rec['status'] != 'implemented':
                return None, "建议尚未实施"
            
            device_id = rec['device_id']
            
            # 获取实施前后的能耗数据
            baseline_analysis, _ = self.analyze_energy_consumption(device_id, days=14)
            current_analysis, _ = self.analyze_energy_consumption(device_id, days=7)
            
            if baseline_analysis and current_analysis:
                baseline_consumption = baseline_analysis['total_energy_kwh']
                current_consumption = current_analysis['total_energy_kwh']
                
                # 按天计算平均值进行比较
                baseline_daily = baseline_consumption / baseline_analysis['period_days']
                current_daily = current_consumption / current_analysis['period_days']
                
                energy_saved = baseline_daily - current_daily
                savings_percentage = (energy_saved / baseline_daily * 100) if baseline_daily > 0 else 0
                
                savings_record = {
                    'recommendation_id': rec_id,
                    'device_id': device_id,
                    'baseline_daily_consumption': round(baseline_daily, 3),
                    'current_daily_consumption': round(current_daily, 3),
                    'daily_energy_saved': round(energy_saved, 3),
                    'savings_percentage': round(savings_percentage, 2),
                    'measurement_date': self.get_current_date()
                }
                
                return savings_record, "节能效果跟踪完成"
            
            return None, "数据不足，无法计算节能效果"
            
        except Exception as e:
            return None, f"跟踪节能效果失败: {e}"
    
    # ==================== 4. 成本计算系统 ====================
    
    def get_tariff_rate(self, rate_type, date_str=None):
        """获取电价费率"""
        try:
            if not date_str:
                date_str = self.get_current_date()
            
            for tariff in self.data['tariff_rates']:
                if rate_type == "peak" and "峰时" in tariff['name']:
                    return tariff['rate_per_kwh']
                elif rate_type == "valley" and "谷时" in tariff['name']:
                    return tariff['rate_per_kwh']
            
            # 默认费率
            return 0.65
            
        except Exception as e:
            print(f"获取电价费率失败: {e}")
            return 0.65
    
    def calculate_electricity_cost(self, device_id, date_str=None):
        """计算电费成本"""
        try:
            if not date_str:
                date_str = self.get_current_date()
            
            # 获取当天的用电数据
            readings = self.get_device_readings(device_id, hours=24)
            if not readings:
                return None, "没有可用的用电数据"
            
            total_cost = 0
            peak_cost = 0
            valley_cost = 0
            total_energy = 0
            
            for reading in readings:
                timestamp = datetime.strptime(reading['timestamp'], "%Y-%m-%d %H:%M:%S")
                hour = timestamp.hour
                energy_kwh = reading['energy_consumed']
                total_energy += energy_kwh
                
                # 判断峰谷时段
                if 8 <= hour < 22:  # 峰时
                    rate = self.get_tariff_rate("peak", date_str)
                    cost = energy_kwh * rate
                    peak_cost += cost
                else:  # 谷时
                    rate = self.get_tariff_rate("valley", date_str)
                    cost = energy_kwh * rate
                    valley_cost += cost
                
                total_cost += cost
            
            cost_analysis = {
                'device_id': device_id,
                'date': date_str,
                'total_cost': round(total_cost, 2),
                'peak_cost': round(peak_cost, 2),
                'valley_cost': round(valley_cost, 2),
                'total_energy_kwh': round(total_energy, 3),
                'average_rate': round(total_cost / total_energy, 3) if total_energy > 0 else 0,
                'peak_energy_kwh': round(sum(r['energy_consumed'] for r in readings 
                                           if 8 <= datetime.strptime(r['timestamp'], "%Y-%m-%d %H:%M:%S").hour < 22), 3),
                'valley_energy_kwh': round(sum(r['energy_consumed'] for r in readings 
                                             if not (8 <= datetime.strptime(r['timestamp'], "%Y-%m-%d %H:%M:%S").hour < 22)), 3)
            }
            
            # 保存成本分析
            cost_id = self.generate_id("COST", "cost_analysis")
            cost_record = cost_analysis.copy()
            cost_record['id'] = cost_id
            self.data['cost_analysis'].append(cost_record)
            self.save_data()
            
            return cost_analysis, "电费计算完成"
            
        except Exception as e:
            return None, f"电费计算失败: {e}"
    
    def calculate_monthly_cost(self, device_id, year, month):
        """计算月度电费"""
        try:
            # 获取月度数据
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
            total_cost = 0
            total_energy = 0
            daily_costs = []
            
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                daily_analysis, _ = self.calculate_electricity_cost(device_id, date_str)
                
                if daily_analysis:
                    total_cost += daily_analysis['total_cost']
                    total_energy += daily_analysis['total_energy_kwh']
                    daily_costs.append({
                        'date': date_str,
                        'cost': daily_analysis['total_cost'],
                        'energy': daily_analysis['total_energy_kwh']
                    })
                
                current_date += timedelta(days=1)
            
            monthly_analysis = {
                'device_id': device_id,
                'year': year,
                'month': month,
                'total_cost': round(total_cost, 2),
                'total_energy_kwh': round(total_energy, 3),
                'average_daily_cost': round(total_cost / (end_date - start_date).days, 2),
                'average_daily_energy': round(total_energy / (end_date - start_date).days, 3),
                'daily_breakdown': daily_costs
            }
            
            return monthly_analysis, "月度电费计算完成"
            
        except Exception as e:
            return None, f"月度电费计算失败: {e}"
    
    def check_budget_variance(self, department):
        """检查预算差异"""
        try:
            budget = None
            for b in self.data['energy_budgets']:
                if b['department'] == department:
                    budget = b
                    break
            
            if not budget:
                return None, "未找到该部门的预算信息"
            
            current_spending = budget['current_spending']
            monthly_budget = budget['monthly_budget']
            variance = current_spending - monthly_budget
            variance_percentage = (variance / monthly_budget * 100) if monthly_budget > 0 else 0
            
            status = "超支" if variance > 0 else "正常"
            
            # 如果超支，创建告警
            if variance > 0:
                self.create_alert(
                    "BUDGET", "budget_overrun", "high",
                    f"{department}部门预算超支 {variance:.2f}元",
                    monthly_budget, current_spending
                )
            
            variance_analysis = {
                'department': department,
                'monthly_budget': monthly_budget,
                'current_spending': current_spending,
                'remaining_budget': monthly_budget - current_spending,
                'variance': round(variance, 2),
                'variance_percentage': round(variance_percentage, 2),
                'status': status,
                'analysis_date': self.get_current_date()
            }
            
            return variance_analysis, "预算差异分析完成"
            
        except Exception as e:
            return None, f"预算差异分析失败: {e}"
    
    # ==================== 5. 设备管理系统 ====================
    
    def register_device(self, name, device_type, location, rated_power, 
                       energy_efficiency="A", manufacturer="通用", model="标准型"):
        """注册新设备"""
        try:
            device_id = self.generate_id("DEV", "devices")
            device = {
                "id": device_id,
                "name": name,
                "type": device_type,
                "location": location,
                "floor": 1,
                "room": "未指定",
                "rated_power": float(rated_power),
                "energy_efficiency": energy_efficiency,
                "installation_date": self.get_current_date(),
                "last_maintenance": self.get_current_date(),
                "status": "online",
                "manufacturer": manufacturer,
                "model": model
            }
            
            self.data['devices'].append(device)
            self.save_data()
            
            return device_id, f"设备注册成功，ID: {device_id}"
            
        except Exception as e:
            return None, f"设备注册失败: {e}"
    
    def update_device_status(self, device_id, status):
        """更新设备状态"""
        try:
            device = self.find_device_by_id(device_id)
            if not device:
                return False, "设备不存在"
            
            device['status'] = status
            device['last_updated'] = self.get_current_timestamp()
            
            self.save_data()
            return True, f"设备状态已更新为: {status}"
            
        except Exception as e:
            return False, f"更新设备状态失败: {e}"
    
    def schedule_maintenance(self, device_id, maintenance_type, scheduled_date, 
                           description, technician="待分配", cost_estimate=0.0):
        """安排设备维护"""
        try:
            device = self.find_device_by_id(device_id)
            if not device:
                return None, "设备不存在"
            
            maint_id = self.generate_id("MAINT", "maintenance_schedule")
            maintenance = {
                "id": maint_id,
                "device_id": device_id,
                "type": maintenance_type,
                "scheduled_date": scheduled_date,
                "description": description,
                "estimated_duration": 60,  # 默认60分钟
                "technician": technician,
                "cost_estimate": float(cost_estimate),
                "status": "scheduled",
                "created_date": self.get_current_date()
            }
            
            self.data['maintenance_schedule'].append(maintenance)
            self.save_data()
            
            return maint_id, f"维护计划已安排，ID: {maint_id}"
            
        except Exception as e:
            return None, f"安排维护失败: {e}"
    
    def get_device_efficiency_rating(self, device_id):
        """获取设备能效评级"""
        try:
            analysis, _ = self.analyze_energy_consumption(device_id, days=30)
            if not analysis:
                return None, "数据不足，无法评级"
            
            efficiency = analysis['efficiency_percentage']
            
            if efficiency >= 90:
                rating = "A++"
                description = "优秀"
            elif efficiency >= 80:
                rating = "A+"
                description = "良好"
            elif efficiency >= 70:
                rating = "A"
                description = "一般"
            elif efficiency >= 60:
                rating = "B"
                description = "较差"
            else:
                rating = "C"
                description = "差"
            
            rating_info = {
                'device_id': device_id,
                'efficiency_percentage': efficiency,
                'rating': rating,
                'description': description,
                'evaluation_date': self.get_current_date(),
                'recommendation': self.get_efficiency_recommendation(efficiency)
            }
            
            return rating_info, "设备能效评级完成"
            
        except Exception as e:
            return None, f"设备能效评级失败: {e}"
    
    def get_efficiency_recommendation(self, efficiency):
        """根据效率获取建议"""
        if efficiency >= 90:
            return "设备运行效率优秀，继续保持"
        elif efficiency >= 80:
            return "设备运行良好，可考虑优化运行参数"
        elif efficiency >= 70:
            return "建议检查设备运行状态，优化使用方式"
        elif efficiency >= 60:
            return "设备效率较低，建议进行维护检查"
        else:
            return "设备效率很低，建议立即检修或更换"
    
    # ==================== 6. 报表生成系统 ====================
    
    def generate_daily_report(self, date_str=None):
        """生成日报表"""
        try:
            if not date_str:
                date_str = self.get_current_date()
            
            report_data = {
                'report_type': 'daily',
                'date': date_str,
                'devices': [],
                'total_consumption': 0,
                'total_cost': 0,
                'alerts_count': 0,
                'efficiency_summary': {}
            }
            
            # 统计各设备数据
            for device in self.data['devices']:
                device_id = device['id']
                
                # 获取设备当日数据
                cost_analysis, _ = self.calculate_electricity_cost(device_id, date_str)
                energy_analysis, _ = self.analyze_energy_consumption(device_id, days=1)
                
                device_data = {
                    'device_id': device_id,
                    'device_name': device['name'],
                    'device_type': device['type'],
                    'energy_consumed': energy_analysis['total_energy_kwh'] if energy_analysis else 0,
                    'cost': cost_analysis['total_cost'] if cost_analysis else 0,
                    'efficiency': energy_analysis['efficiency_percentage'] if energy_analysis else 0,
                    'status': device['status']
                }
                
                report_data['devices'].append(device_data)
                report_data['total_consumption'] += device_data['energy_consumed']
                report_data['total_cost'] += device_data['cost']
            
            # 统计告警数量
            today_alerts = [alert for alert in self.data['alerts'] 
                          if alert['timestamp'].startswith(date_str)]
            report_data['alerts_count'] = len(today_alerts)
            
            # 效率汇总
            efficiencies = [d['efficiency'] for d in report_data['devices'] if d['efficiency'] > 0]
            if efficiencies:
                report_data['efficiency_summary'] = {
                    'average_efficiency': round(sum(efficiencies) / len(efficiencies), 2),
                    'max_efficiency': max(efficiencies),
                    'min_efficiency': min(efficiencies)
                }
            
            # 保存报表
            report_id = self.generate_id("RPT", "reports")
            report_record = {
                'id': report_id,
                'name': f"{date_str}日能耗报表",
                'type': 'daily',
                'period_start': date_str,
                'period_end': date_str,
                'total_consumption': round(report_data['total_consumption'], 3),
                'total_cost': round(report_data['total_cost'], 2),
                'generated_date': self.get_current_timestamp(),
                'data': report_data
            }
            
            self.data['reports'].append(report_record)
            self.save_data()
            
            return report_data, f"日报表生成成功，ID: {report_id}"
            
        except Exception as e:
            return None, f"生成日报表失败: {e}"
    
    def generate_monthly_report(self, year, month):
        """生成月报表"""
        try:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
            report_data = {
                'report_type': 'monthly',
                'year': year,
                'month': month,
                'period_start': start_date.strftime("%Y-%m-%d"),
                'period_end': end_date.strftime("%Y-%m-%d"),
                'devices': [],
                'total_consumption': 0,
                'total_cost': 0,
                'daily_breakdown': [],
                'efficiency_trends': {},
                'cost_trends': {}
            }
            
            # 按设备统计月度数据
            for device in self.data['devices']:
                device_id = device['id']
                monthly_cost, _ = self.calculate_monthly_cost(device_id, year, month)
                
                if monthly_cost:
                    device_data = {
                        'device_id': device_id,
                        'device_name': device['name'],
                        'device_type': device['type'],
                        'monthly_consumption': monthly_cost['total_energy_kwh'],
                        'monthly_cost': monthly_cost['total_cost'],
                        'average_daily_consumption': monthly_cost['average_daily_energy'],
                        'average_daily_cost': monthly_cost['average_daily_cost']
                    }
                    
                    report_data['devices'].append(device_data)
                    report_data['total_consumption'] += device_data['monthly_consumption']
                    report_data['total_cost'] += device_data['monthly_cost']
            
            # 保存月报表
            report_id = self.generate_id("RPT", "reports")
            report_record = {
                'id': report_id,
                'name': f"{year}年{month}月能耗月报",
                'type': 'monthly',
                'period_start': report_data['period_start'],
                'period_end': report_data['period_end'],
                'total_consumption': round(report_data['total_consumption'], 3),
                'total_cost': round(report_data['total_cost'], 2),
                'generated_date': self.get_current_timestamp(),
                'data': report_data
            }
            
            self.data['reports'].append(report_record)
            self.save_data()
            
            return report_data, f"月报表生成成功，ID: {report_id}"
            
        except Exception as e:
            return None, f"生成月报表失败: {e}"
    
    def export_report_to_file(self, report_id, file_format='json'):
        """导出报表到文件"""
        try:
            report = None
            for r in self.data['reports']:
                if r['id'] == report_id:
                    report = r
                    break
            
            if not report:
                return None, "报表不存在"
            
            filename = f"report_{report_id}_{report['type']}.{file_format}"
            filepath = os.path.join(os.path.dirname(self.data_file), filename)
            
            if file_format == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            else:
                return None, "不支持的文件格式"
            
            return filepath, f"报表已导出到: {filepath}"
            
        except Exception as e:
            return None, f"导出报表失败: {e}"
    
    def get_all_devices(self):
        """获取所有设备列表"""
        return self.data['devices']
    
    def get_all_alerts(self, status=None):
        """获取所有告警"""
        if status:
            return [alert for alert in self.data['alerts'] if alert['status'] == status]
        return self.data['alerts']
    
    def get_all_recommendations(self, status=None):
        """获取所有建议"""
        if status:
            return [rec for rec in self.data['recommendations'] if rec['status'] == status]
        return self.data['recommendations']


if __name__ == "__main__":
    # 测试基础功能
    ems = EnergyManagementSystem()
    print("智能能耗管理系统初始化完成")
    print(f"当前设备数量: {len(ems.data['devices'])}")
    print(f"当前读数数量: {len(ems.data['energy_readings'])}")

