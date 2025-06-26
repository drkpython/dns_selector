import subprocess
import time
from ping3 import ping
import ctypes
import sys

# 常见的DNS服务器
dns_servers = [
    "8.8.8.8",  # Google DNS
    "8.8.4.4",  # Google DNS
    "1.1.1.1",  # Cloudflare DNS
    "1.0.0.1",  # Cloudflare DNS
    "208.67.222.222",  # OpenDNS
    "208.67.220.220",  # OpenDNS
]


def ping_dns(dns):
    """Ping DNS服务器并返回响应时间"""
    try:
        response_time = ping(dns, timeout=2)  # 超过2秒的响应时间会认为是不可达
        if response_time is None:
            return float('inf')  # 如果没有响应，返回最大时间
        return response_time
    except Exception as e:
        print(f"Ping error: {e}")
        return float('inf')  # 出现异常时返回最大时间


def get_best_dns(dns_servers):
    """返回响应时间最短的DNS服务器"""
    best_dns = None
    best_time = float('inf')

    for dns in dns_servers:
        response_time = ping_dns(dns)
        print(f"DNS: {dns}, Response time: {response_time:.2f} ms")

        if response_time < best_time:
            best_time = response_time
            best_dns = dns

    return best_dns


def set_dns(dns):
    """应用DNS配置到Windows"""
    try:
        # 修改为正确的网络接口名称：WLAN
        subprocess.run(
            ["netsh", "interface", "ipv4", "set", "dnsservers", "name=WLAN", f"source=static", f"address={dns}"],
            check=True)
        print(f"DNS has been set to {dns}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set DNS: {e}")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    # 如果不是管理员，重新运行脚本并请求管理员权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

if __name__ == "__main__":
    # 提示用户确认是否继续执行
    input("DR.K DNSelector即将开始DNS服务器配置，按下 Enter 键继续...")

    print("Starting DNS selection process...")
    best_dns = get_best_dns(dns_servers)
    if best_dns:
        print(f"Best DNS is {best_dns}. Applying configuration...")
        set_dns(best_dns)
    else:
        print("No suitable DNS found.")

    # 按任意键退出
    input("DNS修改完成，按任意键退出...")