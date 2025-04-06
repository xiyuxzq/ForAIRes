# 3D数学入门：图形和游戏开发

## 引言

这是一本关于3D图形和游戏开发中必需的数学知识的全面指南。本书涵盖了从基础的笛卡尔坐标系到高级的3D曲线等多个主题。

## 目录概述

### 第1章：笛卡尔坐标系
- 基础数学概念
- 一维、二维和三维空间
- 坐标系统和约定
- 三角函数基础

**重点知识：**
- 笛卡尔坐标系的基本概念
- 左手和右手坐标系统的区别
- 角度、弧度的转换和使用

**代码示例：**
```python
import math

# 角度转弧度
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

# 弧度转角度
def radians_to_degrees(radians):
    return radians * (180 / math.pi)
```

**学习资源：**
- [可汗学院 - 坐标系统](https://www.khanacademy.org/math/geometry/hs-geometric-foundations)
- [3Blue1Brown - 向量和空间](https://www.3blue1brown.com/topics/linear-algebra)

### 第2章：矢量
- 矢量的数学和几何定义
- 矢量运算（加、减、乘）
- 点积和叉积

**重点知识：**
- 矢量的基本运算
- 点积在计算角度中的应用
- 叉积在计算法向量中的应用

**代码示例：**
```python
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
```

**学习资源：**
- [线性代数的本质 - 3Blue1Brown](https://www.3blue1brown.com/essence-of-linear-algebra-page)
- [Unity - Vector3 文档](https://docs.unity3d.com/ScriptReference/Vector3.html)

### 第3章：多个坐标空间
- 世界空间
- 对象空间
- 相机空间
- 坐标空间转换

**重点知识：**
- 不同坐标空间的用途
- 坐标空间转换的基本原理
- 基矢量的概念和应用

**代码示例：**
```cpp
// 简单的空间变换示例
struct Transform {
    Vector3 position;
    Quaternion rotation;
    Vector3 scale;
    
    Matrix4x4 GetLocalToWorldMatrix() {
        return Matrix4x4.TRS(position, rotation, scale);
    }
    
    Vector3 TransformPoint(Vector3 localPoint) {
        return GetLocalToWorldMatrix().MultiplyPoint(localPoint);
    }
};
```

**学习资源：**
- [LearnOpenGL - 坐标系统](https://learnopengl.com/Getting-started/Coordinate-Systems)
- [Scratchapixel 2.0 - 几何变换](https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/geometry)

### 第4-6章：矩阵
- 矩阵基础
- 线性变换
- 矩阵运算
- 特殊矩阵（正交、逆等）

**重点知识：**
- 矩阵的基本运算
- 变换矩阵的构建和应用
- 特殊矩阵的性质和用途

**代码示例：**
```cpp
class Matrix4x4 {
public:
    float m[4][4];
    
    // 创建单位矩阵
    static Matrix4x4 Identity() {
        Matrix4x4 mat;
        for(int i = 0; i < 4; i++)
            for(int j = 0; j < 4; j++)
                mat.m[i][j] = (i == j) ? 1.0f : 0.0f;
        return mat;
    }
    
    // 创建旋转矩阵
    static Matrix4x4 RotationY(float angle) {
        float c = cos(angle);
        float s = sin(angle);
        Matrix4x4 mat = Identity();
        mat.m[0][0] = c;
        mat.m[0][2] = -s;
        mat.m[2][0] = s;
        mat.m[2][2] = c;
        return mat;
    }
};
```

**学习资源：**
- [矩阵变换可视化](https://matrix.reshish.com/)
- [计算机图形学中的矩阵数学](https://www.youtube.com/watch?v=vQ60rFwh2ig)

### 第7章：极坐标系
- 二维极坐标
- 三维极坐标（球面和柱面）
- 坐标转换

**重点知识：**
- 极坐标系的基本概念
- 不同坐标系统之间的转换
- 极坐标在实际应用中的优势

**代码示例：**
```python
import math

def cartesian_to_polar(x, y):
    r = math.sqrt(x*x + y*y)
    theta = math.atan2(y, x)
    return r, theta

def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y
```

**学习资源：**
- [极坐标系统可视化](https://www.geogebra.org/m/nv9vex8y)
- [极坐标在游戏开发中的应用](https://www.gamedeveloper.com/programming/polar-coordinates-in-games)

### 第8章：三维旋转
- 欧拉角
- 四元数
- 旋转矩阵
- 轴角表示

**重点知识：**
- 不同旋转表示方法的优缺点
- 四元数的基本运算
- 避免万向节死锁

**代码示例：**
```cpp
class Quaternion {
public:
    float w, x, y, z;
    
    // 从欧拉角创建四元数
    static Quaternion FromEuler(float pitch, float yaw, float roll) {
        float cy = cos(yaw * 0.5f);
        float sy = sin(yaw * 0.5f);
        float cp = cos(pitch * 0.5f);
        float sp = sin(pitch * 0.5f);
        float cr = cos(roll * 0.5f);
        float sr = sin(roll * 0.5f);

        Quaternion q;
        q.w = cr * cp * cy + sr * sp * sy;
        q.x = sr * cp * cy - cr * sp * sy;
        q.y = cr * sp * cy + sr * cp * sy;
        q.z = cr * cp * sy - sr * sp * cy;
        return q;
    }
};
```

**学习资源：**
- [四元数可视化](https://eater.net/quaternions)
- [Unity中的旋转和四元数](https://docs.unity3d.com/Manual/QuaternionAndEulerRotationsInUnity.html)

### 第9章：几何图元
- 直线和射线
- 球体和圆
- 包围盒
- 平面和多边形

**重点知识：**
- 基本几何图元的数学表示
- 碰撞检测基础
- 包围体优化

**代码示例：**
```cpp
struct AABB {
    Vector3 min;
    Vector3 max;
    
    bool Intersects(const AABB& other) {
        return (min.x <= other.max.x && max.x >= other.min.x) &&
               (min.y <= other.max.y && max.y >= other.min.y) &&
               (min.z <= other.max.z && max.z >= other.min.z);
    }
    
    bool Contains(const Vector3& point) {
        return point.x >= min.x && point.x <= max.x &&
               point.y >= min.y && point.y <= max.y &&
               point.z >= min.z && point.z <= max.z;
    }
};
```

**学习资源：**
- [实时碰撞检测](http://realtimecollisiondetection.net/)
- [游戏编程中的几何算法](https://www.geometrictools.com/)

### 第10章：三维图形数学
- 渲染管线
- 视图和投影
- 纹理映射
- 光照模型

**重点知识：**
- 渲染管线的各个阶段
- 不同类型的投影
- 基本光照模型

**代码示例：**
```glsl
// 基础的Phong光照模型
vec3 CalculatePhongLighting(vec3 normal, vec3 lightDir, vec3 viewDir) {
    // 环境光
    vec3 ambient = 0.1 * lightColor;
    
    // 漫反射
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    // 镜面反射
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = 0.5 * spec * lightColor;
    
    return ambient + diffuse + specular;
}
```

**学习资源：**
- [LearnOpenGL教程](https://learnopengl.com/)
- [现代OpenGL教程](https://www.opengl-tutorial.org/)

### 第11-12章：力学
- 运动学
- 动力学
- 碰撞响应
- 刚体模拟

**重点知识：**
- 基本物理定律的应用
- 碰撞检测和响应
- 刚体动力学模拟

**代码示例：**
```cpp
class RigidBody {
public:
    Vector3 position;
    Vector3 velocity;
    Vector3 acceleration;
    float mass;
    
    void Update(float deltaTime) {
        // 欧拉积分
        velocity += acceleration * deltaTime;
        position += velocity * deltaTime;
        
        // 应用阻尼
        velocity *= 0.99f;
    }
    
    void ApplyForce(const Vector3& force) {
        acceleration += force / mass;
    }
};
```

**学习资源：**
- [游戏物理教程](https://gafferongames.com/)
- [Bullet物理引擎文档](https://pybullet.org/wordpress/)

### 第13章：三维曲线
- 参数曲线
- 贝塞尔曲线
- 样条曲线
- 曲线插值

**重点知识：**
- 不同类型的曲线表示
- 曲线的数学性质
- 实际应用中的选择

**代码示例：**
```cpp
class BezierCurve {
public:
    Vector3 p0, p1, p2, p3; // 控制点
    
    Vector3 Evaluate(float t) {
        float u = 1.0f - t;
        float tt = t * t;
        float uu = u * u;
        float uuu = uu * u;
        float ttt = tt * t;
        
        return uuu * p0 +
               3 * uu * t * p1 +
               3 * u * tt * p2 +
               ttt * p3;
    }
};
```

**学习资源：**
- [贝塞尔曲线交互式演示](https://www.desmos.com/calculator/cahqdxeshd)
- [计算机图形学中的曲线](https://www.cs.cmu.edu/~462/lectures/lecture8.pdf)

## 总结

这本书提供了游戏和图形开发所需的全面数学基础。关键要点包括：

1. 坐标系统和向量运算的基础知识
2. 矩阵变换和旋转的深入理解
3. 实用的几何图元和碰撞检测技术
4. 基本的物理模拟原理
5. 曲线和表面的数学表示

## 进阶学习建议

1. 深入学习图形API（OpenGL/DirectX/Vulkan）
2. 研究现代游戏引擎的源码
3. 实践物理模拟项目
4. 学习高级渲染技术
5. 探索计算几何算法

## 实用工具和资源

1. 数学库：GLM, DirectXMath
2. 物理引擎：Bullet, PhysX
3. 图形调试工具：RenderDoc, PIX
4. 3D建模软件：Blender, Maya
5. 游戏引擎：Unity, Unreal Engine

## 在线学习平台

1. [Coursera - 游戏开发专项课程](https://www.coursera.org/specializations/game-development)
2. [Udemy - 计算机图形学课程](https://www.udemy.com/topic/computer-graphics/)
3. [edX - 计算机图形学基础](https://www.edx.org/learn/computer-graphics)
4. [YouTube - TheChernoProject](https://www.youtube.com/user/TheChernoProject)
5. [Scratchapixel 2.0](https://www.scratchapixel.com/)