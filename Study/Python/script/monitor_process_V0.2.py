# -*- coding: utf-8 -*-
r"""
监控指定进程的 CPU、GPU（若可用）和内存占用，并每秒写入 Excel 文件。
- 列: 时间, CPU(%), GPU 内存(MB 或 N/A), GPU 使用率(% 或 N/A), 内存(MB)
- Excel 文件命名: <YYYYmmdd_HHMMSS>_<process_name>_<pid>.xlsx

说明:
- 需要第三方库: psutil, openpyxl
  可通过: pip install psutil openpyxl
- Windows 下：GPU 使用率通过 PowerShell 性能计数器获取；如果可用，则尝试使用 nvidia-smi 获取 NVIDIA 进程显存。
- macOS 下：仅记录进程 CPU/内存占用，GPU 数据默认写入 "N/A"。
- 如果系统不支持，相关 GPU 列将写入 "N/A"。

运行方式:
    python monitor_process.py

"""
import os
import sys
import time
import shutil
import subprocess
import re
import json
from datetime import datetime

try:
    import psutil
except ImportError:
    print("缺少依赖: psutil。请运行: pip install psutil")
    sys.exit(1)

try:
    from openpyxl import Workbook
except ImportError:
    print("缺少依赖: openpyxl。请运行: pip install openpyxl")
    sys.exit(1)


DATA_DIR = os.path.join(os.path.dirname(__file__))
IS_WINDOWS = sys.platform.startswith('win')
IS_MAC = sys.platform == 'darwin'
PLATFORM_NAME = 'Windows' if IS_WINDOWS else 'macOS' if IS_MAC else sys.platform


def sanitize_filename(name: str) -> str:
    # 移除或替换文件名中的非法字符
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        name = name.replace(ch, '_')
    return name


def list_processes(limit=2000):
    procs = []
    for p in psutil.process_iter(['pid', 'name']):
        try:
            info = p.info
            procs.append((info['pid'], info.get('name') or ''))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs = sorted(procs, key=lambda x: (x[1].lower(), x[0]))
    if limit:
        return procs[:limit]
    return procs


def choose_process():
    procs = list_processes()
    print("当前运行进程（编号: pid - name）: \n")
    for idx, (pid, name) in enumerate(procs):
        print(f"{idx:3d}: {pid} - {name}")

    while True:
        sel = input('\n请输入要监控的进程编号(index)或 PID (输入 q 退出): ').strip()
        if not sel:
            continue
        if sel.lower() == 'q':
            print('已退出')
            sys.exit(0)
        # 尝试按 index 选择
        if sel.isdigit():
            val = int(sel)
            # 优先当作 index
            if 0 <= val < len(procs):
                pid = procs[val][0]
                return pid
            # 然后当作 pid
            try:
                pid = int(sel)
                if psutil.pid_exists(pid):
                    return pid
            except ValueError:
                pass
        print('无效的选择，请重试。')


def get_gpu_memory_for_pid(pid: int):
    """尝试使用 nvidia-smi 获取指定进程的 GPU 显存占用。
    通用 Windows PowerShell 无法可靠提供每进程显存，因此这里仅在 NVIDIA 工具可用时返回值。
    """
    if IS_MAC:
        return None
    try:
        cmd = ['nvidia-smi', '--query-compute-apps=pid,used_memory', '--format=csv,noheader,nounits']
        out = subprocess.check_output(cmd, text=True, encoding='utf-8', errors='replace', stderr=subprocess.DEVNULL, timeout=5)
        if os.environ.get('MONITOR_DEBUG') == '1':
            print('[MONITOR_DEBUG] nvidia-smi compute-apps output:\n' + (out or '<empty>'))
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 2:
                continue
            try:
                ppid = int(parts[0])
                mem_mb = float(parts[1])
            except ValueError:
                continue
            if ppid == pid:
                return mem_mb
    except Exception:
        pass

    try:
        cmd = ['nvidia-smi', 'pmon', '-c', '1']
        out = subprocess.check_output(cmd, text=True, encoding='utf-8', errors='replace', stderr=subprocess.DEVNULL, timeout=5)
        if os.environ.get('MONITOR_DEBUG') == '1':
            print('[MONITOR_DEBUG] nvidia-smi pmon output:\n' + (out or '<empty>'))
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            try:
                ppid = int(parts[1])
                mem_mb = float(parts[4])
            except ValueError:
                continue
            if ppid == pid:
                return mem_mb
    except Exception:
        pass

    return None


def get_gpu_stats_for_pid(pid: int):
    r"""
    使用 PowerShell 的 '\GPU Engine(*)\Utilization Percentage' 获取按进程 GPU 引擎利用率。
    通过 ConvertTo-Json 获取结构化数据，匹配实例名中包含 pid_xxx 的条目并累加 CookedValue。
    返回 (gpu_mem_mb_or_None, gpu_util_percent_or_None)。
    """
    if IS_MAC:
        return None, None
    try:
        gpu_mem = get_gpu_memory_for_pid(pid)
        ps_script = (
            r"$data = Get-Counter '\GPU Engine(*)\Utilization Percentage' -MaxSamples 1 | "
            r"Select -ExpandProperty CounterSamples | Select InstanceName, CookedValue; $data | ConvertTo-Json -Compress"
        )
        # 更兼容的调用：允许执行策略并以脚本块执行
        # 首先尝试直接捕获输出
        ps_cmd = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-NoProfile', '-Command', f"& {{ {ps_script} }}"]
        out = ''
        try:
            out = subprocess.check_output(ps_cmd, text=True, encoding='utf-8', errors='replace', stderr=subprocess.DEVNULL, timeout=5)
        except subprocess.TimeoutExpired:
            out = ''
        except Exception:
            out = ''

        # 如果直接调用没有输出，尝试更稳健的文件中转方式：写入临时 .ps1 脚本，让 PowerShell 将 JSON 写入临时文件，再读取该文件
        if not out.strip():
            import tempfile
            ps1_fd, ps1_path = tempfile.mkstemp(suffix='.ps1', text=True)
            os.close(ps1_fd)
            tmp_json_fd, tmp_json_path = tempfile.mkstemp(suffix='.json', text=True)
            os.close(tmp_json_fd)
            try:
                # 使用更明确的 PowerShell 内容，并把结果写到临时 JSON 文件（保证编码为 UTF8）
                ps1_content = (
                    "$ErrorActionPreference = 'Stop'\n"
                    f"$data = Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -MaxSamples 1 | Select -ExpandProperty CounterSamples | Select InstanceName, CookedValue\n"
                    f"if ($data -eq $null) {{ '' | Out-File -FilePath '{tmp_json_path.replace("'","''")}' -Encoding utf8 }} else {{ $data | ConvertTo-Json -Compress | Out-File -FilePath '{tmp_json_path.replace("'","''")}' -Encoding utf8 }}\n"
                )
                with open(ps1_path, 'w', encoding='utf-8') as f:
                    f.write(ps1_content)
                try:
                    subprocess.check_call(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-NoProfile', '-File', ps1_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
                    if os.path.exists(tmp_json_path):
                        with open(tmp_json_path, 'r', encoding='utf-8') as jf:
                            out = jf.read()
                except subprocess.TimeoutExpired:
                    out = ''
                except Exception:
                    out = ''
            finally:
                try:
                    os.remove(ps1_path)
                except Exception:
                    pass
                try:
                    os.remove(tmp_json_path)
                except Exception:
                    pass

        if os.environ.get('MONITOR_DEBUG') == '1':
            print('[MONITOR_DEBUG] PowerShell JSON output for get_gpu_stats_for_pid:\n' + (out or ''))

        try:
            parsed = json.loads(out) if out and out.strip() else None
        except Exception:
            parsed = None

        if isinstance(parsed, dict):
            items = [parsed]
        elif isinstance(parsed, list):
            items = parsed
        else:
            items = []

        pid_str = f'pid_{pid}'
        total_util = 0.0
        found = False
        for item in items:
            try:
                inst = (item.get('InstanceName') or '').strip().lower()
                val = float(item.get('CookedValue') or 0)
            except Exception:
                continue
            if pid_str in inst:
                total_util += val
                found = True

        gpu_util = total_util if found else None
        return gpu_mem, gpu_util
    except Exception:
        return None, None


def get_network_counters():
    try:
        return psutil.net_io_counters()
    except Exception:
        return None


def calc_network_download_speed(prev, current, elapsed):
    if prev is None or current is None or elapsed <= 0:
        return 0.0
    try:
        return max((current.bytes_recv - prev.bytes_recv) / elapsed / 1024.0, 0.0)
    except Exception:
        return 0.0


def monitor(pid: int, out_dir: str = DATA_DIR):
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print('指定的进程不存在。')
        return

    proc_name = proc.name()
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = sanitize_filename(proc_name)
    filename = f"{ts}_{safe_name}_{pid}.xlsx"
    filepath = os.path.join(out_dir, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = 'monitor'
    # 将 GPU Util 列改为 GPU 使用率（对应 perf counter 中的进程 GPU 引擎利用率）
    if IS_MAC:
        ws.append(['时间', 'CPU (%)', '网络下行 (KB/s)', '内存 (MB)'])
    else:
        ws.append(['时间', 'CPU (%)', 'GPU Mem (MB 或 N/A)', 'GPU 使用率 (%)', '网络下行 (KB/s)', '内存 (MB)'])
    wb.save(filepath)

    print(f'开始监控: {proc_name} (pid={pid}), 平台: {PLATFORM_NAME}, 输出: {filepath}')
    print('按 Ctrl+C 停止监控。')

    # 先初始化 cpu 统计
    try:
        proc.cpu_percent(interval=None)
    except Exception:
        pass

    last_gpu_mem = None
    last_net = get_network_counters()
    last_net_time = time.time()

    try:
        while True:
            loop_start = time.time()
            # 使用 psutil 的 cpu_percent 近似每秒采样 CPU 占用
            try:
                cpu = proc.cpu_percent(interval=None)
            except psutil.NoSuchProcess:
                print('监控的进程已退出。')
                break
            except Exception:
                cpu = 0.0

            # 内存
            try:
                mem = proc.memory_info().rss / (1024 * 1024)
            except Exception:
                mem = 0.0

            # GPU: 获取该进程的 GPU 内存和 GPU 利用率
            try:
                gpu_mem, gpu_util = get_gpu_stats_for_pid(pid)
            except Exception:
                gpu_mem, gpu_util = None, None

            if gpu_mem is not None:
                last_gpu_mem = gpu_mem
            else:
                gpu_mem = last_gpu_mem

            gpu_mem_val = round(gpu_mem, 2) if gpu_mem is not None else 'N/A'
            gpu_util_val = round(gpu_util, 2) if gpu_util is not None else 'N/A'

            current_time = time.time()
            current_net = get_network_counters()
            down_speed = calc_network_download_speed(last_net, current_net, current_time - last_net_time)
            if current_net is not None:
                last_net = current_net
                last_net_time = current_time

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if IS_MAC:
                ws.append([now, round(cpu, 2), round(down_speed, 2), round(mem, 2)])
            else:
                ws.append([now, round(cpu, 2), gpu_mem_val, gpu_util_val, round(down_speed, 2), round(mem, 2)])
            # 每次追加后保存文件，保证实时性
            try:
                wb.save(filepath)
            except Exception as e:
                print('保存 Excel 出错:', e)

            # 输出到控制台一行，方便查看
            if IS_MAC:
                print(f"{now} | CPU: {cpu:.2f}% | Down: {down_speed:.2f} KB/s | Mem: {mem:.2f} MB")
            else:
                print(
                    f"{now} | CPU: {cpu:.2f}% | GPU_mem: {gpu_mem_val} | "
                    f"GPU 使用率: {gpu_util_val} % | Down: {down_speed:.2f} KB/s | Mem: {mem:.2f} MB"
                )

            elapsed = time.time() - loop_start
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)
    except KeyboardInterrupt:
        print('\n已手动停止监控')
    finally:
        try:
            wb.save(filepath)
        except Exception:
            pass
        print('监控结束，文件保存在:', filepath)


def main():
    print(f'监控 {PLATFORM_NAME} 进程 CPU/GPU/内存（每秒采样）')
    pid = choose_process()
    monitor(pid)


if __name__ == '__main__':
    main()
