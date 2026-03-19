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
        success, output = GatewayController._execute_command("openclaw gateway stop")
        if success:
            GatewayController._log("Gateway stopped successfully")
        else:
            GatewayController._log(f"Failed to stop Gateway: {output}")
        return success, output

    @staticmethod
    def start_gateway() -> Tuple[bool, str]:
        """启动 OpenClaw Gateway"""
        GatewayController._log("Starting Gateway...")
        success, output = GatewayController._execute_command("openclaw gateway")
        if success:
            GatewayController._log("Gateway started successfully")
        else:
            GatewayController._log(f"Failed to start Gateway: {output}")
        return success, output

    @staticmethod
    def restart_gateway() -> Tuple[bool, str]:
        """重启 OpenClaw Gateway"""
        GatewayController._log("Restarting Gateway...")
        # 先停止
        success, output = GatewayController.stop_gateway()
        if not success:
            GatewayController._log(f"Stop failed: {output}")
            return False, f"停止失败: {output}"

        # 等待2秒
        GatewayController._log("Waiting 2 seconds...")
        time.sleep(2)

        # 再启动
        result = GatewayController.start_gateway()
        GatewayController._log(f"Restart complete: success={result[0]}, message={result[1]}")
        return result

    @staticmethod
    def control_gateway(action: str) -> Tuple[bool, str]:
        """控制 Gateway 服务"""
        GatewayController._log(f"Control action received: {action}")
        action_map = {
            'stop': GatewayController.stop_gateway,
            'start': GatewayController.start_gateway,
            'restart': GatewayController.restart_gateway
        }

        handler = action_map.get(action.lower())
        if not handler:
            GatewayController._log(f"Unknown action: {action}")
            return False, f"未知的操作: {action}"

        return handler()
