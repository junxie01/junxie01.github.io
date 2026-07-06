#!/usr/bin/env python3
"""
自动设置每日工作日报为桌面背景的脚本
适用于 macOS 系统
"""

import os
import subprocess
import datetime
from pathlib import Path

def set_desktop_background(image_path):
    """
    设置指定的图片为桌面背景
    
    Args:
        image_path (str): 图片的完整路径
    """
    if not os.path.exists(image_path):
        print(f"错误：图片文件不存在 - {image_path}")
        return False
    
    try:
        # 使用 AppleScript 设置桌面背景
        applescript = f'''
        tell application "Finder"
            set desktop picture to POSIX file "{image_path}"
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ 已成功设置桌面背景: {image_path}")
            return True
        else:
            print(f"✗ 设置桌面背景失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ 执行脚本时出错: {str(e)}")
        return False

def get_today_image_path():
    """
    获取今天的图片路径
    假设图片保存在 ~/Pictures/ 目录下，格式为 YYYY-MM-DD_*.png
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    pictures_dir = os.path.expanduser("~/Pictures")
    
    # 查找今天的图片
    for file in os.listdir(pictures_dir):
        if file.startswith(today) and file.endswith('.png'):
            return os.path.join(pictures_dir, file)
    
    # 如果没有今天的图片，尝试查找最近的一张
    print(f"⚠️ 未找到今天的图片 ({today})，尝试查找最近的图片...")
    
    png_files = []
    for file in os.listdir(pictures_dir):
        if file.endswith('.png'):
            try:
                # 尝试从文件名中提取日期
                date_str = file.split('_')[0]
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                png_files.append((date_str, os.path.join(pictures_dir, file)))
            except:
                continue
    
    if png_files:
        # 按日期排序，选择最新的
        png_files.sort(reverse=True)
        return png_files[0][1]
    
    print("✗ 未找到任何合适的图片文件")
    return None

def main():
    """主函数"""
    print("=" * 50)
    print("工作日报桌面背景设置工具")
    print("=" * 50)
    
    # 方法1：使用今天的图片
    image_path = get_today_image_path()
    
    if image_path:
        success = set_desktop_background(image_path)
        if success:
            print("\n✅ 桌面背景已成功更新！")
            print(f"   使用的图片: {os.path.basename(image_path)}")
            print(f"   图片路径: {image_path}")
        else:
            print("\n❌ 设置桌面背景失败")
    else:
        # 方法2：让用户手动指定图片
        print("\n请手动指定图片路径:")
        user_path = input("请输入图片完整路径: ").strip()
        
        if user_path and os.path.exists(user_path):
            success = set_desktop_background(user_path)
            if success:
                print("\n✅ 桌面背景已成功更新！")
            else:
                print("\n❌ 设置桌面背景失败")
        else:
            print("✗ 无效的图片路径")

if __name__ == "__main__":
    main()
