# 一键安装

## 工具列表

已支持工具列表：

- 一键安装:sim2real 运控代码 一键更新 
.........


## 使用方法
```
wget https://raw.githubusercontent.com/wwwwwyt/intall/refs/heads/master/install -O hightorque && . hightorque
```


## 脚本目录
-tools

## 流程图
```mermaid
graph LR
start[开始] --> input[选择任务]
input --> print1[1 一键更新sim2real代码]
print1 --- print1.1[检查是否以 root 用户运行]
print1.1 --- print1.2[检查 SSH_AUTH_SOCK 环境变量是否设置]
print1.2 --- condition1.3{检查本地仓库是否存在}
condition1.3 -- 是 --- print1.5[更新仓库并切换到最新标签]
condition1.3 -- 否 --- print1.4[输入机器人类型并克隆仓库]
print1.4 --- print1.5
print1.5 --- print1.6[编译]
input --> print2[2 一键安装]
```