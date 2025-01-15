# -*- coding: utf-8 -*-
from .base import BaseTool
from .base import PrintUtils, CmdTask, FileUtils, AptUtils, ChooseTask
from .base import osversion
from .base import run_tool_file
import os

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_INSTALL
        self.name = "高扭矩 PI RL 工作空间部署和编译"
        self.author = 'yt_w'

    def run(self):
        PrintUtils.print_info("开始运行了 aaaaaaaaa")
        # 正式的运行
        SWAP_SIZE = "10G"
        SWAP_FILE = "/swapfile"

        # 检查是否存在 swap 文件
        if not os.path.exists(SWAP_FILE):
            PrintUtils.print_info("创建 swap 文件：{}，大小：{} ...".format(SWAP_FILE, SWAP_SIZE))
            CmdTask("sudo fallocate -l {} {}".format(SWAP_SIZE, SWAP_FILE)).run()
            CmdTask("sudo chmod 600 {}".format(SWAP_FILE)).run()
            CmdTask("sudo mkswap {}".format(SWAP_FILE)).run()
            CmdTask("sudo swapon {}".format(SWAP_FILE)).run()
            PrintUtils.print_info("Swap 已启用，当前可用内存：")
            CmdTask("free -h").run()
        else:
            PrintUtils.print_info("检测到 {} 已经作为 swap 启用，跳过创建。".format(SWAP_FILE))

        # ========= 配置部分，根据需要修改 =========
        ROS_DISTRO = "noetic"  # ROS 发行版，如 melodic, noetic 等
        WORKSPACE_NAME = "hightorque_pi_rl"  # 工作空间名称
        SOURCE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", WORKSPACE_NAME))
        TARGET_DIR = "/opt/{}".format(WORKSPACE_NAME)

        # ========= 开始安装流程 =========
        # 0. 检查源目录是否存在
        # if not os.path.isdir(SOURCE_DIR):
        #     PrintUtils.print_error("在当前目录下找不到 {} 文件夹，请确保脚本与工作空间在同级目录。".format(WORKSPACE_NAME))
        #     return

        # 1. 如果 /opt 下已有 hightorque_pi_rl，先删除
        if os.path.isdir(TARGET_DIR):
            PrintUtils.print_info("检测到 {} 已存在，执行替换操作...".format(TARGET_DIR))
            CmdTask("sudo rm -rf {}".format(TARGET_DIR)).run()

        # 2. 复制新的工作空间到 /opt
        PrintUtils.print_info("复制 {} 到 /opt 目录...".format(WORKSPACE_NAME))
        # CmdTask("git clone -b joy_teleop_control git@github.com:HighTorque-Locomotion/sim2real_master.git && sudo mv ~/intall/sim2real_master /opt/").run()
        clone_command = "git clone -b joy_teleop_control git@github.com:HighTorque-Locomotion/sim2real_master.git && sudo mv ~/intall/sim2real_master /opt/"
        clone_return_code = CmdTask(clone_command).run()

        if clone_return_code != 0:
            PrintUtils.print_error("克隆仓库失败，请检查网络连接和仓库访问权限。")
            return
        PrintUtils.print_info("复制完成。")

        # # 3. 检查并加载 ROS 环境
        # ros_setup = "/opt/ros/{}/setup.bash".format(ROS_DISTRO)
        # if not os.path.exists(ros_setup):
        #     PrintUtils.print_error("找不到 {}，请检查 ROS 是否正确安装。".format(ros_setup))
        #     return

        # # 4. 切换到工作空间并执行 catkin build
        # PrintUtils.print_info("开始编译 {} 工作空间...".format(WORKSPACE_NAME))
        # # 构建编译命令，确保加载 ROS 环境
        # build_command = "cd {} && source {} && catkin build".format(TARGET_DIR, ros_setup)
        # CmdTask(build_command, use_bash=True).run()

        # # 5. 提示完成
        # PrintUtils.print_info("{} 已安装/更新至 {} 并成功编译。".format(WORKSPACE_NAME, TARGET_DIR))

        # 询问是否重启
        answer = input("输入 y 或 Y 确认重启，或按其他任意键取消: ")
        if answer.lower() == 'y':
            PrintUtils.print_info("系统即将重启...")
            CmdTask("sudo reboot").run()
        else:
            PrintUtils.print_info("已取消重启。脚本执行结束。")
