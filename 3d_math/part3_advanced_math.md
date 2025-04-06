# 3D数学基础：高级数学概念（第7-8章）

## 第7章 极坐标系统

### 知识点概述
- 极坐标的基本概念
- 2D极坐标系统
- 3D极坐标（球坐标）系统
- 坐标系统转换

### 详细知识点

#### 7.1 极坐标基础
- 极坐标的定义：角度和距离
  ```csharp
  // 极坐标结构体定义
  struct PolarCoordinate {
      public float radius;    // 极径（到原点距离）
      public float angle;     // 极角（弧度）
      
      public PolarCoordinate(float r, float a) {
          radius = r;
          angle = a;
      }
  }
  ```

- 极点和极轴：坐标系的基准
  ```csharp
  // 极坐标系统类
  public class PolarSystem {
      private Vector2 origin;     // 极点位置
      private float axisAngle;    // 极轴角度（相对于x轴）
      
      public PolarSystem(Vector2 origin, float axisAngle) {
          this.origin = origin;
          this.axisAngle = axisAngle;
      }
  }
  ```

#### 7.2 2D极坐标系统
- 平面极坐标与笛卡尔坐标转换
  ```csharp
  public static class CoordinateConverter {
      // 笛卡尔坐标转极坐标
      public static PolarCoordinate CartesianToPolar(Vector2 cartesian) {
          float radius = Mathf.Sqrt(cartesian.x * cartesian.x + cartesian.y * cartesian.y);
          float angle = Mathf.Atan2(cartesian.y, cartesian.x);
          return new PolarCoordinate(radius, angle);
      }
      
      // 极坐标转笛卡尔坐标
      public static Vector2 PolarToCartesian(PolarCoordinate polar) {
          float x = polar.radius * Mathf.Cos(polar.angle);
          float y = polar.radius * Mathf.Sin(polar.angle);
          return new Vector2(x, y);
      }
  }
  ```

- 应用场景：环形运动系统
  ```csharp
  public class CircularMotion : MonoBehaviour {
      public float radius = 5f;           // 运动半径
      public float angularSpeed = 2f;     // 角速度
      private float currentAngle = 0f;    // 当前角度
      
      void Update() {
          // 更新角度
          currentAngle += angularSpeed * Time.deltaTime;
          
          // 计算新位置
          Vector2 position = new Vector2(
              radius * Mathf.Cos(currentAngle),
              radius * Mathf.Sin(currentAngle)
          );
          
          transform.position = new Vector3(position.x, position.y, 0);
      }
  }
  ```

#### 7.3 3D极坐标（球坐标）系统
- 球坐标表示和转换
  ```csharp
  public struct SphericalCoordinate {
      public float radius;        // 到原点距离
      public float theta;         // 方位角（水平面内的角度）
      public float phi;           // 仰角（与垂直轴的夹角）
      
      // 球坐标转笛卡尔坐标
      public Vector3 ToCartesian() {
          float x = radius * Mathf.Sin(phi) * Mathf.Cos(theta);
          float y = radius * Mathf.Sin(phi) * Mathf.Sin(theta);
          float z = radius * Mathf.Cos(phi);
          return new Vector3(x, y, z);
      }
  }
  ```

- 应用示例：轨道相机
  ```csharp
  public class OrbitCamera : MonoBehaviour {
      public Transform target;
      public float distance = 10f;
      public float horizontalSpeed = 1f;
      public float verticalSpeed = 1f;
      
      private float theta = 0f;
      private float phi = Mathf.PI / 4f;
      
      void Update() {
          // 更新角度
          theta += Input.GetAxis("Mouse X") * horizontalSpeed;
          phi = Mathf.Clamp(
              phi - Input.GetAxis("Mouse Y") * verticalSpeed,
              0.1f,
              Mathf.PI - 0.1f
          );
          
          // 更新相机位置
          Vector3 position = new Vector3(
              distance * Mathf.Sin(phi) * Mathf.Cos(theta),
              distance * Mathf.Cos(phi),
              distance * Mathf.Sin(phi) * Mathf.Sin(theta)
          );
          
          transform.position = target.position + position;
          transform.LookAt(target);
      }
  }
  ```

#### 7.4 圆柱坐标系统
- 圆柱坐标实现
  ```csharp
  public struct CylindricalCoordinate {
      public float radius;    // 到中轴距离
      public float theta;     // 方位角
      public float height;    // 高度
      
      // 圆柱坐标转笛卡尔坐标
      public Vector3 ToCartesian() {
          return new Vector3(
              radius * Mathf.Cos(theta),
              height,
              radius * Mathf.Sin(theta)
          );
      }
  }
  ```

### 实际应用示例
1. 游戏开发
   - 环形运动系统
   - 雷达显示
   - 星球轨道
   - 螺旋运动

2. 计算机图形学
   - 纹理映射
   - 环境贴图
   - 球面投影
   - 全景图像

3. 物理模拟
   - 行星运动
   - 旋转物体
   - 场力分析
   - 波动传播

### 补充资料
1. 在线资源
   - [极坐标系统可视化](https://www.geogebra.org/m/ERXphSW7)
   - [球坐标系统教程](https://mathworld.wolfram.com/SphericalCoordinates.html)

2. 开发工具
   - Unity极坐标转换工具
   - 数学库实现
   - 图形库支持

## 第8章 3D旋转

### 知识点概述
- 旋转的数学表示
- 欧拉角
- 四元数
- 旋转矩阵

### 详细知识点

#### 8.1 基本旋转概念
- 旋转的定义
- 旋转轴和旋转角
- 右手定则
- 旋转方向约定

#### 8.2 欧拉角
- 欧拉角定义：偏航、俯仰、滚转
- 欧拉角序列
- 万向节死锁问题
- 欧拉角的优缺点

#### 8.3 四元数
- 四元数的数学定义
- 四元数运算规则
- 四元数与旋转的关系
- 四元数插值

#### 8.4 旋转矩阵
- 基本旋转矩阵
- 复合旋转
- 旋转矩阵的性质
- 旋转表示方法比较

### 实际应用示例
1. 角色控制系统
   ```csharp
   public class CharacterRotationController : MonoBehaviour {
       public float turnSpeed = 180f;
       private Quaternion targetRotation;
       
       void Update() {
           float horizontal = Input.GetAxis("Horizontal");
           if (Mathf.Abs(horizontal) > 0.1f) {
               // 计算目标旋转
               float angle = horizontal * turnSpeed * Time.deltaTime;
               targetRotation *= Quaternion.Euler(0, angle, 0);
           }
           
           // 平滑旋转
           transform.rotation = Quaternion.Slerp(
               transform.rotation,
               targetRotation,
               Time.deltaTime * 10f
           );
       }
   }
   ```

2. 高级相机系统
   ```csharp
   public class AdvancedCamera : MonoBehaviour {
       public Transform target;
       public float distance = 5f;
       public Vector2 pitchMinMax = new Vector2(-40f, 85f);
       
       private float currentPitch = 0f;
       private float currentYaw = 0f;
       
       void LateUpdate() {
           // 更新相机角度
           currentYaw += Input.GetAxis("Mouse X") * 2f;
           currentPitch -= Input.GetAxis("Mouse Y") * 2f;
           currentPitch = Mathf.Clamp(currentPitch, pitchMinMax.x, pitchMinMax.y);
           
           // 计算相机位置
           Quaternion rotation = Quaternion.Euler(currentPitch, currentYaw, 0);
           Vector3 position = target.position - (rotation * Vector3.forward * distance);
           
           // 应用变换
           transform.rotation = rotation;
           transform.position = position;
       }
   }
   ```

3. 物理模拟：陀螺运动
   ```csharp
   public class Gyroscope : MonoBehaviour {
       public Vector3 angularVelocity = Vector3.zero;
       public Vector3 angularAcceleration = Vector3.zero;
       private Quaternion rotation;
       
       void Update() {
           // 更新角速度
           angularVelocity += angularAcceleration * Time.deltaTime;
           
           // 计算旋转增量
           Quaternion deltaRotation = Quaternion.Euler(
               angularVelocity * Time.deltaTime
           );
           
           // 应用旋转
           rotation *= deltaRotation;
           transform.rotation = rotation;
           
           // 模拟阻尼
           angularVelocity *= 0.99f;
       }
   }
   ```

### 补充资料
1. 技术文档
   - [四元数旋转指南](https://docs.unity3d.com/Manual/QuaternionAndEulerRotationsInUnity.html)
   - [3D旋转最佳实践](https://www.gamedev.net/articles/programming/math-and-physics/a-guide-to-understanding-3d-rotations-r3205/)

2. 开发工具
   - Unity Quaternion类
   - Unreal Engine旋转系统
   - 物理引擎旋转API

### 练习题
1. 基础练习
   - 欧拉角转换
   - 四元数计算
   - 旋转矩阵构建

2. 实践项目
   - 实现简单的相机系统
   - 构建角色控制器
   - 开发物理模拟系统

3. 进阶挑战
   - 实现平滑的相机跟随
   - 开发高级动画混合系统
   - 构建飞行模拟器

### 重要算法实现
1. 四元数插值
```cpp
Quaternion Slerp(Quaternion q1, Quaternion q2, float t) {
    // 确保最短路径旋转
    float cosHalfTheta = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z;
    if (cosHalfTheta < 0) {
        q2 = new Quaternion(-q2.x, -q2.y, -q2.z, -q2.w);
        cosHalfTheta = -cosHalfTheta;
    }
    
    if (cosHalfTheta >= 1.0f)
        return q1;
        
    float halfTheta = Mathf.Acos(cosHalfTheta);
    float sinHalfTheta = Mathf.Sqrt(1.0f - cosHalfTheta * cosHalfTheta);
    
    if (Mathf.Abs(sinHalfTheta) < 0.001f)
        return new Quaternion(
            q1.x * 0.5f + q2.x * 0.5f,
            q1.y * 0.5f + q2.y * 0.5f,
            q1.z * 0.5f + q2.z * 0.5f,
            q1.w * 0.5f + q2.w * 0.5f
        );
        
    float ratioA = Mathf.Sin((1 - t) * halfTheta) / sinHalfTheta;
    float ratioB = Mathf.Sin(t * halfTheta) / sinHalfTheta;
    
    return new Quaternion(
        q1.x * ratioA + q2.x * ratioB,
        q1.y * ratioA + q2.y * ratioB,
        q1.z * ratioA + q2.z * ratioB,
        q1.w * ratioA + q2.w * ratioB
    );
}
```

2. 欧拉角转旋转矩阵
```cpp
Matrix3x3 EulerToMatrix(float pitch, float yaw, float roll) {
    float cp = Mathf.Cos(pitch);
    float sp = Mathf.Sin(pitch);
    float cy = Mathf.Cos(yaw);
    float sy = Mathf.Sin(yaw);
    float cr = Mathf.Cos(roll);
    float sr = Mathf.Sin(roll);
    
    Matrix3x3 matrix;
    matrix[0,0] = cy * cr + sy * sp * sr;
    matrix[0,1] = -cy * sr + sy * sp * cr;
    matrix[0,2] = sy * cp;
    
    matrix[1,0] = sr * cp;
    matrix[1,1] = cr * cp;
    matrix[1,2] = -sp;
    
    matrix[2,0] = -sy * cr + cy * sp * sr;
    matrix[2,1] = sy * sr + cy * sp * cr;
    matrix[2,2] = cy * cp;
    
    return matrix;
}
```