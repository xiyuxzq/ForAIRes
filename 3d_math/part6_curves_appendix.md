# 3D数学基础：曲线和附录（第13章及附录）

## 第13章 3D曲线

### 知识点概述
- 曲线的数学表示
- 参数曲线
- 样条曲线
- 曲线插值

### 详细知识点

#### 13.1 曲线基础
- 曲线表示系统
  ```csharp
  public abstract class Curve3D {
      // 获取曲线上的点
      public abstract Vector3 GetPoint(float t);
      
      // 获取曲线在某点的切线
      public abstract Vector3 GetTangent(float t);
      
      // 获取曲线在某点的法线
      public virtual Vector3 GetNormal(float t) {
          Vector3 tangent = GetTangent(t);
          Vector3 binormal = Vector3.Cross(tangent, Vector3.up);
          return Vector3.Cross(binormal, tangent).normalized;
      }
      
      // 计算曲线长度（数值积分）
      public float CalculateLength(float start, float end, int segments = 100) {
          float length = 0;
          float step = (end - start) / segments;
          Vector3 prevPoint = GetPoint(start);
          
          for (int i = 1; i <= segments; i++) {
              float t = start + step * i;
              Vector3 currentPoint = GetPoint(t);
              length += Vector3.Distance(prevPoint, currentPoint);
              prevPoint = currentPoint;
          }
          
          return length;
      }
  }
  ```

#### 13.2 参数曲线
- 贝塞尔曲线系统
  ```csharp
  public class BezierCurve : Curve3D {
      private Vector3[] controlPoints;
      
      public BezierCurve(Vector3[] points) {
          controlPoints = points;
      }
      
      // 德卡斯特里奥算法计算贝塞尔曲线点
      public override Vector3 GetPoint(float t) {
          Vector3[] points = (Vector3[])controlPoints.Clone();
          int n = points.Length;
          
          for (int r = 1; r < n; r++) {
              for (int i = 0; i < n - r; i++) {
                  points[i] = Vector3.Lerp(points[i], points[i + 1], t);
              }
          }
          
          return points[0];
      }
      
      public override Vector3 GetTangent(float t) {
          if (controlPoints.Length < 2) return Vector3.zero;
          
          Vector3[] points = (Vector3[])controlPoints.Clone();
          int n = points.Length;
          
          // 计算一阶导数
          Vector3[] derivatives = new Vector3[n - 1];
          for (int i = 0; i < n - 1; i++) {
              derivatives[i] = (points[i + 1] - points[i]) * (n - 1);
          }
          
          // 使用德卡斯特里奥算法计算导数点
          for (int r = 1; r < n - 1; r++) {
              for (int i = 0; i < n - r - 1; i++) {
                  derivatives[i] = Vector3.Lerp(derivatives[i], derivatives[i + 1], t);
              }
          }
          
          return derivatives[0].normalized;
      }
  }
  ```

- B样条曲线实现
  ```csharp
  public class BSplineCurve : Curve3D {
      private Vector3[] controlPoints;
      private int degree;
      private float[] knots;
      
      public BSplineCurve(Vector3[] points, int p) {
          controlPoints = points;
          degree = p;
          
          // 生成均匀B样条的节点向量
          int n = points.Length - 1;
          int m = n + p + 1;
          knots = new float[m + 1];
          
          for (int i = 0; i <= m; i++) {
              if (i < p) knots[i] = 0;
              else if (i > n) knots[i] = 1;
              else knots[i] = (float)(i - p) / (n - p + 1);
          }
      }
      
      // 计算基函数
      private float BasisFunction(int i, int p, float t) {
          if (p == 0) {
              return (t >= knots[i] && t < knots[i + 1]) ? 1 : 0;
          }
          
          float d1 = knots[i + p] - knots[i];
          float d2 = knots[i + p + 1] - knots[i + 1];
          
          float c1 = (d1 > 0) ? (t - knots[i]) / d1 : 0;
          float c2 = (d2 > 0) ? (knots[i + p + 1] - t) / d2 : 0;
          
          return c1 * BasisFunction(i, p - 1, t) + 
                 c2 * BasisFunction(i + 1, p - 1, t);
      }
      
      public override Vector3 GetPoint(float t) {
          if (t >= 1) t = 1 - float.Epsilon;
          
          Vector3 point = Vector3.zero;
          for (int i = 0; i < controlPoints.Length; i++) {
              float basis = BasisFunction(i, degree, t);
              point += controlPoints[i] * basis;
          }
          return point;
      }
      
      public override Vector3 GetTangent(float t) {
          // 数值方法计算切线
          float h = 0.0001f;
          Vector3 p1 = GetPoint(t);
          Vector3 p2 = GetPoint(t + h);
          return ((p2 - p1) / h).normalized;
      }
  }
  ```

#### 13.3 曲线性质
- 曲线分析工具
  ```csharp
  public class CurveAnalyzer {
      // 计算曲率
      public static float CalculateCurvature(Curve3D curve, float t) {
          float h = 0.0001f;
          Vector3 p0 = curve.GetPoint(t - h);
          Vector3 p1 = curve.GetPoint(t);
          Vector3 p2 = curve.GetPoint(t + h);
          
          Vector3 v1 = (p1 - p0).normalized;
          Vector3 v2 = (p2 - p1).normalized;
          float angle = Mathf.Acos(Vector3.Dot(v1, v2));
          
          return angle / (Vector3.Distance(p0, p2));
      }
      
      // 检查连续性
      public static bool CheckContinuity(Curve3D curve1, Curve3D curve2, float t, int order) {
          const float epsilon = 0.0001f;
          
          switch (order) {
              case 0: // C0连续性（位置连续）
                  return Vector3.Distance(
                      curve1.GetPoint(1),
                      curve2.GetPoint(0)
                  ) < epsilon;
                  
              case 1: // C1连续性（切线连续）
                  return Vector3.Distance(
                      curve1.GetTangent(1),
                      curve2.GetTangent(0)
                  ) < epsilon;
                  
              default:
                  return false;
          }
      }
  }
  ```

#### 13.4 曲线应用
- 路径跟随系统
  ```csharp
  public class PathFollower : MonoBehaviour {
      public Curve3D path;
      public float speed = 1.0f;
      public bool lookForward = true;
      
      private float currentT = 0;
      
      void Update() {
          // 更新路径位置
          currentT += speed * Time.deltaTime;
          if (currentT > 1) currentT -= 1;
          
          // 设置位置
          transform.position = path.GetPoint(currentT);
          
          // 设置朝向
          if (lookForward) {
              Vector3 forward = path.GetTangent(currentT);
              if (forward != Vector3.zero) {
                  transform.forward = forward;
              }
          }
      }
  }
  ```

- 相机轨道系统
  ```csharp
  public class CameraSpline : MonoBehaviour {
      public Transform target;
      public Vector3[] controlPoints;
      private BezierCurve orbitPath;
      
      void Start() {
          orbitPath = new BezierCurve(controlPoints);
      }
      
      public Vector3 GetCameraPosition(float t) {
          Vector3 position = orbitPath.GetPoint(t);
          Vector3 targetPos = target.position;
          Vector3 up = Vector3.up;
          
          // 计算相机朝向
          Vector3 forward = (targetPos - position).normalized;
          Vector3 right = Vector3.Cross(up, forward).normalized;
          up = Vector3.Cross(forward, right);
          
          transform.rotation = Quaternion.LookRotation(forward, up);
          return position;
      }
  }
  ```

### 实际应用示例
1. 贝塞尔曲线实现
```cpp
Vector3 CubicBezier(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t) {
    float u = 1 - t;
    float tt = t * t;
    float uu = u * u;
    float uuu = uu * u;
    float ttt = tt * t;
    
    Vector3 p = uuu * p0;
    p += 3 * uu * t * p1;
    p += 3 * u * tt * p2;
    p += ttt * p3;
    
    return p;
}

Vector3 CubicBezierDerivative(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t) {
    float u = 1 - t;
    float tt = t * t;
    float uu = u * u;
    
    Vector3 p = -3 * uu * p0;
    p += 3 * (3*tt - 4*t + 1) * p1;
    p += 3 * (-3*tt + 2*t) * p2;
    p += 3 * tt * p3;
    
    return p;
}
```

2. 样条曲线系统
```cpp
class SplineSystem {
    struct SplinePoint {
        Vector3 position;
        Vector3 tangent;
        float tension;
    };
    
    Vector3 CatmullRom(SplinePoint p0, SplinePoint p1, SplinePoint p2, SplinePoint p3, float t) {
        float t2 = t * t;
        float t3 = t2 * t;
        
        Vector3 a = 2 * p1.position;
        Vector3 b = p2.position - p0.position;
        Vector3 c = 2*p0.position - 5*p1.position + 4*p2.position - p3.position;
        Vector3 d = -p0.position + 3*p1.position - 3*p2.position + p3.position;
        
        return 0.5f * (a + (b * t) + (c * t2) + (d * t3));
    }
    
    Vector3 GetSplinePoint(float t) {
        // 找到对应的样条段
        int numPoints = points.size();
        float segment = t * (numPoints - 1);
        int i = (int)segment;
        float localT = segment - i;
        
        return CatmullRom(
            points[max(0, i-1)],
            points[i],
            points[min(numPoints-1, i+1)],
            points[min(numPoints-1, i+2)],
            localT
        );
    }
};
```

### 补充资料
1. 曲线设计资源
   - [计算机辅助几何设计](https://www.sciencedirect.com/science/article/abs/pii/B9780444534620000016)
   - [数字曲线与曲面](https://www.springer.com/gp/book/9783540367109)

2. 开发工具
   - Unity Animation Curves
   - Maya曲线工具
   - AutoCAD样条工具

## 附录A：几何测试

### 知识点概述
- 相交测试
- 包含测试
- 距离计算
- 最近点计算

### 详细知识点

#### A.1 基本测试
- 几何测试工具
  ```csharp
  public static class GeometryTest {
      // 点到直线距离
      public static float PointLineDistance(Vector3 point, Vector3 lineStart, Vector3 lineEnd) {
          Vector3 line = lineEnd - lineStart;
          float len = line.magnitude;
          line.Normalize();
          
          Vector3 v = point - lineStart;
          float d = Vector3.Dot(v, line);
          d = Mathf.Clamp(d, 0f, len);
          
          Vector3 projection = lineStart + line * d;
          return Vector3.Distance(point, projection);
      }
      
      // 点到平面距离
      public static float PointPlaneDistance(Vector3 point, Vector3 planeNormal, Vector3 planePoint) {
          planeNormal.Normalize();
          return Vector3.Dot(point - planePoint, planeNormal);
      }
      
      // 线段相交检测
      public static bool LineSegmentIntersection(
          Vector2 p1, Vector2 p2, Vector2 p3, Vector2 p4, out Vector2 intersection
      ) {
          intersection = Vector2.zero;
          
          float denominator = (p4.y - p3.y) * (p2.x - p1.x) - 
                            (p4.x - p3.x) * (p2.y - p1.y);
                            
          if (Mathf.Abs(denominator) < float.Epsilon)
              return false;
              
          float ua = ((p4.x - p3.x) * (p1.y - p3.y) - 
                     (p4.y - p3.y) * (p1.x - p3.x)) / denominator;
          float ub = ((p2.x - p1.x) * (p1.y - p3.y) - 
                     (p2.y - p1.y) * (p1.x - p3.x)) / denominator;
          
          if (ua < 0 || ua > 1 || ub < 0 || ub > 1)
              return false;
              
          intersection = p1 + ua * (p2 - p1);
          return true;
      }
  }
  ```

#### A.2 复杂测试
- 高级碰撞检测
  ```csharp
  public class CollisionDetection {
      // 分离轴定理（SAT）检测多边形碰撞
      public static bool PolygonCollision(Vector2[] polygonA, Vector2[] polygonB) {
          // 获取所有投影轴
          Vector2[] axes = GetProjectionAxes(polygonA, polygonB);
          
          // 在每个轴上检查重叠
          foreach (Vector2 axis in axes) {
              float minA, maxA, minB, maxB;
              ProjectPolygon(axis, polygonA, out minA, out maxA);
              ProjectPolygon(axis, polygonB, out minB, out maxB);
              
              // 检查是否有分离轴
              if (maxA < minB || maxB < minA)
                  return false;
          }
          
          return true;
      }
      
      private static Vector2[] GetProjectionAxes(Vector2[] polygonA, Vector2[] polygonB) {
          List<Vector2> axes = new List<Vector2>();
          
          // 添加多边形A的所有边的法线
          for (int i = 0; i < polygonA.Length; i++) {
              Vector2 edge = polygonA[(i + 1) % polygonA.Length] - polygonA[i];
              axes.Add(new Vector2(-edge.y, edge.x).normalized);
          }
          
          // 添加多边形B的所有边的法线
          for (int i = 0; i < polygonB.Length; i++) {
              Vector2 edge = polygonB[(i + 1) % polygonB.Length] - polygonB[i];
              axes.Add(new Vector2(-edge.y, edge.x).normalized);
          }
          
          return axes.ToArray();
      }
      
      private static void ProjectPolygon(
          Vector2 axis, Vector2[] polygon, out float min, out float max
      ) {
          min = float.MaxValue;
          max = float.MinValue;
          
          foreach (Vector2 point in polygon) {
              float projection = Vector2.Dot(point, axis);
              min = Mathf.Min(min, projection);
              max = Mathf.Max(max, projection);
          }
      }
      
      // 动态包围盒树（AABB树）
      public class AABBTree {
          public class Node {
              public AABB bounds;
              public Node left;
              public Node right;
              public object data;
              
              public bool IsLeaf() {
                  return left == null && right == null;
              }
          }
          
          private Node root;
          
          public void Insert(AABB bounds, object data) {
              Node newNode = new Node { bounds = bounds, data = data };
              
              if (root == null) {
                  root = newNode;
                  return;
              }
              
              Node node = root;
              while (!node.IsLeaf()) {
                  float costLeft = CalculateInsertionCost(node.left, newNode);
                  float costRight = CalculateInsertionCost(node.right, newNode);
                  
                  if (costLeft <= costRight)
                      node = node.left;
                  else
                      node = node.right;
              }
              
              // 创建新的父节点
              Node oldParent = node.parent;
              Node newParent = new Node();
              newParent.parent = oldParent;
              newParent.bounds = AABB.Union(node.bounds, newNode.bounds);
              newParent.left = node;
              newParent.right = newNode;
              node.parent = newParent;
              newNode.parent = newParent;
              
              // 更新树
              if (oldParent != null) {
                  if (oldParent.left == node)
                      oldParent.left = newParent;
                  else
                      oldParent.right = newParent;
              }
              else {
                  root = newParent;
              }
          }
          
          private float CalculateInsertionCost(Node node, Node newNode) {
              AABB combinedBounds = AABB.Union(node.bounds, newNode.bounds);
              return combinedBounds.GetArea() - node.bounds.GetArea();
          }
      }
  }
  ```

这些补充内容提供了详细的代码实现和实际应用示例，涵盖了3D曲线和几何测试的核心概念。每个示例都包含了必要的注释，有助于理解其工作原理和实际应用场景。

## 附录B：学习建议和资源

### 1. 学习路径建议

#### 入门阶段
1. 基础数学
   - 复习线性代数
   - 学习基本的三角函数
   - 理解向量运算

2. 编程基础
   - C++/C#基础
   - 基本的数据结构
   - 算法思维

#### 进阶阶段
1. 3D数学
   - 矩阵变换
   - 四元数旋转
   - 投影原理

2. 图形编程
   - OpenGL/DirectX基础
   - 着色器编程
   - 渲染管线

#### 专业阶段
1. 物理模拟
   - 刚体动力学
   - 碰撞检测
   - 约束求解

2. 高级主题
   - 曲线与曲面
   - 几何算法
   - 优化技术

### 2. 推荐资源

#### 书籍
1. 基础教材
   - 《3D数学基础：图形和游戏开发》
   - 《计算机图形学原理》
   - 《游戏引擎架构》

2. 进阶读物
   - 《实时碰撞检测算法技术》
   - 《物理引擎开发》
   - 《游戏编程模式》

#### 在线资源
1. 教程网站
   - [LearnOpenGL](https://learnopengl.com/)
   - [Scratchapixel](https://www.scratchapixel.com/)
   - [Game Programming Patterns](http://gameprogrammingpatterns.com/)

2. 开发工具
   - Unity3D
   - Unreal Engine
   - Bullet Physics

#### 实践项目
1. 入门项目
   - 实现简单的变换系统
   - 创建基本的渲染器
   - 开发2D物理模拟

2. 进阶项目
   - 3D游戏引擎开发
   - 物理引擎实现
   - 高级渲染技术

### 3. 学习方法建议

1. 理论结合实践
   - 每学习一个概念就实现一个小demo
   - 在实际项目中应用所学知识
   - 分析现有引擎的源码

2. 循序渐进
   - 打好基础再学习高级主题
   - 由简单到复杂逐步深入
   - 注重知识的连贯性

3. 持续学习
   - 关注领域最新发展
   - 参与开源项目
   - 与他人交流分享

### 4. 常见问题解决

1. 数学基础薄弱
   - 复习相关数学知识
   - 使用可视化工具理解
   - 多做练习题

2. 编程能力不足
   - 系统学习编程语言
   - 练习基本算法
   - 阅读优质代码

3. 概念理解困难
   - 寻找可视化解释
   - 简化问题
   - 多角度思考

### 5. 职业发展

1. 技能方向
   - 游戏开发工程师
   - 图形引擎开发者
   - 物理引擎专家
   - 技术美术

2. 行业机会
   - 游戏公司
   - 3D软件开发
   - 虚拟现实
   - 科学可视化