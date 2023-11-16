pids=$(pgrep -f "python app.py --env prod --http_port 8900")
# 计算进程数量
num_pids=$(echo "$pids" | wc -w)
if [ $num_pids -eq 0 ]; then
    echo "没有匹配的进程需要终止"
    nohup  python app.py --env prod --http_port 8900 > app.log 2>&1 &
    tail -f app.log
elif [ $num_pids -eq 1 ]; then
    # 只有一个匹配的进程，使用kill命令终止它
    echo "正在终止进程: $pids"
    kill $pids
    nohup  python app.py --env prod --http_port 8900 > app.log 2>&1 &
    tail -f app.log
else
    # 多个匹配的进程，报错
    echo "找到多个匹配的进程 ($num_pids 个)，请手动处理:"
    echo "$pids"
    exit 1
fi