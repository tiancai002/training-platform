#!/bin/bash
# 后端进程监控脚本
# 每 30 秒检查一次，如果后端挂了自动重启

LOG_FILE="/var/www/training-platform/logs/monitor.log"
BACKEND_DIR="/var/www/training-platform/backend/backend"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== 后端监控启动 ==="

while true; do
    # 检查后端进程
    UVICORN_COUNT=$(ps aux | grep "[u]vicorn" | wc -l)
    
    if [ "$UVICORN_COUNT" -lt 2 ]; then
        log "⚠️  检测到后端进程异常 (当前：$UVICORN_COUNT 个)"
        log "🔄 正在重启后端..."
        
        # 杀掉残留进程
        pkill -9 -f uvicorn 2>/dev/null
        sleep 2
        
        # 启动新进程
        cd "$BACKEND_DIR"
        nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 > /var/www/training-platform/logs/backend.log 2>&1 &
        
        sleep 5
        
        # 验证启动
        NEW_COUNT=$(ps aux | grep "[u]vicorn" | wc -l)
        if [ "$NEW_COUNT" -ge 2 ]; then
            log "✅ 后端重启成功 ($NEW_COUNT 个进程)"
        else
            log "❌ 后端重启失败"
        fi
    else
        # 检查健康状态
        HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
        if echo "$HEALTH" | grep -q "healthy"; then
            log "✅ 后端正常 ($UVICORN_COUNT 个进程)"
        else
            log "⚠️  健康检查失败：$HEALTH"
        fi
    fi
    
    sleep 30
done
