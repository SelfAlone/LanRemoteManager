import subprocess
import os
import ctypes
import sys
import time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def install_cert(cert_path):
    if not os.path.exists(cert_path):
        raise FileNotFoundError(f"证书文件未找到: {cert_path}")

    command = ['certutil', '-addstore', 'Root', cert_path]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"证书安装失败: {result.stderr}")
    print("证书安装成功")


def install_driver(inf_path):
    if not os.path.exists(inf_path):
        raise FileNotFoundError(f"驱动文件未找到: {inf_path}")

    # 安装驱动到驱动存储区
    install_cmd = ['pnputil', '/add-driver', inf_path, '/install']
    result = subprocess.run(install_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"驱动安装失败: {result.stderr}")
    print("驱动安装成功")


driver_path = ".\\IddSampleDriver\\IddSampleDriver\\IddSampleDriver.inf"
cert_path = ".\\IddSampleDriver\\IddSampleDriver.cer"
try:
    if not is_admin():
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    else:
        install_cert(cert_path)
        install_driver(driver_path)
except Exception as e:
    print(f"错误: {str(e)}")
    time.sleep(10)
