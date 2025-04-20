# ZBrush高精度模型制作工作流程

## 一、基础设置

### 1. 项目设置
```zbrush
- 分辨率：4096 x 4096
- 默认材质：SkinShade4
- 笔刷设置：
  - Standard笔刷
  - ClayBuildup笔刷
  - Dam_Standard笔刷
```

### 2. 子工具组织
```
- 头部
  - 基础网格
  - 细节层
  - 皮肤纹理层
- 眼睛
  - 眼球
  - 眼睑
- 牙齿和舌头
```

## 二、高精度雕刻流程

### 1. 基础形态
```zbrush
1. 使用ZSphere创建基础网格
2. 自适应重拓扑(ZRemesher)
   - 目标面数：100K
   - Keep Groups选项开启
3. 分区设置
   - PolyGroup按解剖结构划分
   - 使用GroupsLoops确保边界清晰
```

### 2. 细节雕刻
```zbrush
1. 面部特征
   - 使用Dam_Standard定义主要轮廓
   - ClayBuildup添加体积
   - 使用Alpha贴图添加皮肤纹理

2. 分层处理
   - SubTool > Divide设置
     - 层级1: 100K面 (基础形态)
     - 层级2: 500K面 (中等细节)
     - 层级3: 2M面 (高频细节)
```

### 3. 特殊处理
```zbrush
1. 眼睛区域
   - 使用Insert Mesh放置眼球
   - 雕刻眼睑褶皱
   - 添加睫毛基础形态

2. 嘴部细节
   - 雕刻唇纹
   - 添加牙齿和舌头
   - 处理口腔内部
```

## 三、UV和拓扑处理

### 1. UV展开
```zbrush
1. UV Master设置
   - Enable Control Painting
   - 标记缝合线
   - 使用Unwrap处理

2. 检查和优化
   - 确保无重叠
   - 优化UV空间利用
   - 导出UV贴图
```

### 2. 拓扑优化
```zbrush
1. ZRemesher设置
   - Target Polygon Count: 适应目标平台
   - Keep Groups: 开启
   - Legacy: 关闭
   
2. 手动调整
   - 使用ZModeler处理特殊区域
   - 确保面部变形区域拓扑质量
```

## 四、导出准备

### 1. 细节贴图生成
```zbrush
1. 置换贴图
   - 分辨率：4K或8K
   - 32位精度
   - 适当的强度范围

2. 法线贴图
   - 切线空间
   - 翻转Y通道
```

### 2. 文件整理
```zbrush
1. 命名规范
   - 主要部件_子部件_类型
   - 使用统一前缀

2. 导出选项
   - OBJ/FBX格式
   - 包含UV信息
   - 保留组信息
```

## 五、质量检查清单

### 1. 模型检查
- [ ] 面数是否符合要求
- [ ] 拓扑流线是否合理
- [ ] 是否存在非流形边
- [ ] 是否存在反面

### 2. UV检查
- [ ] UV是否有重叠
- [ ] 缝合线是否合理
- [ ] 贴图空间利用是否合理
- [ ] 是否保留边界延展

### 3. 细节检查
- [ ] 置换贴图是否完整
- [ ] 法线贴图是否正确
- [ ] 细节层级是否合适
- [ ] 是否存在穿插

## 六、常见问题解决

### 1. 性能问题
```zbrush
1. 卡顿处理
   - 使用较低细分层级工作
   - 关闭实时预览
   - 使用FOV控制显示范围

2. 内存优化
   - 定期保存和清理
   - 合理使用分层
   - 控制贴图大小
```

### 2. 导出问题
```zbrush
1. 贴图错误
   - 检查UV设置
   - 验证贴图尺寸
   - 确认导出路径

2. 模型问题
   - 修复非流形边
   - 检查法线方向
   - 验证骨骼绑定
```

## 七、优化建议

### 1. 工作流程优化
```zbrush
1. 使用快捷键
   - 自定义常用操作
   - 创建工具预设
   - 使用宏录制

2. 文件管理
   - 创建项目模板
   - 使用版本控制
   - 定期备份
```

### 2. 性能优化
```zbrush
1. 显示设置
   - 适当的视口设置
   - 合理的细分层级
   - 优化预览质量

2. 资源管理
   - 控制贴图大小
   - 优化笔刷设置
   - 清理未使用资源
```

## 八、参考资源

### 1. 官方资源
- [ZBrush文档](https://docs.pixologic.com/)
- [ZBrush教程](https://pixologic.com/zclassroom/)
- [ZBrush论坛](https://forums.pixologic.com/)

### 2. 推荐插件
- ZRemesher
- UV Master
- Decimation Master
- FiberMesh

### 3. 学习资料
- Anatomy for Sculptors
- ZBrush Character Creation
- Digital Sculpting with ZBrush

## 更新记录

- 2024-03-22: 初始版本
- 2024-03-23: 添加高级雕刻技巧
- 2024-03-24: 更新优化建议 