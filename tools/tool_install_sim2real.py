# -*- coding: utf-8 -*-
import os
import getpass
import subprocess
from .base import BaseTool
from .base import PrintUtils, CmdTask

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_INSTALL
        self.name = "更新并编译 sim2real_master 工程（最新标签）"
        self.author = 'yt_w'

    def run(self):
        # 正式的运行
        # ========= 配置部分，请根据需要修改 =========
        REPO_URL = "git@github.com:HighTorque-Locomotion/sim2real_master.git"  # 仓库的 SSH 地址
        REPO_BASE_URL = "git@github.com:HighTorque-Locomotion"
        REPO_DIR_NAME = "sim2real_master"
        REPO_NAME_pi = "sim2real_master"
        REPO_NAME_hi = "sim2real_master"
        HOME_DIR = os.path.expanduser("~")
        LOCAL_DIR = os.path.join(HOME_DIR, REPO_DIR_NAME)
        ROS_DISTRO = "noetic"  # 根据您的 ROS 版本修改，例如 "melodic"、"noetic" 等

        # ========= 开始执行步骤 =========
        # 1. 检查是否以 root 用户身份运行脚本
        current_user = getpass.getuser()
        if current_user == 'root':
            PrintUtils.print_error("请不要以 root 用户身份运行此脚本。")
            return
        else:
            PrintUtils.print_info("当前用户：{}".format(current_user))

        # 检查 SSH_AUTH_SOCK
        ssh_auth_sock = os.environ.get('SSH_AUTH_SOCK')
        if not ssh_auth_sock:
            PrintUtils.print_error("SSH_AUTH_SOCK 未设置，可能无法访问 SSH 代理。")
            return
        else:
            PrintUtils.print_info("SSH_AUTH_SOCK: {}".format(ssh_auth_sock))

        # 2. 检查本地仓库是否存在
        if os.path.exists(LOCAL_DIR):
            PrintUtils.print_info("发现本地仓库 {}，开始更新...".format(LOCAL_DIR))
            # 进入仓库目录
            os.chdir(LOCAL_DIR)
            # 获取最新的标签
            PrintUtils.print_info("获取最新的标签...")
            fetch_tags_cmd = "git fetch --tags"
            subprocess.run(fetch_tags_cmd, shell=True)
            latest_tag_cmd = "git describe --tags `git rev-list --tags --max-count=1`"
            result = subprocess.run(latest_tag_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                latest_tag = result.stdout.strip()
                PrintUtils.print_info("最新的标签是：{}".format(latest_tag))
                # 检查当前是否已经在最新的标签上
                current_tag_cmd = "git describe --tags"
                current_tag_result = subprocess.run(current_tag_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if current_tag_result.returncode == 0:
                    current_tag = current_tag_result.stdout.strip()
                    if current_tag != latest_tag:
                        # 切换到最新的标签
                        checkout_cmd = "git checkout {}".format(latest_tag)
                        checkout_process = subprocess.run(checkout_cmd, shell=True)
                        if checkout_process.returncode != 0:
                            PrintUtils.print_error("切换到最新标签 {} 失败。".format(latest_tag))
                            return
                        else:
                            PrintUtils.print_info("已切换到最新标签 {}。".format(latest_tag))
                    else:
                        PrintUtils.print_info("当前已经是最新的标签 {}。".format(current_tag))
                else:
                    # 当前不是在标签上，切换到最新标签
                    checkout_cmd = "git checkout {}".format(latest_tag)
                    checkout_process = subprocess.run(checkout_cmd, shell=True)
                    if checkout_process.returncode != 0:
                        PrintUtils.print_error("切换到最新标签 {} 失败。".format(latest_tag))
                        return
                    else:
                        PrintUtils.print_info("已切换到最新标签 {}。".format(latest_tag))
            else:
                PrintUtils.print_error("获取最新标签失败，请检查网络连接和仓库访问权限。")
                return
        else:
            # 仓库不存在，进行克隆
            PrintUtils.print_info("本地仓库不存在，开始克隆...")
            # 仓库不存在，要求用户输入机器人类型
            PrintUtils.print_info("本地仓库不存在，需要克隆仓库。")
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
                REPO_NAME = REPO_NAME_pi 
            else:
                REPO_NAME = REPO_NAME_hi  

            REPO_URL = "{}/{}.git".format(REPO_BASE_URL, REPO_NAME)

            # 克隆仓库
            clone_command = "git clone {} {}".format(REPO_URL, LOCAL_DIR)
            clone_process = subprocess.run(clone_command, shell=True)
            if clone_process.returncode != 0:
                PrintUtils.print_error("克隆仓库失败，请检查网络连接和仓库访问权限。")
                return
            PrintUtils.print_info("仓库已克隆至 {}。".format(LOCAL_DIR))
            os.chdir(LOCAL_DIR)
            # 获取最新的标签
            PrintUtils.print_info("获取最新的标签...")
            fetch_tags_cmd = "git fetch --tags"
            subprocess.run(fetch_tags_cmd, shell=True)
            latest_tag_cmd = "git describe --tags `git rev-list --tags --max-count=1`"
            result = subprocess.run(latest_tag_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                latest_tag = result.stdout.strip()
                PrintUtils.print_info("最新的标签是：{}".format(latest_tag))
                # 切换到最新的标签
                checkout_cmd = "git checkout {}".format(latest_tag)
                checkout_process = subprocess.run(checkout_cmd, shell=True)
                if checkout_process.returncode != 0:
                    PrintUtils.print_error("切换到最新标签 {} 失败。".format(latest_tag))
                    return
                else:
                    PrintUtils.print_info("已切换到最新标签 {}。".format(latest_tag))
            else:
                PrintUtils.print_error("获取最新标签失败，请检查网络连接和仓库访问权限。")
                return

        # 3. 编译工程
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

        # 4. 提示完成
        PrintUtils.print_info("sim2real_master 工程已更新并编译完成（最新标签版本）。")
