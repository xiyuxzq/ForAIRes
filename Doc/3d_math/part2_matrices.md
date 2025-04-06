# 3D数学基础：矩阵（第4-6章）

## 第4章 矩阵介绍

### 知识点概述
- 矩阵的基本概念
- 矩阵的运算规则
- 矩阵在3D图形中的应用
- 特殊矩阵类型

### 详细知识点

#### 4.1 矩阵的基本概念
- 矩阵的定义：m×n个数的矩形数组
  ```cpp
  // C++中的矩阵定义示例
  template<typename T, size_t M, size_t N>
  class Matrix {
      T data[M][N];
  public:
      Matrix() { /* 初始化为0 */ }
      T& operator()(size_t i, size_t j) { return data[i][j]; }
  };
  ```

- 矩阵的维度：行数和列数
- 矩阵元素的表示：下标约定
- 方阵：行数等于列数的矩阵

#### 4.2 矩阵运算
- 矩阵加减法：同型矩阵的运算
  ```csharp
  // Unity中的矩阵加法示例
  Matrix4x4 MatrixAdd(Matrix4x4 a, Matrix4x4 b) {
      Matrix4x4 result = new Matrix4x4();
      for (int i = 0; i < 4; i++)
          for (int j = 0; j < 4; j++)
              result[i,j] = a[i,j] + b[i,j];
      return result;
  }
  ```

- 矩阵数乘：标量与矩阵的乘法
  ```csharp
  // Unity中的矩阵数乘示例
  Matrix4x4 MatrixScale(float scalar, Matrix4x4 mat) {
      Matrix4x4 result = new Matrix4x4();
      for (int i = 0; i < 4; i++)
          for (int j = 0; j < 4; j++)
              result[i,j] = scalar * mat[i,j];
      return result;
  }
  ```

- 矩阵乘法：行列相乘规则
  ```csharp
  // Unity中的矩阵乘法示例
  Matrix4x4 MatrixMultiply(Matrix4x4 a, Matrix4x4 b) {
      return a * b; // Unity内置运算符
  }
  
  // OpenGL中的矩阵乘法示例
  mat4 modelViewProjection = projectionMatrix * viewMatrix * modelMatrix;
  ```

#### 4.3 特殊矩阵
- 单位矩阵：对角线为1，其余为0
  ```csharp
  // Unity中创建单位矩阵
  Matrix4x4 identity = Matrix4x4.identity;
  ```

- 零矩阵：所有元素为0
  ```csharp
  // Unity中创建零矩阵
  Matrix4x4 zero = Matrix4x4.zero;
  ```

- 对角矩阵：非对角线元素为0
  ```csharp
  // 创建缩放矩阵（对角矩阵的特例）
  Matrix4x4 CreateScaleMatrix(float x, float y, float z) {
      Matrix4x4 m = Matrix4x4.identity;
      m[0,0] = x;
      m[1,1] = y;
      m[2,2] = z;
      return m;
  }
  ```

### 实际应用示例
1. 3D图形变换
   ```csharp
   // Unity中的变换矩阵示例
   public class TransformExample : MonoBehaviour {
       void ApplyTransformation() {
           // 创建平移矩阵
           Matrix4x4 translation = Matrix4x4.Translate(new Vector3(1, 2, 3));
           
           // 创建旋转矩阵
           Matrix4x4 rotation = Matrix4x4.Rotate(Quaternion.Euler(30, 45, 60));
           
           // 创建缩放矩阵
           Matrix4x4 scale = Matrix4x4.Scale(new Vector3(2, 2, 2));
           
           // 复合变换（注意顺序：缩放->旋转->平移）
           Matrix4x4 transform = translation * rotation * scale;
           
           // 应用变换到顶点
           Vector3 vertex = new Vector3(1, 1, 1);
           Vector3 transformed = transform.MultiplyPoint3x4(vertex);
       }
   }
   ```

2. 游戏开发应用
   - 角色动画变换
   - 相机视图矩阵
   - 投影矩阵

### 补充资料
1. 在线资源
   - [Matrix Mathematics Tutorial](https://www.mathsisfun.com/algebra/matrix-introduction.html)
   - [3Blue1Brown - 矩阵变换可视化](https://www.3blue1brown.com/lessons/matrices)

2. 开发工具
   - Unity Matrix4x4类
   - DirectX矩阵运算
   - GLSL矩阵操作

## 第5章 矩阵和线性变换

### 知识点概述
- 线性变换的概念
- 变换矩阵的构建
- 仿射变换
- 齐次坐标

### 详细知识点

#### 5.1 线性变换
- 线性变换的定义：保持向量加法和标量乘法的变换
- 线性变换的性质：可叠加性和比例性
  ```csharp
  // Unity中的线性变换示例
  public class LinearTransformExample {
      // 检查变换是否是线性的
      bool IsLinearTransform(Matrix4x4 transform) {
          // 线性变换必须将原点映射到原点
          Vector3 origin = Vector3.zero;
          Vector3 transformedOrigin = transform.MultiplyPoint3x4(origin);
          return transformedOrigin == origin;
      }
  }
  ```

#### 5.2 变换矩阵
- 2D变换矩阵
  ```csharp
  // 2D旋转矩阵
  Matrix4x4 Create2DRotationMatrix(float angleInDegrees) {
      float rad = angleInDegrees * Mathf.Deg2Rad;
      float cos = Mathf.Cos(rad);
      float sin = Mathf.Sin(rad);
      
      Matrix4x4 m = Matrix4x4.identity;
      m[0,0] = cos;  m[0,1] = -sin;
      m[1,0] = sin;  m[1,1] = cos;
      return m;
  }
  ```

- 3D变换矩阵
  ```csharp
  // 3D旋转矩阵（绕任意轴旋转）
  Matrix4x4 CreateRotationMatrix(Vector3 axis, float angleInDegrees) {
      return Matrix4x4.Rotate(Quaternion.AngleAxis(angleInDegrees, axis));
  }
  ```

#### 5.3 仿射变换
- 仿射变换的实现
  ```csharp
  // Unity中的仿射变换示例
  public class AffineTransformExample {
      Matrix4x4 CreateAffineTransform(Vector3 translation, Quaternion rotation, Vector3 scale) {
          Matrix4x4 m = Matrix4x4.identity;
          
          // 构建变换矩阵（TRS）
          m = Matrix4x4.TRS(translation, rotation, scale);
          
          return m;
      }
      
      // 应用仿射变换
      Vector3 ApplyAffineTransform(Matrix4x4 transform, Vector3 point) {
          return transform.MultiplyPoint3x4(point);
      }
  }
  ```

#### 5.4 齐次坐标
- 齐次坐标的使用
  ```glsl
  // GLSL中使用齐次坐标的顶点着色器示例
  #version 330 core
  layout (location = 0) in vec3 position;
  
  uniform mat4 model;
  uniform mat4 view;
  uniform mat4 projection;
  
  void main() {
      // 将3D点转换为齐次坐标 (x,y,z,1)
      vec4 homogeneous = vec4(position, 1.0);
      // 应用MVP变换
      gl_Position = projection * view * model * homogeneous;
  }
  ```

### 实际应用示例
1. 计算机图形学
   - 模型变换
   - 视图变换
   - 投影变换
   - 视口变换

2. 游戏物理系统
   - 碰撞检测
   - 物理模拟
   - 粒子系统

### 补充资料
1. 技术文档
   - OpenGL变换指南
   - DirectX矩阵变换
   - Unity Transform API

2. 进阶学习
   - 计算机图形学中的矩阵应用
   - 游戏引擎中的变换系统

## 第6章 矩阵详解

### 知识点概述
- 矩阵的高级运算
- 特征值和特征向量
- 矩阵分解
- 矩阵优化

### 详细知识点

#### 6.1 矩阵的高级运算
- 矩阵求逆
  ```csharp
  // Unity中的矩阵求逆
  Matrix4x4 GetInverseTransform(Matrix4x4 transform) {
      Matrix4x4 inverse = Matrix4x4.Inverse(transform);
      return inverse;
  }
  ```

- 行列式计算
  ```cpp
  // C++中计算2x2矩阵行列式
  float Determinant2x2(const Matrix2x2& m) {
      return m(0,0) * m(1,1) - m(0,1) * m(1,0);
  }
  ```

#### 6.2 特征值和特征向量
- 特征值计算示例
  ```cpp
  // 使用幂迭代法计算最大特征值（简化版本）
  float PowerIteration(const Matrix& A, Vector& v, int iterations) {
      for(int i = 0; i < iterations; i++) {
          v = A * v;
          v = v.normalized();
      }
      // v现在近似于最大特征值对应的特征向量
      return (A * v).magnitude();
  }
  ```

#### 6.3 矩阵分解
- LU分解示例
  ```cpp
  // 简化版LU分解
  void LUDecomposition(const Matrix& A, Matrix& L, Matrix& U) {
      int n = A.size();
      L = Matrix::Identity(n);
      U = A;
      
      for(int i = 0; i < n; i++) {
          for(int j = i + 1; j < n; j++) {
              float factor = U[j][i] / U[i][i];
              L[j][i] = factor;
              for(int k = i; k < n; k++) {
                  U[j][k] -= factor * U[i][k];
              }
          }
      }
  }
  ```

#### 6.4 矩阵优化
- SIMD优化示例
  ```cpp
  // 使用SSE指令优化矩阵乘法
  void MatrixMultiplySIMD(const float* A, const float* B, float* C, int n) {
      for(int i = 0; i < n; i += 4) {
          for(int j = 0; j < n; j++) {
              __m128 sum = _mm_setzero_ps();
              for(int k = 0; k < n; k++) {
                  __m128 a = _mm_load_ps(&A[i * n + k]);
                  __m128 b = _mm_set1_ps(B[k * n + j]);
                  sum = _mm_add_ps(sum, _mm_mul_ps(a, b));
              }
              _mm_store_ps(&C[i * n + j], sum);
          }
      }
  }
  ```

### 实际应用示例
1. 物理引擎中的矩阵应用
   ```csharp
   // 刚体变换示例
   public class RigidBodyTransform {
       Matrix4x4 worldTransform;
       Vector3 linearVelocity;
       Vector3 angularVelocity;
       
       void UpdateTransform(float deltaTime) {
           // 更新位置
           Vector3 position = worldTransform.GetPosition();
           position += linearVelocity * deltaTime;
           
           // 更新旋转
           Quaternion rotation = worldTransform.rotation;
           Quaternion deltaRotation = Quaternion.Euler(angularVelocity * deltaTime);
           rotation *= deltaRotation;
           
           // 构建新的变换矩阵
           worldTransform = Matrix4x4.TRS(position, rotation, Vector3.one);
       }
   }
   ```

2. 动画系统中的矩阵应用
   ```csharp
   // 骨骼动画示例
   public class SkeletalAnimation {
       struct Bone {
           Matrix4x4 bindPose;
           Matrix4x4 currentPose;
           int parentIndex;
       }
       
       void UpdateBoneTransforms(Bone[] bones) {
           for(int i = 0; i < bones.Length; i++) {
               if(bones[i].parentIndex >= 0) {
                   // 计算世界空间变换
                   bones[i].currentPose = 
                       bones[bones[i].parentIndex].currentPose * 
                       bones[i].currentPose;
               }
           }
       }
   }
   ```

这些补充内容和代码示例展示了矩阵在3D图形学和游戏开发中的实际应用。每个示例都包含了详细的注释，帮助理解其实现原理和用途。特别是在变换、动画和物理模拟等领域，矩阵运算起着核心作用。

### 练习题
1. 基础练习
   - 矩阵运算
   - 变换矩阵构建
   - 特征值计算

2. 实践项目
   - 实现简单的变换系统
   - 构建基本的物理引擎
   - 优化矩阵运算性能

3. 进阶挑战
   - 实现高级动画系统
   - 开发碰撞检测系统
   - 构建渲染管线