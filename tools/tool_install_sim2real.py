# -*- coding: utf-8 -*-
import os
import sys
import getpass
import subprocess
from pwd import getpwnam

# 如果存在相对导入的问题，请修改为绝对导入或调整 sys.path
try:
    from .base import BaseTool
    from .base import PrintUtils, CmdTask
except ImportError:
    # 调整 sys.path，确保可以导入 base 模块
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from base import BaseTool
    from base import PrintUtils, CmdTask

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_INSTALL
        self.name = "更新并编译 sim2real_master 工程（指定标签版本）"
        self.author = 'yt_w'

    def install_code(self):
        # ========= 配置部分，请根据需要修改 =========
        REPO_BASE_URL = "https://github.com/HighTorque-Locomotion"
        REPO_DIR_NAME = "sim2real_master"
        REPO_NAME_PI = "sim2real_master"
        REPO_NAME_HI = "sim2real_master"
        ROS_DISTRO = "noetic"  # 根据您的 ROS 版本修改，例如 "melodic"、"noetic" 等

        # ========= 开始执行步骤 =========
        # 1. 检测当前用户是否为 root
        if os.geteuid() == 0:
            # 获取目标普通用户名
            target_user = os.getenv('SUDO_USER')
            if not target_user:
                PrintUtils.print_error("无法获取普通用户用户名，请以普通用户身份运行脚本。")
                return
            else:
                PrintUtils.print_info(f"检测到当前用户为 root，将以普通用户 {target_user} 的身份重新执行脚本。")
                python_executable = sys.executable
                script_path = os.path.abspath(__file__)
                args = [script_path] + sys.argv[1:]
                subprocess.run(['sudo', '-u', target_user, python_executable] + args)
                sys.exit(0)
        else:
            target_user = getpass.getuser()
            PrintUtils.print_info(f"当前用户：{target_user}")

        # 获取目标用户的主目录
        try:
            target_user_info = getpwnam(target_user)
            HOME_DIR = target_user_info.pw_dir
            PrintUtils.print_info(f"目标用户的主目录：{HOME_DIR}")
        except KeyError:
            PrintUtils.print_error(f"无法获取用户 {target_user} 的主目录。")
            return

        LOCAL_DIR = os.path.join(HOME_DIR, REPO_DIR_NAME)

        # 2. 检查本地仓库是否存在
        if os.path.exists(LOCAL_DIR):
            PrintUtils.print_info("发现本地仓库 {}，开始更新...".format(LOCAL_DIR))
            # 进入仓库目录
            os.chdir(LOCAL_DIR)
            # 拉取最新的代码
            subprocess.run("git fetch", shell=True)
        else:
            # 仓库不存在，进行克隆
            PrintUtils.print_info("本地仓库不存在，需要克隆仓库。")
            # 要求用户输入机器人类型
            robot_type = None
            while robot_type not in ['1', '2']:
                print("\n请选择机器人类型：")
                print("1. pi 1")
                print("2. hi 2")
                robot_type = input("请输入数字 1 或 2，然后按回车键确认：")
                if robot_type not in ['1', '2']:
                    PrintUtils.print_error("输入无效，请输入数字 1 或 2。")
            PrintUtils.print_info("您选择了机器人类型 {}。".format(robot_type))

            # 根据机器人类型设置仓库名
            if robot_type == '1':
                REPO_NAME = REPO_NAME_PI
            else:
                REPO_NAME = REPO_NAME_HI

            REPO_URL = "{}/{}.git".format(REPO_BASE_URL, REPO_NAME)

            # 克隆仓库
            clone_command = "git clone {} {}".format(REPO_URL, LOCAL_DIR)
            clone_process = subprocess.run(clone_command, shell=True)
            if clone_process.returncode != 0:
                PrintUtils.print_error("克隆仓库失败，请检查网络连接和仓库访问权限。")
                return
            PrintUtils.print_info("仓库已克隆至 {}。".format(LOCAL_DIR))
            os.chdir(LOCAL_DIR)

        # 3. 获取可用的标签列表
        PrintUtils.print_info("获取可用的标签列表...")
        fetch_tags_cmd = "git fetch --tags"
        subprocess.run(fetch_tags_cmd, shell=True)
        tag_list_cmd = "git tag"
        result = subprocess.run(tag_list_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            tags = result.stdout.strip().split('\n')
            if not tags:
                PrintUtils.print_error("未找到任何标签，请检查仓库是否包含标签。")
                return
            else:
                PrintUtils.print_info("可用的标签列表：")
                for idx, tag in enumerate(tags):
                    print(f"{idx + 1}. {tag}")
                # 让用户选择标签
                selected_tag = None
                while selected_tag is None:
                    user_input = input("请输入要切换到的标签编号或名称，然后按回车键确认：").strip()
                    if user_input.isdigit():
                        idx = int(user_input) - 1
                        if 0 <= idx < len(tags):
                            selected_tag = tags[idx]
                        else:
                            PrintUtils.print_error("输入的编号超出范围，请重新输入。")
                    else:
                        if user_input in tags:
                            selected_tag = user_input
                        else:
                            PrintUtils.print_error("输入的标签名称不存在，请重新输入。")
                PrintUtils.print_info(f"您选择了标签：{selected_tag}")
                # 切换到选定的标签
                checkout_cmd = "git checkout {}".format(selected_tag)
                checkout_process = subprocess.run(checkout_cmd, shell=True)
                if checkout_process.returncode != 0:
                    PrintUtils.print_error(f"切换到标签 {selected_tag} 失败。")
                    return
                else:
                    PrintUtils.print_info(f"已切换到标签 {selected_tag}。")
        else:
            PrintUtils.print_error("获取标签列表失败，请检查网络连接和仓库访问权限。")
            return

        # 4. 编译工程
        PrintUtils.print_info("开始编译工程...")
        os.chdir(LOCAL_DIR)
        # 检查并加载 ROS 环境
        ros_setup = "/opt/ros/{}/setup.bash".format(ROS_DISTRO)
        if not os.path.exists(ros_setup):
            PrintUtils.print_error("找不到 ROS 环境设置文件 {}，请检查 ROS 是否正确安装。".format(ros_setup))
            return
        # 构建编译命令，确保加载 ROS 环境
        build_command = "source {} && catkin build".format(ros_setup)
        build_process = subprocess.run(build_command, shell=True, executable='/bin/bash')
        if build_process.returncode != 0:
            PrintUtils.print_error("编译失败，请检查编译输出以获取详细信息。")
            return
        PrintUtils.print_info("工程已成功编译。")

        # 5. 提示完成
        PrintUtils.print_info("sim2real_master 工程已更新并编译完成（标签版本：{}）。".format(selected_tag))

    def run(self):
        self.install_code()
