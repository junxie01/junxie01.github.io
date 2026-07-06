#!/bin/bash
# 每日工作日报自动化脚本

# 配置
PICTURES_DIR="$HOME/Pictures"
LOG_FILE="$HOME/Library/Logs/daily_report.log"
DATE_TAG=$(date +"%Y-%m-%d")
TODAY_IMAGE="${PICTURES_DIR}/${DATE_TAG}_daily_report.png"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "开始执行每日工作日报自动化任务"

# 1. 检查是否已生成今天的图片
if [ -f "$TODAY_IMAGE" ]; then
    log "发现今天的图片: $TODAY_IMAGE"
else
    log "警告: 今天的图片尚未生成 ($TODAY_IMAGE)"
    log "提示: 请先生成今日的工作日报图片"
fi

# 2. 设置桌面背景
if [ -f "$TODAY_IMAGE" ]; then
    log "正在设置桌面背景..."
    
    # 使用 AppleScript 设置桌面背景
    osascript <<eof
    tell application "Finder"
        set desktop picture to POSIX file "$TODAY_IMAGE"
    end tell
EOF
    
    if [ $? -eq 0 ]; then
        log "✅ 桌面背景已成功设置为: $TODAY_IMAGE"
    else
        log "❌ 设置桌面背景失败"
    fi
fi

# 3. 显示通知 (macOS)
if [ -f "$TODAY_IMAGE" ]; then
    osascript <<EOF
    display notification "今日工作日报已设置为桌面背景" with title "工作日报" subtitle "日期: $DATE_TAG"
EOF
    log "已发送桌面通知"
fi

log "任务执行完成"
