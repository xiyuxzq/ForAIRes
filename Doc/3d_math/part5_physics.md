# 3D数学基础：物理学（第11-12章）

## 第11章 力学1：线性运动学和微积分

### 知识点概述
- 微积分基础
- 运动学基本概念
- 速度和加速度
- 路径和轨迹

### 详细知识点

#### 11.1 微积分基础
- 导数的概念和实现
  ```csharp
  public class NumericalDerivative {
      // 数值导数计算
      public static float Derivative(Func<float, float> f, float x, float h = 0.0001f) {
          return (f(x + h) - f(x)) / h;
      }
      
      // 二阶导数计算
      public static float SecondDerivative(Func<float, float> f, float x, float h = 0.0001f) {
          return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h);
      }
  }
  ```

- 积分的数值实现
  ```csharp
  public class NumericalIntegration {
      // 梯形法则积分
      public static float TrapezoidalIntegration(Func<float, float> f, float a, float b, int n) {
          float h = (b - a) / n;
          float sum = 0.5f * (f(a) + f(b));
          
          for (int i = 1; i < n; i++) {
              sum += f(a + i * h);
          }
          
          return h * sum;
      }
      
      // 辛普森积分
      public static float SimpsonIntegration(Func<float, float> f, float a, float b, int n) {
          float h = (b - a) / n;
          float sum = f(a) + f(b);
          
          for (int i = 1; i < n; i += 2) {
              sum += 4 * f(a + i * h);
          }
          
          for (int i = 2; i < n-1; i += 2) {
              sum += 2 * f(a + i * h);
          }
          
          return h * sum / 3;
      }
  }
  ```

#### 11.2 运动学基础
- 运动状态表示
  ```csharp
  public class MotionState {
      public Vector3 position;
      public Vector3 velocity;
      public Vector3 acceleration;
      public float time;
      
      // 更新运动状态（使用欧拉积分）
      public void Update(float dt) {
          velocity += acceleration * dt;
          position += velocity * dt;
          time += dt;
      }
      
      // 预测未来位置
      public Vector3 PredictPosition(float deltaTime) {
          return position + velocity * deltaTime + 
                 0.5f * acceleration * deltaTime * deltaTime;
      }
  }
  ```

#### 11.3 运动分析
- 复杂运动系统
  ```csharp
  public class MotionAnalysis {
      // 抛物运动模拟
      public class ProjectileMotion {
          public Vector3 initialPosition;
          public Vector3 initialVelocity;
          public Vector3 gravity = new Vector3(0, -9.81f, 0);
          
          public Vector3 GetPositionAtTime(float t) {
              return initialPosition + 
                     initialVelocity * t + 
                     0.5f * gravity * t * t;
          }
          
          // 计算落地时间
          public float CalculateTimeToGround(float groundY = 0) {
              // 求解二次方程
              float a = 0.5f * gravity.y;
              float b = initialVelocity.y;
              float c = initialPosition.y - groundY;
              
              float discriminant = b * b - 4 * a * c;
              if (discriminant < 0) return float.NaN;
              
              float t1 = (-b + Mathf.Sqrt(discriminant)) / (2 * a);
              float t2 = (-b - Mathf.Sqrt(discriminant)) / (2 * a);
              
              return Mathf.Max(t1, t2);
          }
      }
      
      // 简谐运动模拟
      public class HarmonicMotion {
          public float amplitude;
          public float frequency;
          public float phase;
          
          public float GetDisplacement(float t) {
              return amplitude * Mathf.Sin(2 * Mathf.PI * frequency * t + phase);
          }
          
          public float GetVelocity(float t) {
              return amplitude * 2 * Mathf.PI * frequency * 
                     Mathf.Cos(2 * Mathf.PI * frequency * t + phase);
          }
      }
  }
  ```

#### 11.4 数值方法
- 高级积分器实现
  ```csharp
  public class AdvancedIntegrator {
      // RK4积分器
      public class RK4Integrator {
          public delegate Vector3 DerivativeFunction(Vector3 state, float t);
          
          public static Vector3 Integrate(Vector3 state, float t, float dt, DerivativeFunction f) {
              Vector3 k1 = f(state, t);
              Vector3 k2 = f(state + k1 * dt * 0.5f, t + dt * 0.5f);
              Vector3 k3 = f(state + k2 * dt * 0.5f, t + dt * 0.5f);
              Vector3 k4 = f(state + k3 * dt, t + dt);
              
              return state + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6;
          }
      }
      
      // Verlet积分器
      public class VerletIntegrator {
          private Vector3 previousPosition;
          private Vector3 currentPosition;
          private float dt;
          
          public void Initialize(Vector3 position, Vector3 velocity, float timeStep) {
              currentPosition = position;
              previousPosition = position - velocity * timeStep;
              dt = timeStep;
          }
          
          public Vector3 Integrate(Vector3 acceleration) {
              Vector3 nextPosition = 2 * currentPosition - previousPosition + 
                                   acceleration * dt * dt;
              previousPosition = currentPosition;
              currentPosition = nextPosition;
              return currentPosition;
          }
          
          public Vector3 GetVelocity() {
              return (currentPosition - previousPosition) / dt;
          }
      }
  }
  ```

### 实际应用示例
1. 物理引擎实现
```cpp
class PhysicsSystem {
    struct Particle {
        Vector3 position;
        Vector3 velocity;
        Vector3 acceleration;
        float mass;
    };
    
    void UpdateParticle(Particle& p, float dt) {
        // 半隐式欧拉积分
        p.velocity += p.acceleration * dt;
        p.position += p.velocity * dt;
    }
    
    void ApplyForce(Particle& p, Vector3 force) {
        p.acceleration = force / p.mass;
    }
    
    Vector3 CalculateGravity(float mass) {
        return Vector3(0, -9.81f, 0) * mass;
    }
}
```

2. 轨迹预测
```cpp
Vector3[] PredictProjectileTrajectory(Vector3 initialPos, Vector3 initialVel, float time, int steps) {
    Vector3[] positions = new Vector3[steps];
    float dt = time / steps;
    Vector3 gravity = Vector3(0, -9.81f, 0);
    
    positions[0] = initialPos;
    Vector3 pos = initialPos;
    Vector3 vel = initialVel;
    
    for(int i = 1; i < steps; i++) {
        vel += gravity * dt;
        pos += vel * dt;
        positions[i] = pos;
    }
    
    return positions;
}
```

### 补充资料
1. 物理模拟资源
   - [物理引擎教程](https://gafferongames.com/)
   - [数值方法指南](https://www.numerical-methods.com/)

2. 开发工具
   - Unity Physics
   - Bullet Physics
   - PhysX

## 第12章 力学2：线性和旋转动力学

### 知识点概述
- 力和运动定律
- 动量和能量
- 旋转运动
- 刚体动力学

### 详细知识点

#### 12.1 牛顿运动定律
- 第一定律：惯性定律
- 第二定律：加速度定律
- 第三定律：作用力与反作用力
- 重力和摩擦力

#### 12.2 动量和能量
- 线性动量
- 角动量
- 动能
- 势能
- 能量守恒

#### 12.3 旋转运动
- 角速度
- 角加速度
- 转动惯量
- 旋转动能

#### 12.4 刚体动力学
- 刚体定义
- 质心运动
- 转动方程
- 欧拉方程

### 实际应用示例
1. 刚体物理模拟
```cpp
class RigidBody {
    Matrix3x3 inertiaTensor;
    Vector3 angularVelocity;
    Quaternion orientation;
    Vector3 position;
    Vector3 velocity;
    
    void UpdatePhysics(float dt) {
        // 更新位置
        position += velocity * dt;
        
        // 更新旋转
        Quaternion spin(angularVelocity * dt);
        orientation = spin * orientation;
        orientation.Normalize();
        
        // 更新惯性张量
        Matrix3x3 rotMat = orientation.ToMatrix();
        Matrix3x3 worldInertia = rotMat * inertiaTensor * rotMat.Transpose();
        
        // 计算角加速度
        Vector3 torque = CalculateTorque();
        Vector3 angularAccel = worldInertia.Inverse() * torque;
        angularVelocity += angularAccel * dt;
    }
};
```

2. 碰撞响应
```cpp
void ResolveCollision(RigidBody& a, RigidBody& b, Vector3 normal, float penetration) {
    // 计算相对速度
    Vector3 relativeVel = b.velocity - a.velocity;
    
    // 计算冲量
    float restitution = 0.8f; // 弹性系数
    float j = -(1 + restitution) * dot(relativeVel, normal) /
              (1/a.mass + 1/b.mass);
              
    // 应用冲量
    a.velocity -= j * normal / a.mass;
    b.velocity += j * normal / b.mass;
    
    // 处理穿透
    float percent = 0.8f; // 穿透修正系数
    Vector3 correction = normal * penetration * percent;
    a.position -= correction * (1/a.mass)/(1/a.mass + 1/b.mass);
    b.position += correction * (1/b.mass)/(1/a.mass + 1/b.mass);
}
```

### 补充资料
1. 物理引擎设计
   - [Game Physics Engine Development](http://gameenginebook.com/)
   - [Real-Time Collision Detection](http://realtimecollisiondetection.net/)

2. 高级主题
   - 约束求解
   - 连续碰撞检测
   - 软体模拟

### 练习题
1. 基础练习
   - 实现简单的粒子系统
   - 编写基本的碰撞检测
   - 模拟抛物运动

2. 进阶项目
   - 开发刚体物理引擎
   - 实现约束系统
   - 构建车辆物理模型

3. 性能优化
   - 空间划分
   - 碰撞优化
   - 并行计算

### 重要算法
1. 积分器
```cpp
class Integrator {
    Vector3 RK4(Vector3 x, Vector3 v, float dt) {
        Vector3 k1 = v;
        Vector3 k2 = v + acceleration(x + k1 * dt/2) * dt/2;
        Vector3 k3 = v + acceleration(x + k2 * dt/2) * dt/2;
        Vector3 k4 = v + acceleration(x + k3 * dt) * dt;
        
        return x + (k1 + k2*2 + k3*2 + k4) * dt/6;
    }
};
```

2. 碰撞检测
```cpp
bool SphereCollision(Vector3 c1, float r1, Vector3 c2, float r2, out Vector3 normal, out float depth) {
    Vector3 d = c2 - c1;
    float dist2 = dot(d, d);
    float radiusSum = r1 + r2;
    
    if(dist2 <= radiusSum * radiusSum) {
        float dist = sqrt(dist2);
        normal = d / dist;
        depth = radiusSum - dist;
        return true;
    }
    return false;
}
```