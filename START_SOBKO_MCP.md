# Sobko MCP 启动指令

进入项目目录：

```bash
cd /home/axie/Sobko_MCP_project
```

## 推荐：启动共享 BGE-M3 embedding daemon

直接复制整段：

```bash
cd /home/axie/Sobko_MCP_project
mkdir -p .omx/logs .omx/state
if ! curl -sf http://127.0.0.1:8769/health >/dev/null 2>&1; then
  setsid python scripts/run_embedding_daemon.py > .omx/logs/sobko-embedding-daemon.log 2>&1 < /dev/null &
  echo $! > .omx/state/sobko-embedding-daemon.pid
  sleep 3
fi
curl -s http://127.0.0.1:8769/health
```

然后重启 Codex / Claude 会话，它们会自动启动 `sobko-kb` MCP，并优先调用这个共享 daemon。

## 一键脚本版

```bash
cd /home/axie/Sobko_MCP_project
bash scripts/start_sobko_embedding_daemon.sh
```

## 查看日志

```bash
cd /home/axie/Sobko_MCP_project
tail -f .omx/logs/sobko-embedding-daemon.log
```

## 停止 daemon

```bash
cd /home/axie/Sobko_MCP_project
kill $(cat .omx/state/sobko-embedding-daemon.pid)
```

## 日常怎么问

```text
用 Sobko 查一下：Gaussian 频率分析出现虚频怎么办？
```

```text
查 Sobko top 5，并展开最相关上下文：ORCA TDDFT 空穴电子分析 Multiwfn
```
