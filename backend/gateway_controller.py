import subprocess
import time
import sys
from typing import Tuple


class GatewayController:
    """OpenClaw Gateway 服务控制器"""

    @staticmethod
    def _execute_command(command: str) -> Tuple[bool, str]:
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _log(msg: str):
        """输出日志到终端"""
        print(f"[GatewayController] {msg}", flush=True)
        sys.stdout.flush()

    @staticmethod
    def stop_gateway() -> Tuple[bool, str]:
        """停止 OpenClaw Gateway"""
        GatewayController._log("Stopping Gateway...")
        # 使用 taskkill 强制终止进程
        success, output = GatewayController._execute_command("taskkill /F /IM openclaw.exe 2>nul")
        if success or "not found" in output.lower():
            GatewayController._log("Gateway stopped")
            return True, "Gateway stopped"
        return success, output

    @staticmethod
    def start_gateway() -> Tuple[bool, str]:
        """启动 OpenClaw Gateway"""
        GatewayController._log("Starting Gateway...")

        # gateway.cmd 的路径
        gateway_cmd = r"C:\Users\Administrator\.openclaw\gateway.cmd"

        try:
            # 隐藏窗口启动
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.Popen(
                f'"{gateway_cmd}"',
                shell=True,
                startupinfo=startupinfo,
                cwd=r"C:\Users\Administrator\.openclaw"
            )
            GatewayController._log("Gateway started in new window")
            return True, "Gateway 服务已启动"
        except Exception as e:
            GatewayController._log(f"Failed to start Gateway: {e}")
            return False, str(e)

    @staticmethod
    def restart_gateway() -> Tuple[bool, str]:
        """重启 OpenClaw Gateway"""
        GatewayController._log("=== Restarting Gateway ===")

        # Step 1: 停止
        GatewayController._log("Step 1: Stopping...")
        GatewayController.stop_gateway()
        time.sleep(1)

        # Step 2: 启动
        GatewayController._log("Step 2: Starting...")
        return GatewayController.start_gateway()

    @staticmethod
    def control_gateway(action: str) -> Tuple[bool, str]:
        """控制 Gateway 服务"""
        GatewayController._log(f"Control action: {action}")
        action_map = {
            'stop': GatewayController.stop_gateway,
            'start': GatewayController.start_gateway,
            'restart': GatewayController.restart_gateway
        }
        handler = action_map.get(action.lower())
        if not handler:
            return False, f"未知的操作: {action}"
        return handler()


if __name__ == "__main__":
    # 测试用
    print("Testing Gateway Controller...")
    success, msg = GatewayController.restart_gateway()
    print(f"Result: success={success}, message={msg}")
