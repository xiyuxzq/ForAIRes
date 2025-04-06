# 3D数学基础：基础概念（第1-3章）

## 第1章 笛卡尔坐标系

### 知识点概述
- 一维数学基础
- 二维笛卡尔空间
- 三维笛卡尔空间
- 基础数学知识

### 详细知识点

#### 1.1 一维数学
- 数轴概念：实数轴的基本性质和特点
- 正负方向：方向的概念和表示方法
- 原点和坐标：坐标系的基本元素
- 一维距离计算：绝对值和距离公式

#### 1.2 二维笛卡尔空间
- x轴和y轴的概念：两个相互垂直的数轴
- 平面坐标系的建立：原点、方向和刻度
- 二维点的表示方法：有序对(x,y)
- 二维距离计算：毕达哥拉斯定理
  ```csharp
  // Unity中计算二维距离的示例
  float Distance2D(Vector2 point1, Vector2 point2) {
      float dx = point2.x - point1.x;
      float dy = point2.y - point1.y;
      return Mathf.Sqrt(dx * dx + dy * dy);
  }
  ```
- Cartesia城市示例：实际应用中的坐标系统

#### 1.3 三维笛卡尔空间
- x、y、z轴的概念：三个相互垂直的数轴
- 三维坐标系的建立：空间直角坐标系
- 三维点的表示方法：有序三元组(x,y,z)
- 左手和右手坐标系的区别：两种常用约定
  ```csharp
  // Unity（左手坐标系）中的向前方向
  Vector3 forward = transform.forward; // (0, 0, 1)

  // OpenGL（右手坐标系）中的向前方向
  vec3 forward = vec3(0.0, 0.0, -1.0);
  ```
- 常用坐标系约定：不同领域的标准选择

#### 1.4 基础数学知识
- 求和与求积符号：Σ和Π的使用
- 区间表示方法：开区间、闭区间、半开区间
- 角度、弧度转换：π弧度=180度
- 基本三角函数：正弦、余弦、正切
- 重要三角恒等式：和差公式、倍角公式

### 实际应用示例
1. 游戏开发中的坐标系统
   - Unity3D中的坐标系统：左手坐标系
   - Unreal Engine中的坐标系统：左手坐标系
   - 2D游戏中的坐标应用：像素坐标系

2. 计算机图形学应用
   - OpenGL中的坐标系统：右手坐标系
   - DirectX中的坐标系统：左手坐标系
   - 3D建模软件中的坐标系统：Maya、3ds Max

3. 实际工程应用
   - CAD系统中的坐标应用：工程制图
   - 机器人运动控制：机械臂定位
   - 计算机视觉中的坐标系统：相机坐标系

### 补充资料
1. 在线资源
   - [Khan Academy - 坐标系统教程](https://www.khanacademy.org/math/geometry/hs-geometric-transforms)
   - [OpenGL坐标系统教程](https://learnopengl.com/Getting-started/Coordinate-Systems)

2. 进阶阅读
   - 《计算机图形学》相关章节
   - 《游戏引擎架构》中的坐标系统部分

### 练习题
1. 一维数学练习
   - 计算数轴上两点之间的距离
   - 理解正负方向的实际应用

2. 二维坐标系练习
   - 在平面上绘制指定坐标的点
   - 计算平面上两点之间的距离
   - 解决Cartesia城市导航问题

3. 三维坐标系练习
   - 绘制三维空间中的点
   - 在左手和右手坐标系中转换坐标
   - 计算空间中两点之间的距离

## 第2章 矢量

### 知识点概述
- 矢量的数学定义
- 矢量的几何定义
- 矢量运算
- 矢量应用

### 详细知识点

#### 2.1 矢量的数学定义
- 矢量的基本概念：有大小和方向的量
- 矢量的表示方法：坐标形式和几何形式
- 矢量的性质：可加性和数乘性质

#### 2.2 矢量的几何定义
- 方向性：矢量的指向
- 大小：矢量的长度或模
- 起点和终点：矢量的位置
- 平移不变性：平移后保持相等

#### 2.3-2.4 矢量和点
- 位移表示：从一点到另一点的有向线段
- 零矢量：长度为零的特殊矢量
- 相对位置：点之间的位置关系
- 点与矢量的关系：位置和方向

#### 2.5-2.7 矢量运算
- 负矢量：方向相反的矢量
- 标量乘法：改变矢量的大小
- 矢量加减法：平行四边形法则
- 线性代数规则：运算法则
- 几何解释：图形表示

##### 点积（Dot Product）应用
1. 判断两个向量的夹角：
```csharp
// 判断敌人是否在玩家前方
bool IsInFront(Vector3 playerForward, Vector3 directionToEnemy) {
    float dot = Vector3.Dot(playerForward, directionToEnemy);
    return dot > 0; // 大于0表示夹角小于90度
}
```

2. 计算投影：
```csharp
// 计算向量在另一个向量上的投影
Vector3 ProjectOnto(Vector3 v1, Vector3 v2) {
    float dot = Vector3.Dot(v1, v2);
    float lengthSq = v2.sqrMagnitude;
    return v2 * (dot / lengthSq);
}
```

##### 叉积（Cross Product）应用
1. 判断向量的左右关系：
```csharp
// 判断点是否在线段的左侧
bool IsPointOnLeft(Vector3 lineStart, Vector3 lineEnd, Vector3 point) {
    Vector3 lineDir = lineEnd - lineStart;
    Vector3 pointDir = point - lineStart;
    Vector3 cross = Vector3.Cross(lineDir, pointDir);
    return cross.y > 0; // 在2D平面中使用
}
```

2. 计算法线：
```csharp
// 计算平面法线
Vector3 CalculateNormal(Vector3 v1, Vector3 v2) {
    return Vector3.Cross(v1, v2).normalized;
}
```

### 实际应用示例
1. 游戏物理系统
   - 力的表示：作用力和反作用力
   - 速度和加速度：运动描述
   - 碰撞检测：法向量和切向量

2. 计算机图形学
   - 光照计算：法线和光线方向
   - 表面法线：几何形状描述
   - 纹理映射：UV坐标系统

3. 动画系统
   - 角色移动：位移向量
   - 摄像机跟随：视角控制
   - 粒子系统：运动轨迹

### 补充资料
1. 在线资源
   - [Vector Mathematics Tutorial](https://www.mathsisfun.com/algebra/vectors.html)
   - [3Blue1Brown - 线性代数的本质](https://www.3blue1brown.com/essence-of-linear-algebra-page)

2. 开发工具
   - Unity Vector3类：游戏开发中的矢量操作
   - Unreal Engine FVector类：虚幻引擎中的矢量
   - GLSL向量运算：着色器编程

## 第3章 多个坐标空间

### 知识点概述
- 坐标空间的概念
- 常用坐标空间类型
- 坐标空间转换
- 嵌套坐标空间

### 详细知识点

#### 3.1 多坐标空间的必要性
- 不同参考系的需求：相对运动和观察
- 局部和全局坐标的关系：层次结构
- 坐标变换的意义：空间转换的实际应用

#### 3.2 常用坐标空间
- 世界空间：全局参考系
- 对象空间：局部参考系
- 相机空间：观察参考系
- 直立空间：特殊用途的参考系

#### 3.3 坐标空间转换
- 基矢量概念：空间的基本方向
- 转换矩阵：空间变换的数学表示
- 坐标系统间的映射：转换规则
- 变换链：多重转换的组合

##### 实际代码示例
1. 世界空间到局部空间的转换：
```csharp
// Unity中的坐标转换示例
Vector3 WorldToLocal(Vector3 worldPosition, Transform reference) {
    return reference.InverseTransformPoint(worldPosition);
}
```

2. 视图矩阵变换：
```csharp
// OpenGL中的视图矩阵计算
mat4 CalculateViewMatrix(vec3 cameraPos, vec3 target, vec3 up) {
    vec3 zaxis = normalize(cameraPos - target);    // 相机方向
    vec3 xaxis = normalize(cross(up, zaxis));      // 右方向
    vec3 yaxis = cross(zaxis, xaxis);             // 上方向
    
    // 构建视图矩阵
    mat4 viewMatrix = mat4(
        vec4(xaxis.x, yaxis.x, zaxis.x, 0),
        vec4(xaxis.y, yaxis.y, zaxis.y, 0),
        vec4(xaxis.z, yaxis.z, zaxis.z, 0),
        vec4(-dot(xaxis, cameraPos), -dot(yaxis, cameraPos), -dot(zaxis, cameraPos), 1)
    );
    return viewMatrix;
}
```

### 实际应用示例
1. 游戏开发
   - 角色控制系统：局部和世界坐标
   - 相机系统：视图变换
   - 场景管理：空间层次

2. 3D建模
   - 模型编辑：对象空间操作
   - 骨骼动画：多重空间变换
   - UV映射：纹理空间

3. 虚拟现实
   - 头显追踪：视点变换
   - 手柄控制：交互空间
   - 空间定位：追踪系统

### 补充资料
1. 技术文档
   - [Unity坐标空间指南](https://docs.unity3d.com/Manual/Transforms.html)
   - [DirectX坐标系统](https://docs.microsoft.com/en-us/windows/win32/direct3d9/coordinate-systems)

2. 教程资源
   - 游戏引擎架构设计：空间系统
   - 计算机图形学：坐标变换

### 练习题
1. 坐标转换练习
   - 世界坐标到局部坐标的转换
   - 相机视图变换计算
   - 多重变换链的应用

2. 实际应用练习
   - 设计角色跟随系统
   - 实现第三人称相机
   - VR控制器空间定位