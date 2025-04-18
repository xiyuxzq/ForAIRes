# Data Layers 系统

## 定义

Data Layers 是一个系统，旨在为运行时和编辑提供条件性加载世界数据。Actor和 World Partition 定义流送逻辑（Is Spatially Loaded、Runtime Grid 和 Enable Streaming），而 Data Layers 作为关卡流送的过滤器。

## 类型和状态

### 运行时 Data Layers
- 处理不同场景
- 在同一世界中创建变化
- 管理序列、任务、游戏进程、事件等的特定数据
- 完全支持 HLODs
- 也是编辑器数据层

运行时状态：
- Unloaded：内容从内存中卸载且不可见
- Loaded：内容加载到内存中但不可见
- Activated：内容加载到内存中且可见

### 编辑器 Data Layers
- 组织内容
- 隔离数据以更好地进行上下文工作
- 预览运行时数据层内容
- 编辑器专用数据层在 PIE 和烘焙构建中不可访问

编辑器状态：
- IsInitiallyVisible：加载世界时默认是否可见
- IsInitiallyLoaded：加载世界时默认是否加载
- Loaded：用户切换加载
- Visible：用户切换可见性

## UE 5.4 重要更新

### 客户端/服务器专用数据层
- 使用每个数据层的 Load Filter 选项定义数据层是否应仅在客户端或服务器端加载

### 外部包数据层实例
- 通过将数据层实例外部化为单独的文件，消除了对 WorldDataLayers Actor的争用

### 运行时默认逻辑运算符
- 公开在创建新关卡时应使用的默认逻辑运算符
- 可以在项目设置中设置默认逻辑操作为 "OR" 或 "AND"

## 最佳实践

1. **使用编辑器专用数据层隔离内容**
   - 轻松隔离电影和特定游戏序列的工作集内容
   - 允许分离自动/程序化数据或特定类型

2. **预加载和序列器**
   - 使用序列器数据层轨道，可以预滚动并设置不同状态
   - 当播放开始时，所有内容都已准备就绪

3. **数据层所有者和项目范围数据层**
   - 最好在制作中为项目范围的数据层和结构设置技术所有者
   - 尽可能预定义匹配项目结构和目标的数据层资产

## 限制

1. **OR 逻辑**
   - 在运行时和编辑器中，数据层逻辑操作都是 OR
   - 只要其中一个数据层加载或激活，Actor就会加载
   - 注意：5.4 引入了 AND 作为可选的数据层逻辑运算符

2. **层次和最小逻辑**
   - 在数据层层次结构中，应用了与父数据层状态的最小逻辑
   - 编辑器专用数据层不能是运行时数据层的子级

3. **WorldDataLayers Actor**
   - 数据层实例添加到 WorldDataLayers Actor中
   - 这个Actor是一个外部Actor文件
   - 频繁操作可能导致争用和冲突

## 实际应用案例

### Fortnite Chapter 5
- 50+ 运行时用于事件/季节更改
- 用于电影制作工作流程以应用每镜头的世界更改
- 用于测试世界以层叠不同配置进行测试

### The Matrix Awaken 演示
- 35 个运行时
- 32 个编辑器：
  - 序列和游戏玩法内容流送和卸载
  - 序列特定优化
  - 所有平台优化
  - 多个编辑器专用工作集

## 未来发展

1. 用于插件的外部数据层，以便更轻松地将 DLC/未来内容注入现有世界
2. 数据层 - 有用的命令

## 实用命令

- `wp.DumpDatalayers`：在日志中转储数据层列表及其运行时状态
- `wp.Runtime.DebugFilerByDatalayer`：用于过滤运行时哈希 2d 调试显示中可见的数据层
- `wp.Runtime.SetDataLayerRuntimeState [state] [layer]`：强制数据层到特定运行时状态
- `wp.Runtime.ToggleDataLayerActivation [layer]`：激活/停用特定运行时数据层
- `wp.Runtime.ToggleDrawDataLayers`：在主视图中显示数据层及其状态列表