# -*- coding: utf-8 -*-
import os
import importlib

url_prefix = os.environ.get('FISHROS_URL','https://raw.githubusercontent.com/wwwwwyt/intall/refs/heads/master')
base_url = os.path.join(url_prefix,'tools/base.py')
translator_url = os.path.join(url_prefix,'tools/translation/translator.py')

INSTALL_ROS = 0  # 安装ROS相关
INSTALL_SOFTWARE = 1  # 安装软件
CONFIG_TOOL = 2  # 配置相关
CODE_UPDATES = 3 # 代码相关

tools_type_map = {
    INSTALL_ROS: "ROS相关",
    INSTALL_SOFTWARE: "常用软件",
    CONFIG_TOOL: "配置工具",
    CODE_UPDATES: "代码相关"
}


tools ={
    1: {'tip':'一键更新：sim2real运控代码',                 'type':CODE_UPDATES,     'tool':'tools/tool_install_ros.py' ,'dep':[] },
    # 2: {'tip':'一键安装:github桌面版(小鱼常用的github客户端)',             'type':INSTALL_SOFTWARE,     'tool':'tools/tool_install_github_desktop.py' ,'dep':[] },
    # 3: {'tip':'一键安装:rosdep(小鱼的rosdepc,又快又好用)',                 'type':INSTALL_ROS,    'tool':'tools/tool_config_rosdep.py' ,'dep':[] },
    # 4: {'tip':'一键配置:ROS环境(快速更新ROS环境设置,自动生成环境选择)',     'type':INSTALL_ROS,     'tool':'tools/tool_config_rosenv.py' ,'dep':[] },
    # 5: {'tip':'一键配置:系统源(更换系统源,支持全版本Ubuntu系统)',           'type':CONFIG_TOOL,    'tool':'tools/tool_config_system_source.py' ,'dep':[1] },
    # 6: {'tip':'一键安装:NodeJS环境',      'type':INSTALL_SOFTWARE,     'tool':'tools/tool_install_nodejs.py' ,'dep':[] },
    # 7: {'tip':'一键安装:VsCode开发工具',      'type':INSTALL_SOFTWARE,     'tool':'tools/tool_install_vscode.py' ,'dep':[] },
    # 8: {'tip':'一键安装:Docker',      'type':INSTALL_SOFTWARE,     'tool':'tools/tool_install_docker.py' ,'dep':[] },
    # 9: {'tip':'一键安装:Cartographer(18 20测试通过,16未测. updateTime 20240125)',      'type':INSTALL_ROS,     'tool':'tools/tool_install_cartographer.py' ,'dep':[3] },
    # 10: {'tip':'一键安装:微信(可以在Linux上使用的微信)',      'type':INSTALL_SOFTWARE,     'tool':'tools/tool_install_wechat.py' ,'dep':[8] },
    # 11: {'tip':'一键安装:ROS Docker版(支持所有版本ROS/ROS2)',                'type':INSTALL_ROS,    'tool':'tools/tool_install_ros_with_docker.py' ,'dep':[7,8] },
    # 12: {'tip':'一键安装:PlateformIO MicroROS开发环境(支持Fishbot)',      'type':INSTALL_SOFTWARE,     'tool':'tools/tool_install_micros_fishbot_env.py' ,'dep':[] },
    # 13: {'tip':'一键配置:python国内源','type':CONFIG_TOOL,'tool':'tools/tool_config_python_source.py' ,'dep':[] },
    # # 14: {'tip':'一键安装:科学上网代理工具','type':INSTALL_SOFTWARE,'tool':'tools/tool_install_proxy_tool.py' ,'dep':[8] },
    # 15: {'tip':'一键安装：QQ for Linux', 'type':INSTALL_SOFTWARE, 'tool': 'tools/tool_install_qq.py', 'dep':[]},
    # 16: {'tip':'一键安装：系统自带ROS (！！警告！！仅供特殊情况下使用)', 'type':INSTALL_ROS, 'tool': 'tools/tool_install_ros1_systemdefault.py', 'dep':[5]},
    # 17: {'tip':'一键配置: Docker代理(支持VPN+代理服务两种模式)', 'type':CONFIG_TOOL, 'tool': 'tools/tool_config_docker_proxy.py', 'dep':[]},
    }
# 


# 创建用于存储不同类型工具的字典
tool_categories = {}

# 遍历tools字典，根据type值进行分类
for tool_id, tool_info in tools.items():
    tool_type = tool_info['type']
    # 如果该类型还没有在字典中创建，则创建一个新的列表来存储该类型的工具
    if tool_type not in tool_categories:
        tool_categories[tool_type] = {}
    # 将工具信息添加到相应类型的列表中
    tool_categories[tool_type][tool_id]=tool_info

tracking = None
def main():
    # download base
    url_prefix = os.environ.get('FISHROS_URL','https://raw.githubusercontent.com/wwwwwyt/intall/refs/heads/master')
    os.system("wget {} -O /tmp/HighTorque_install{} --no-check-certificate".format(base_url,base_url.replace(url_prefix,'')))

    from tools.base import CmdTask,FileUtils,PrintUtils,ChooseTask,ChooseWithCategoriesTask,Tracking
    from tools.base import encoding_utf8,osversion,osarch
    from tools.base import run_tool_file,download_tools
    from tools.base import config_helper,tr

    # download translations
    CmdTask("wget {} -O /tmp/HighTorque_install{} --no-check-certificate".format(translator_url,translator_url.replace(url_prefix,''))).run()

    importlib.import_module("tools.translation.translator").Linguist()
    from tools.base import tr
    import copy

    global tracing
    tracing = copy.copy(Tracking)


    # 使用量统计 
    # CmdTask("wget https://fishros.org.cn/forum/topic/1733 -O /tmp/t1733 -q  --timeout 10 && rm -rf /tmp/t1733").run()

    # PrintUtils.print_success(tr.tr("已为您切换语言至当前所在国家语言:")+tr.lang)
    # if tr.country != 'CN':
    #     PrintUtils.print_success(tr.tr("检测到当前不在CN,切换服务地址为:https://raw.githubusercontent.com/fishros/install/master/"))
    #     url_prefix = 'https://raw.githubusercontent.com/fishros/install/master/'


    # check base config
    if not encoding_utf8:
        print("Your system encoding not support ,will install some packgaes..")
        CmdTask("sudo apt-get install language-pack-zh-hans -y",0).run()
        CmdTask("sudo apt-get install apt-transport-https -y",0).run()
        FileUtils.append("/etc/profile",'export LANG="zh_CN.UTF-8"')
        print('Finish! Please Try Again!')
        print('Solutions: https://fishros.org.cn/forum/topic/24 ')
        return False
    PrintUtils.print_success(tr.tr("基础检查通过..."))
    
    book = tr.tr("""
                        .-~~~~~~~~~-._       _.-~~~~~~~~~-.
                    __.'              ~.   .~              `.__
                .'//     开卷有益        \./     书山有路     \\ `.
                .'// 可以多看看小鱼的文章  | 关注B站鱼香ROS机器人 \\ `.
            .'// .-~~~~~~~~~~~~~~-._     |     _,-~~~~~~~~~~~. \\`.
            .'//.-"                 `-.  |  .-'                 "-.\\`.
        .'//______.============-..   \ | /   ..-============.______\\`.
        .'______________________________\|/______________________________`
        ----------------------------------------------------------------------""")

    tip =tr.tr("""===============================================================================
======一键安装工具=======
===============================================================================
    """)
    end_tip = tr.tr("""===============================================================================
如果觉得工具好用,请给个star,如果你想和小鱼一起编写工具,请关注B站/公众号<鱼香ROS>,联系小鱼
更多工具教程，请访问鱼香ROS官方网站:http://fishros.com
    """)
    PrintUtils.print_delay(tip,0.001)
    # PrintUtils.print_delay(book,0.001)
    # download tools
    code,result = ChooseWithCategoriesTask(tool_categories, tips=tr.tr("---众多工具，等君来用---"),categories=tools_type_map).run()
    if code==0: PrintUtils().print_success(tr.tr("是觉得没有合胃口的菜吗？那快联系的小鱼增加菜单吧~"))
    else: 
        download_tools(code,tools,url_prefix)
        run_tool_file(tools[code]['tool'].replace("/","."))
    config_helper.gen_config_file()
    
    # PrintUtils.print_delay(tr.tr("欢迎加入机器人学习交流QQ群：438144612(入群口令：一键安装)"),0.05)
    # PrintUtils.print_delay(tr.tr("鱼香小铺正式开业，最低499可入手一台能建图会导航的移动机器人，淘宝搜店：鱼香ROS 或打开链接查看：https://item.taobao.com/item.htm?id=696573635888"),0.001)
    # PrintUtils.print_delay(tr.tr("如在使用过程中遇到问题，请打开：https://fishros.org.cn/forum 进行反馈"),0.001)

if __name__=='__main__':
    run_exc = []

    try:
        main()
    except Exception as e:
        import traceback
        print('\r\n检测到程序发生异常退出，请打开：https://fishros.org.cn/forum 携带如下内容进行反馈\n\n')
        print("标题：使用一键安装过程中遇到程序崩溃")
        print("```")
        traceback.print_exc()
        run_exc.append(traceback.format_exc())
        print("```")
        print('本次运行详细日志文件已保存至 /tmp/fishros_install.log')

    try:
        with open("/tmp/fishros_install.log", "w", encoding="utf-8") as f:
            for exec in run_exc:
                print(exec, file=f)  # 打印异常输出到文件中
            for text,end in tracing.logs:
                print(text, file=f,end=end)  # 打印输出到文件中
            for text in tracing.err_logs:
                print(text, file=f)  # 打印输出到文件中     
        if tracing.need_report:
            print("")
            input('检测到本次运行出现失败命令,直接退出按Ctrl+C,按任意键上传日志并退出\n')
            ret = os.system("""curl -s -F "file=@/tmp/fishros_install.log" http://103.226.124.73:5000/upload > /tmp/fishros_upload 2>&1""")
            if ret == 0:
                with open("/tmp/fishros_upload","r") as f:
                    print("错误日志上传成功，反馈码:",f.read())
            else:
                print("日志上传失败，若还需反馈请手动发帖!")
    except:
        pass

    