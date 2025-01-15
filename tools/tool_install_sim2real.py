# -*- coding: utf-8 -*-
import os
import getpass
import subprocess
from .base import BaseTool
from .base import PrintUtils, CmdTask

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_INSTALL
        self.name = "更新并编译 sim2real_master 工程"
        self.author = '小鱼'

    def run(self):
        # 正式的运行
        # ========= 配置部分，请根据需要修改 =========
        REPO_URL = "git@github.com:HighTorque-Locomotion/sim2real_master.git"  # 仓库的 SSH 地址
        REPO_BRANCH = "main"  # 要拉取的分支名称
        REPO_DIR_NAME = "sim2real_master"
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

        # 2. 检查本地仓库是否存在
        if os.path.exists(LOCAL_DIR):
            PrintUtils.print_info("发现本地仓库 {}，开始更新...".format(LOCAL_DIR))
            # 进入仓库目录
            os.chdir(LOCAL_DIR)
            # 检查当前分支是否与需要的分支一致，如果不一致，切换分支
            cmd_current_branch = "git rev-parse --abbrev-ref HEAD"
            result = subprocess.run(cmd_current_branch, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                current_branch = result.stdout.strip()
                if current_branch != REPO_BRANCH:
                    cmd_checkout_branch = "git checkout {}".format(REPO_BRANCH)
                    checkout_process = subprocess.run(cmd_checkout_branch, shell=True)
                    if checkout_process.returncode != 0:
                        PrintUtils.print_error("切换到分支 {} 失败。".format(REPO_BRANCH))
                        return
            else:
                PrintUtils.print_error("获取当前分支失败，无法更新仓库。")
                return
            # 拉取最新代码
            cmd_git_pull = "git pull origin {}".format(REPO_BRANCH)
            pull_process = subprocess.run(cmd_git_pull, shell=True)
            if pull_process.returncode != 0:
                PrintUtils.print_error("更新仓库失败，请检查网络连接和仓库访问权限。")
                return
            PrintUtils.print_info("仓库已更新。")
        else:
            # 仓库不存在，进行克隆
            PrintUtils.print_info("本地仓库不存在，开始克隆...")
            clone_command = "git clone -b {} {} {}".format(REPO_BRANCH, REPO_URL, LOCAL_DIR)
            clone_process = subprocess.run(clone_command, shell=True)
            if clone_process.returncode != 0:
                PrintUtils.print_error("克隆仓库失败，请检查网络连接和仓库访问权限。")
                return
            PrintUtils.print_info("仓库已克隆至 {}。".format(LOCAL_DIR))

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
        PrintUtils.print_info("sim2real_master 工程已更新并编译完成。")
