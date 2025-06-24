#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能能耗管理系统综合测试脚本
"""

import sys
import os
import time
from datetime import datetime, timedelta
from energy_management_system import EnergyManagementSystem


class SystemTester:
    """系统测试类"""
    
    def __init__(self):
        self.ems = EnergyManagementSystem()
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
    
    def log_test(self, test_name, passed, message=""):
        """记录测试结果"""
        status = "PASS" if passed else "FAIL"
        result = f"[{status}] {test_name}"
        if message:
            result += f" - {message}"
        
        self.test_results.append(result)
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        
        print(result)
    
    def test_data_persistence(self):
        """测试数据持久化"""
        print("\n=== 测试数据持久化 ===")
        
        try:
            # 测试数据加载
            original_devices_count = len(self.ems.get_all_devices())
            self.log_test("数据加载", True, f"加载了{original_devices_count}个设备")
            
            # 测试数据保存
            self.ems.save_data()
            self.log_test("数据保存", True, "数据保存成功")
            
            # 测试数据重新加载
            new_ems = EnergyManagementSystem()
            new_devices_count = len(new_ems.get_all_devices())
            
            if new_devices_count == original_devices_count:
                self.log_test("数据重新加载", True, f"重新加载了{new_devices_count}个设备")
            else:
                self.log_test("数据重新加载", False, f"设备数量不匹配: {original_devices_count} vs {new_devices_count}")
                
        except Exception as e:
            self.log_test("数据持久化", False, str(e))
    
    def test_device_management(self):
        """测试设备管理功能"""
        print("\n=== 测试设备管理功能 ===")
        
        try:
            # 测试设备注册
            device_id, msg = self.ems.register_device(
                "测试设备", "Test", "测试位置", 1000, "A", "测试厂商", "测试型号"
            )
            
            if device_id:
                self.log_test("设备注册", True, f"设备ID: {device_id}")
                
                # 测试设备查找
                device = self.ems.find_device_by_id(device_id)
                if device:
                    self.log_test("设备查找", True, f"找到设备: {device['name']}")
                else:
                    self.log_test("设备查找", False, "未找到刚注册的设备")
                
                # 测试设备状态更新
                success, msg = self.ems.update_device_status(device_id, "maintenance")
                self.log_test("设备状态更新", success, msg)
                
                # 测试维护安排
                maint_id, msg = self.ems.schedule_maintenance(
                    device_id, "preventive", "2024-12-31", "测试维护", "测试技术员", 100
                )
                self.log_test("维护安排", bool(maint_id), msg)
                
            else:
                self.log_test("设备注册", False, msg)
                
        except Exception as e:
            self.log_test("设备管理功能", False, str(e))
    
    def test_energy_monitoring(self):
        """测试用电监控功能"""
        print("\n=== 测试用电监控功能 ===")
        
        try:
            devices = self.ems.get_all_devices()
            if not devices:
                self.log_test("用电监控", False, "没有可用设备")
                return
            
            device_id = devices[0]['id']
            
            # 测试用电数据记录
            success, msg = self.ems.record_energy_reading(
                device_id, 220, 5, 1100, 25, 60
            )
            self.log_test("用电数据记录", success, msg)
            
            # 测试数据查询
            readings = self.ems.get_device_readings(device_id, 24)
            self.log_test("用电数据查询", len(readings) > 0, f"查询到{len(readings)}条记录")
            
            # 测试告警检测
            success, msg = self.ems.record_energy_reading(
                device_id, 250, 15, 3750, 80, 90  # 异常数据
            )
            if success:
                alerts = self.ems.get_all_alerts('active')
                self.log_test("告警检测", len(alerts) > 0, f"检测到{len(alerts)}个告警")
            
        except Exception as e:
            self.log_test("用电监控功能", False, str(e))
    
    def test_energy_analysis(self):
        """测试能耗分析功能"""
        print("\n=== 测试能耗分析功能 ===")
        
        try:
            devices = self.ems.get_all_devices()
            if not devices:
                self.log_test("能耗分析", False, "没有可用设备")
                return
            
            device_id = devices[0]['id']
            
            # 测试基础能耗分析
            analysis, msg = self.ems.analyze_energy_consumption(device_id, 7)
            self.log_test("基础能耗分析", bool(analysis), msg)
            
            # 测试峰谷分析
            pv_analysis, msg = self.ems.analyze_peak_valley_consumption(device_id, 7)
            self.log_test("峰谷分析", bool(pv_analysis), msg)
            
            # 测试能耗预测
            prediction, msg = self.ems.predict_energy_consumption(device_id, 24)
            self.log_test("能耗预测", bool(prediction), msg)
            
            # 测试效率评级
            rating, msg = self.ems.get_device_efficiency_rating(device_id)
            self.log_test("效率评级", bool(rating), msg)
            
        except Exception as e:
            self.log_test("能耗分析功能", False, str(e))
    
    def test_recommendations(self):
        """测试节能建议功能"""
        print("\n=== 测试节能建议功能 ===")
        
        try:
            devices = self.ems.get_all_devices()
            if not devices:
                self.log_test("节能建议", False, "没有可用设备")
                return
            
            device_id = devices[0]['id']
            
            # 测试建议生成
            recs, msg = self.ems.generate_energy_recommendations(device_id)
            self.log_test("建议生成", bool(recs), msg)
            
            if recs:
                rec_id = recs[0]
                
                # 测试建议实施
                success, msg = self.ems.implement_recommendation(rec_id)
                self.log_test("建议实施", success, msg)
                
                # 测试效果跟踪
                savings, msg = self.ems.track_savings_performance(rec_id)
                self.log_test("效果跟踪", bool(savings), msg)
            
        except Exception as e:
            self.log_test("节能建议功能", False, str(e))
    
    def test_cost_calculation(self):
        """测试成本计算功能"""
        print("\n=== 测试成本计算功能 ===")
        
        try:
            devices = self.ems.get_all_devices()
            if not devices:
                self.log_test("成本计算", False, "没有可用设备")
                return
            
            device_id = devices[0]['id']
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 测试日成本计算
            cost_analysis, msg = self.ems.calculate_electricity_cost(device_id, today)
            self.log_test("日成本计算", bool(cost_analysis), msg)
            
            # 测试月成本计算
            now = datetime.now()
            monthly_cost, msg = self.ems.calculate_monthly_cost(device_id, now.year, now.month)
            self.log_test("月成本计算", bool(monthly_cost), msg)
            
        except Exception as e:
            self.log_test("成本计算功能", False, str(e))
    
    def test_report_generation(self):
        """测试报表生成功能"""
        print("\n=== 测试报表生成功能 ===")
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 测试日报表生成
            report_data, msg = self.ems.generate_daily_report(today)
            self.log_test("日报表生成", bool(report_data), msg)
            
            # 测试月报表生成
            now = datetime.now()
            monthly_report, msg = self.ems.generate_monthly_report(now.year, now.month)
            self.log_test("月报表生成", bool(monthly_report), msg)
            
        except Exception as e:
            self.log_test("报表生成功能", False, str(e))
    
    def test_performance(self):
        """测试系统性能"""
        print("\n=== 测试系统性能 ===")
        
        try:
            # 测试大量数据处理
            device_id = self.ems.get_all_devices()[0]['id'] if self.ems.get_all_devices() else None
            
            if device_id:
                start_time = time.time()
                
                # 批量添加数据
                for i in range(100):
                    self.ems.record_energy_reading(
                        device_id, 220 + i % 20, 5 + i % 5, 1100 + i * 10, 25 + i % 10, 60 + i % 20
                    )
                
                end_time = time.time()
                duration = end_time - start_time
                
                self.log_test("批量数据处理", duration < 5, f"处理100条记录耗时{duration:.2f}秒")
                
                # 测试数据查询性能
                start_time = time.time()
                readings = self.ems.get_device_readings(device_id, 24)
                end_time = time.time()
                query_duration = end_time - start_time
                
                self.log_test("数据查询性能", query_duration < 1, f"查询{len(readings)}条记录耗时{query_duration:.3f}秒")
            
        except Exception as e:
            self.log_test("系统性能", False, str(e))
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n=== 测试错误处理 ===")
        
        try:
            # 测试无效设备ID
            device = self.ems.find_device_by_id("INVALID_ID")
            self.log_test("无效设备ID处理", device is None, "正确返回None")
            
            # 测试无效数据记录
            success, msg = self.ems.record_energy_reading("INVALID_ID", 220, 5, 1100, 25, 60)
            self.log_test("无效数据记录处理", not success, "正确拒绝无效数据")
            
            # 测试重复设备注册
            device_id, msg1 = self.ems.register_device("重复设备", "Test", "位置", 1000)
            device_id2, msg2 = self.ems.register_device("重复设备", "Test", "位置", 1000)
            
            # 应该允许重复名称但生成不同ID
            self.log_test("重复设备处理", device_id != device_id2, "正确处理重复设备名称")
            
        except Exception as e:
            self.log_test("错误处理", False, str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("           智能能耗管理系统综合测试")
        print("=" * 60)
        print(f"测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 运行各项测试
        self.test_data_persistence()
        self.test_device_management()
        self.test_energy_monitoring()
        self.test_energy_analysis()
        self.test_recommendations()
        self.test_cost_calculation()
        self.test_report_generation()
        self.test_performance()
        self.test_error_handling()
        
        # 输出测试结果
        print("\n" + "=" * 60)
        print("                测试结果汇总")
        print("=" * 60)
        
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {self.passed_tests}")
        print(f"失败测试: {self.failed_tests}")
        print(f"通过率: {pass_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if "[FAIL]" in result:
                    print(f"  {result}")
        
        print(f"\n测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return self.failed_tests == 0


def main():
    """主函数"""
    tester = SystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✓ 所有测试通过！系统运行正常。")
        return 0
    else:
        print("\n✗ 部分测试失败，请检查系统。")
        return 1


if __name__ == "__main__":
    sys.exit(main())

