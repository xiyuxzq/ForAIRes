## 一. 基础坐标系统应用

### 1.1 游戏引擎中的坐标系统
#### Unity3D（左手坐标系）
```csharp
// Unity中的坐标系统示例
public class CoordinateSystemExample : MonoBehaviour 
{
    void Example() 
    {
        // 世界坐标系中的位置
        Vector3 worldPosition = transform.position;
        
        // 本地坐标系中的位置
        Vector3 localPosition = transform.localPosition;
        
        // 方向向量
        Vector3 forward = transform.forward;    // (0, 0, 1)
        Vector3 right = transform.right;        // (1, 0, 0)
        Vector3 up = transform.up;              // (0, 1, 0)
    }
}
```

#### Unreal Engine（左手坐标系）
```cpp
// UE中的坐标系统示例
void ACustomActor::CoordinateExample()
{
    // 世界坐标系中的位置
    FVector WorldLocation = GetActorLocation();
    
    // 本地坐标系中的位置
    FVector LocalLocation = GetRootComponent()->GetRelativeLocation();
    
    // 方向向量
    FVector ForwardVector = GetActorForwardVector();
    FVector RightVector = GetActorRightVector();
    FVector UpVector = GetActorUpVector();
}
```

## 二. 向量运算实战

### 2.1 点积应用
#### 视野检测
```csharp
public class VisionSystem : MonoBehaviour 
{
    public float fieldOfView = 90f;
    
    public bool IsInFieldOfView(Vector3 targetPosition) 
    {
        Vector3 directionToTarget = (targetPosition - transform.position).normalized;
        float angle = Vector3.Angle(transform.forward, directionToTarget);
        return angle <= fieldOfView * 0.5f;
    }
    
    public float GetVisibilityFactor(Vector3 targetPosition) 
    {
        Vector3 directionToTarget = (targetPosition - transform.position).normalized;
        float dot = Vector3.Dot(transform.forward, directionToTarget);
        return Mathf.Max(0, dot); // 0表示背向，1表示正向
    }
}
```

### 2.2 叉积应用
#### 判断转向方向
```csharp
public class SteeringSystem : MonoBehaviour 
{
    public enum TurnDirection { Left, Right, None }
    
    public TurnDirection GetTurnDirection(Vector3 forward, Vector3 targetDirection) 
    {
        Vector3 cross = Vector3.Cross(forward, targetDirection);
        if (cross.y > 0.01f) return TurnDirection.Left;
        if (cross.y < -0.01f) return TurnDirection.Right;
        return TurnDirection.None;
    }
}
```

## 三. 矩阵变换应用

### 3.1 基础变换矩阵
```csharp
public class TransformationMatrix 
{
    // 创建平移矩阵
    public static Matrix4x4 CreateTranslation(Vector3 translation) 
    {
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 3] = translation.x;
        matrix[1, 3] = translation.y;
        matrix[2, 3] = translation.z;
        return matrix;
    }
    
    // 创建缩放矩阵
    public static Matrix4x4 CreateScale(Vector3 scale) 
    {
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 0] = scale.x;
        matrix[1, 1] = scale.y;
        matrix[2, 2] = scale.z;
        return matrix;
    }
    
    // 创建绕X轴旋转矩阵
    public static Matrix4x4 CreateRotationX(float angleInDegrees) 
    {
        Matrix4x4 matrix = Matrix4x4.identity;
        float rad = angleInDegrees * Mathf.Deg2Rad;
        float cos = Mathf.Cos(rad);
        float sin = Mathf.Sin(rad);
        
        matrix[1, 1] = cos;
        matrix[1, 2] = -sin;
        matrix[2, 1] = sin;
        matrix[2, 2] = cos;
        
        return matrix;
    }
}
```

### 3.2 复合变换应用
```csharp
public class TransformationExample : MonoBehaviour 
{
    void ApplyComplexTransform(Vector3 position, Vector3 rotation, Vector3 scale) 
    {
        // 创建各个变换矩阵
        Matrix4x4 translationMatrix = TransformationMatrix.CreateTranslation(position);
        Matrix4x4 rotationX = TransformationMatrix.CreateRotationX(rotation.x);
        Matrix4x4 rotationY = TransformationMatrix.CreateRotationX(rotation.y);
        Matrix4x4 rotationZ = TransformationMatrix.CreateRotationX(rotation.z);
        Matrix4x4 scaleMatrix = TransformationMatrix.CreateScale(scale);
        
        // 组合变换（注意顺序：缩放->旋转->平移）
        Matrix4x4 finalTransform = translationMatrix * 
                                 rotationZ * 
                                 rotationY * 
                                 rotationX * 
                                 scaleMatrix;
                                 
        // 应用变换到物体
        transform.position = finalTransform.MultiplyPoint3x4(Vector3.zero);
        transform.rotation = Quaternion.Euler(rotation);
        transform.localScale = scale;
    }
}
```

## 四. 游戏物理系统应用

### 4.1 基础物理模拟
```csharp
public class PhysicsSimulation : MonoBehaviour 
{
    public Vector3 velocity;
    public Vector3 acceleration;
    public float mass = 1f;
    
    void Update() 
    {
        // 基础物理更新
        velocity += acceleration * Time.deltaTime;
        transform.position += velocity * Time.deltaTime;
        
        // 重力
        ApplyGravity();
        
        // 空气阻力
        ApplyDrag();
    }
    
    void ApplyGravity() 
    {
        Vector3 gravity = new Vector3(0, -9.81f, 0);
        velocity += gravity * Time.deltaTime;
    }
    
    void ApplyDrag() 
    {
        float dragCoefficient = 0.1f;
        Vector3 drag = -velocity.normalized * velocity.sqrMagnitude * dragCoefficient;
        velocity += drag * Time.deltaTime / mass;
    }
}
```

### 4.2 碰撞检测
```csharp
public class CollisionDetection 
{
    // 球体碰撞检测
    public static bool SphereCollision(Vector3 center1, float radius1, 
                                     Vector3 center2, float radius2) 
    {
        float distanceSquared = (center2 - center1).sqrMagnitude;
        float radiusSum = radius1 + radius2;
        return distanceSquared <= radiusSum * radiusSum;
    }
    
    // AABB碰撞检测
    public static bool AABBCollision(Vector3 min1, Vector3 max1, 
                                   Vector3 min2, Vector3 max2) 
    {
        return (min1.x <= max2.x && max1.x >= min2.x) &&
               (min1.y <= max2.y && max1.y >= min2.y) &&
               (min1.z <= max2.z && max1.z >= min2.z);
    }
}
```

## 五. 计算机图形学应用

### 5.1 光照计算
```csharp
public class LightingCalculator 
{
    public static float CalculateDiffuseLighting(Vector3 normal, Vector3 lightDir) 
    {
        float NdotL = Mathf.Max(0, Vector3.Dot(normal, lightDir));
        return NdotL;
    }
    
    public static Vector3 CalculateSpecularLighting(Vector3 normal, Vector3 lightDir, 
                                                  Vector3 viewDir, float shininess) 
    {
        Vector3 reflectDir = Vector3.Reflect(-lightDir, normal);
        float spec = Mathf.Pow(Mathf.Max(0, Vector3.Dot(viewDir, reflectDir)), shininess);
        return new Vector3(spec, spec, spec);
    }
}
```

### 5.2 相机投影
```csharp
public class CameraProjection 
{
    public static Matrix4x4 CreatePerspectiveProjection(
        float fov, float aspectRatio, float near, float far) 
    {
        Matrix4x4 matrix = Matrix4x4.zero;
        float tanHalfFov = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad);
        
        matrix[0,0] = 1f / (aspectRatio * tanHalfFov);
        matrix[1,1] = 1f / tanHalfFov;
        matrix[2,2] = -(far + near) / (far - near);
        matrix[2,3] = -(2f * far * near) / (far - near);
        matrix[3,2] = -1f;
        
        return matrix;
    }
}
```

## 六. 工程应用

### 6.1 CAD系统基础操作
```csharp
public class CADSystem 
{
    // 2D绘图功能
    public static Vector2[] CreateRectangle(Vector2 center, float width, float height) 
    {
        Vector2[] points = new Vector2[4];
        points[0] = center + new Vector2(-width/2, -height/2);
        points[1] = center + new Vector2(width/2, -height/2);
        points[2] = center + new Vector2(width/2, height/2);
        points[3] = center + new Vector2(-width/2, height/2);
        return points;
    }
    
    // 3D建模功能
    public static Mesh CreateCube(Vector3 center, Vector3 dimensions) 
    {
        Mesh mesh = new Mesh();
        // 实现省略...
        return mesh;
    }
}
```

### 6.2 机器人运动控制
```csharp
public class RobotController 
{
    public struct Joint 
    {
        public Vector3 position;
        public Vector3 rotation;
        public Vector3 axis;
    }
    
    public static Vector3 CalculateEndEffectorPosition(Joint[] joints) 
    {
        Vector3 position = Vector3.zero;
        Quaternion rotation = Quaternion.identity;
        
        foreach (Joint joint in joints) 
        {
            rotation *= Quaternion.AngleAxis(
                Vector3.Angle(Vector3.forward, joint.axis),
                joint.rotation
            );
            position += rotation * joint.position;
        }
        
        return position;
    }
} 

## 七. 极坐标系统应用

### 7.1 基础极坐标系统
```csharp
public struct PolarCoordinate 
{
    public float radius;    // 极径（到原点距离）
    public float angle;     // 极角（弧度）
    
    public PolarCoordinate(float r, float a) 
    {
        radius = r;
        angle = a;
    }
    
    // 转换为笛卡尔坐标
    public Vector2 ToCartesian() 
    {
        return new Vector2(
            radius * Mathf.Cos(angle),
            radius * Mathf.Sin(angle)
        );
    }
    
    // 从笛卡尔坐标创建
    public static PolarCoordinate FromCartesian(Vector2 cartesian) 
    {
        float radius = Mathf.Sqrt(cartesian.x * cartesian.x + cartesian.y * cartesian.y);
        float angle = Mathf.Atan2(cartesian.y, cartesian.x);
        return new PolarCoordinate(radius, angle);
    }
}
```

### 7.2 环形运动系统
```csharp
public class CircularMotionController : MonoBehaviour 
{
    public float radius = 5f;           // 运动半径
    public float angularSpeed = 2f;     // 角速度（弧度/秒）
    public float phase = 0f;            // 初始相位
    public bool clockwise = true;       // 顺时针方向
    
    private float currentAngle;
    
    void Start() 
    {
        currentAngle = phase;
    }
    
    void Update() 
    {
        // 更新角度
        float direction = clockwise ? -1f : 1f;
        currentAngle += direction * angularSpeed * Time.deltaTime;
        
        // 计算新位置
        Vector2 position = new Vector2(
            radius * Mathf.Cos(currentAngle),
            radius * Mathf.Sin(currentAngle)
        );
        
        // 更新物体位置
        transform.position = new Vector3(position.x, position.y, 0);
        
        // 可选：使物体始终朝向运动方向
        float rotationAngle = (currentAngle * Mathf.Rad2Deg) + (clockwise ? 90f : -90f);
        transform.rotation = Quaternion.Euler(0, 0, rotationAngle);
    }
}
```

### 7.3 雷达扫描效果
```csharp
public class RadarSystem : MonoBehaviour 
{
    public float scanRadius = 10f;
    public float scanSpeed = 2f;
    public float detectionAngle = 30f;
    public LayerMask targetLayer;
    
    private float currentAngle;
    
    void Update() 
    {
        // 更新扫描角度
        currentAngle += scanSpeed * Time.deltaTime;
        if (currentAngle >= 360f) currentAngle -= 360f;
        
        // 执行扫描
        Vector2 direction = new Vector2(
            Mathf.Cos(currentAngle * Mathf.Deg2Rad),
            Mathf.Sin(currentAngle * Mathf.Deg2Rad)
        );
        
        RaycastHit2D[] hits = Physics2D.CircleCastAll(
            transform.position,
            scanRadius,
            direction,
            0f,
            targetLayer
        );
        
        foreach (RaycastHit2D hit in hits) 
        {
            Vector2 toTarget = (hit.point - (Vector2)transform.position).normalized;
            float angle = Vector2.Angle(direction, toTarget);
            
            if (angle <= detectionAngle * 0.5f) 
            {
                // 目标在扫描范围内
                OnTargetDetected(hit.collider.gameObject);
            }
        }
    }
    
    void OnTargetDetected(GameObject target) 
    {
        // 处理目标检测逻辑
        Debug.Log($"Detected target: {target.name}");
    }
}
```

## 八. 球坐标系统应用

### 8.1 球坐标基础系统
```csharp
public struct SphericalCoordinate 
{
    public float radius;    // 到原点的距离
    public float theta;     // 方位角（水平面内的角度）
    public float phi;       // 仰角（与垂直轴的夹角）
    
    public SphericalCoordinate(float r, float t, float p) 
    {
        radius = r;
        theta = t;
        phi = p;
    }
    
    // 转换为笛卡尔坐标
    public Vector3 ToCartesian() 
    {
        return new Vector3(
            radius * Mathf.Sin(phi) * Mathf.Cos(theta),
            radius * Mathf.Cos(phi),
            radius * Mathf.Sin(phi) * Mathf.Sin(theta)
        );
    }
    
    // 从笛卡尔坐标创建
    public static SphericalCoordinate FromCartesian(Vector3 cartesian) 
    {
        float radius = cartesian.magnitude;
        float theta = Mathf.Atan2(cartesian.z, cartesian.x);
        float phi = Mathf.Acos(cartesian.y / radius);
        return new SphericalCoordinate(radius, theta, phi);
    }
}
```

### 8.2 高级轨道相机
```csharp
public class AdvancedOrbitCamera : MonoBehaviour 
{
    public Transform target;
    public float distance = 10f;
    public float minDistance = 5f;
    public float maxDistance = 20f;
    public float horizontalSpeed = 1f;
    public float verticalSpeed = 1f;
    public float zoomSpeed = 1f;
    public float smoothness = 5f;
    
    private float currentTheta = 0f;
    private float currentPhi = Mathf.PI / 4f;
    private float currentDistance;
    private Vector3 currentPosition;
    private Quaternion currentRotation;
    
    void Start() 
    {
        currentDistance = distance;
        UpdatePosition(true);
    }
    
    void Update() 
    {
        // 处理输入
        float mouseX = Input.GetAxis("Mouse X");
        float mouseY = Input.GetAxis("Mouse Y");
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        
        if (Input.GetMouseButton(1)) // 右键按下时旋转
        {
            currentTheta += mouseX * horizontalSpeed;
            currentPhi = Mathf.Clamp(
                currentPhi - mouseY * verticalSpeed,
                0.1f,
                Mathf.PI - 0.1f
            );
        }
        
        // 处理缩放
        currentDistance = Mathf.Clamp(
            currentDistance - scroll * zoomSpeed,
            minDistance,
            maxDistance
        );
        
        UpdatePosition(false);
    }
    
    void UpdatePosition(bool instant) 
    {
        // 计算目标位置
        Vector3 targetPosition = new Vector3(
            currentDistance * Mathf.Sin(currentPhi) * Mathf.Cos(currentTheta),
            currentDistance * Mathf.Cos(currentPhi),
            currentDistance * Mathf.Sin(currentPhi) * Mathf.Sin(currentTheta)
        );
        targetPosition += target.position;
        
        // 计算目标旋转
        Quaternion targetRotation = Quaternion.LookRotation(
            target.position - targetPosition,
            Vector3.up
        );
        
        if (instant) 
        {
            currentPosition = targetPosition;
            currentRotation = targetRotation;
        } 
        else 
        {
            // 平滑插值
            currentPosition = Vector3.Lerp(
                currentPosition,
                targetPosition,
                Time.deltaTime * smoothness
            );
            currentRotation = Quaternion.Slerp(
                currentRotation,
                targetRotation,
                Time.deltaTime * smoothness
            );
        }
        
        // 应用变换
        transform.position = currentPosition;
        transform.rotation = currentRotation;
    }
}
```

## 九. 圆柱坐标系统应用

### 9.1 圆柱坐标基础系统
```csharp
public struct CylindricalCoordinate 
{
    public float radius;    // 到中轴的距离
    public float theta;     // 方位角
    public float height;    // 高度
    
    public CylindricalCoordinate(float r, float t, float h) 
    {
        radius = r;
        theta = t;
        height = h;
    }
    
    // 转换为笛卡尔坐标
    public Vector3 ToCartesian() 
    {
        return new Vector3(
            radius * Mathf.Cos(theta),
            height,
            radius * Mathf.Sin(theta)
        );
    }
    
    // 从笛卡尔坐标创建
    public static CylindricalCoordinate FromCartesian(Vector3 cartesian) 
    {
        float radius = Mathf.Sqrt(cartesian.x * cartesian.x + cartesian.z * cartesian.z);
        float theta = Mathf.Atan2(cartesian.z, cartesian.x);
        return new CylindricalCoordinate(radius, theta, cartesian.y);
    }
}
```

### 9.2 螺旋楼梯生成器
```csharp
public class SpiralStairGenerator : MonoBehaviour 
{
    public float radius = 2f;           // 螺旋半径
    public float heightPerStep = 0.3f;  // 每级台阶高度
    public float anglePerStep = 30f;    // 每级台阶角度
    public int totalSteps = 12;         // 总台阶数
    public GameObject stepPrefab;       // 台阶预制体
    
    void Start() 
    {
        GenerateStairs();
    }
    
    void GenerateStairs() 
    {
        for (int i = 0; i < totalSteps; i++) 
        {
            float angle = i * anglePerStep * Mathf.Deg2Rad;
            float height = i * heightPerStep;
            
            // 使用圆柱坐标计算位置
            CylindricalCoordinate coord = new CylindricalCoordinate(radius, angle, height);
            Vector3 position = coord.ToCartesian();
            
            // 创建台阶
            GameObject step = Instantiate(stepPrefab, transform);
            step.transform.position = position;
            
            // 设置旋转（使台阶朝向中心轴）
            float rotationAngle = angle * Mathf.Rad2Deg;
            step.transform.rotation = Quaternion.Euler(0, rotationAngle, 0);
        }
    }
}
```

## 十. 3D旋转应用

### 10.1 欧拉角旋转系统
```csharp
public class EulerRotationController : MonoBehaviour 
{
    public Vector3 rotationSpeed = new Vector3(30f, 45f, 60f);
    public bool useLocalRotation = true;
    
    private Vector3 currentRotation;
    
    void Update() 
    {
        // 更新欧拉角
        currentRotation += rotationSpeed * Time.deltaTime;
        
        // 标准化角度到0-360范围
        currentRotation.x = NormalizeAngle(currentRotation.x);
        currentRotation.y = NormalizeAngle(currentRotation.y);
        currentRotation.z = NormalizeAngle(currentRotation.z);
        
        // 应用旋转
        if (useLocalRotation)
            transform.localRotation = Quaternion.Euler(currentRotation);
        else
            transform.rotation = Quaternion.Euler(currentRotation);
    }
    
    float NormalizeAngle(float angle) 
    {
        while (angle > 360f) angle -= 360f;
        while (angle < 0f) angle += 360f;
        return angle;
    }
}
```

### 10.2 四元数旋转插值
```csharp
public class QuaternionRotationController : MonoBehaviour 
{
    public Transform targetA;
    public Transform targetB;
    public float rotationDuration = 1f;
    public AnimationCurve rotationCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);
    
    private float currentTime = 0f;
    private bool isRotating = false;
    private Quaternion startRotation;
    private Quaternion endRotation;
    
    public void StartRotation() 
    {
        startRotation = transform.rotation;
        endRotation = targetB.rotation;
        currentTime = 0f;
        isRotating = true;
    }
    
    void Update() 
    {
        if (!isRotating) return;
        
        currentTime += Time.deltaTime;
        float t = currentTime / rotationDuration;
        
        if (t >= 1f) 
        {
            transform.rotation = endRotation;
            isRotating = false;
            return;
        }
        
        // 使用曲线进行插值
        float curveValue = rotationCurve.Evaluate(t);
        transform.rotation = Quaternion.Slerp(startRotation, endRotation, curveValue);
    }
}
```

## 十一. 高级相机系统

### 11.1 自由视角相机
```csharp
public class FreeLookCamera : MonoBehaviour 
{
    public float moveSpeed = 5f;
    public float rotationSpeed = 3f;
    public float smoothness = 10f;
    public bool invertY = false;
    
    private Vector3 targetPosition;
    private Quaternion targetRotation;
    
    void Start() 
    {
        targetPosition = transform.position;
        targetRotation = transform.rotation;
        Cursor.lockState = CursorLockMode.Locked;
    }
    
    void Update() 
    {
        // 处理移动输入
        Vector3 moveInput = new Vector3(
            Input.GetAxis("Horizontal"),
            0,
            Input.GetAxis("Vertical")
        );
        
        if (Input.GetKey(KeyCode.Q)) moveInput.y -= 1;
        if (Input.GetKey(KeyCode.E)) moveInput.y += 1;
        
        // 转换移动方向到相机空间
        Vector3 moveDirection = transform.TransformDirection(moveInput);
        targetPosition += moveDirection * moveSpeed * Time.deltaTime;
        
        // 处理旋转输入
        float mouseX = Input.GetAxis("Mouse X") * rotationSpeed;
        float mouseY = Input.GetAxis("Mouse Y") * rotationSpeed * (invertY ? 1 : -1);
        
        // 计算目标旋转
        Vector3 currentEuler = targetRotation.eulerAngles;
        currentEuler.x = ClampAngle(currentEuler.x + mouseY, -89f, 89f);
        currentEuler.y += mouseX;
        targetRotation = Quaternion.Euler(currentEuler);
        
        // 平滑应用变换
        transform.position = Vector3.Lerp(
            transform.position,
            targetPosition,
            Time.deltaTime * smoothness
        );
        transform.rotation = Quaternion.Slerp(
            transform.rotation,
            targetRotation,
            Time.deltaTime * smoothness
        );
    }
    
    float ClampAngle(float angle, float min, float max) 
    {
        if (angle < -360) angle += 360;
        if (angle > 360) angle -= 360;
        return Mathf.Clamp(angle, min, max);
    }
    
    void OnDisable() 
    {
        Cursor.lockState = CursorLockMode.None;
    }
}
```

## 十二. 粒子系统应用

### 12.1 螺旋粒子发射器
```csharp
public class SpiralParticleEmitter : MonoBehaviour 
{
    public int particlesPerSpiral = 50;
    public float spiralRadius = 3f;
    public float spiralHeight = 5f;
    public float rotationsPerSpiral = 2f;
    public float particleLifetime = 2f;
    public float emissionRate = 0.1f;
    public Color startColor = Color.white;
    public Color endColor = Color.clear;
    
    private ParticleSystem particleSystem;
    private float emissionTimer;
    
    void Start() 
    {
        InitializeParticleSystem();
    }
    
    void InitializeParticleSystem() 
    {
        particleSystem = gameObject.AddComponent<ParticleSystem>();
        var main = particleSystem.main;
        main.startLifetime = particleLifetime;
        main.startSize = 0.1f;
        main.startColor = startColor;
        main.simulationSpace = ParticleSystemSimulationSpace.World;
        
        var emission = particleSystem.emission;
        emission.enabled = false; // 我们将手动发射粒子
        
        var colorOverLifetime = particleSystem.colorOverLifetime;
        colorOverLifetime.enabled = true;
        
        Gradient gradient = new Gradient();
        gradient.SetKeys(
            new GradientColorKey[] { 
                new GradientColorKey(startColor, 0.0f),
                new GradientColorKey(endColor, 1.0f)
            },
            new GradientAlphaKey[] {
                new GradientAlphaKey(1.0f, 0.0f),
                new GradientAlphaKey(0.0f, 1.0f)
            }
        );
        colorOverLifetime.color = gradient;
    }
    
    void Update() 
    {
        emissionTimer += Time.deltaTime;
        if (emissionTimer >= emissionRate) 
        {
            EmitSpiralParticles();
            emissionTimer = 0f;
        }
    }
    
    void EmitSpiralParticles() 
    {
        for (int i = 0; i < particlesPerSpiral; i++) 
        {
            float t = (float)i / particlesPerSpiral;
            float angle = t * rotationsPerSpiral * 2f * Mathf.PI;
            float height = t * spiralHeight;
            
            // 使用圆柱坐标计算位置
            CylindricalCoordinate coord = new CylindricalCoordinate(
                spiralRadius,
                angle,
                height
            );
            
            Vector3 position = coord.ToCartesian() + transform.position;
            
            // 发射粒子
            var particle = new ParticleSystem.EmitParams();
            particle.position = position;
            particle.startColor = startColor;
            particleSystem.Emit(particle, 1);
        }
    }
} 

## 十三. 基础几何图元

### 13.1 3D点和向量操作
```csharp
public struct Point3D 
{
    public float x, y, z;
    
    // 计算两点之间的距离
    public float DistanceTo(Point3D other) 
    {
        float dx = other.x - x;
        float dy = other.y - y;
        float dz = other.z - z;
        return Mathf.Sqrt(dx * dx + dy * dy + dz * dz);
    }
    
    // 判断点是否在包围盒内
    public bool IsInBoundingBox(Point3D min, Point3D max) 
    {
        return x >= min.x && x <= max.x &&
               y >= min.y && y <= max.y &&
               z >= min.z && z <= max.z;
    }
}
```

### 13.2 射线和直线系统
```csharp
public class RaycastSystem : MonoBehaviour 
{
    public LayerMask collisionLayer;
    public float maxDistance = 100f;
    
    public bool CastRay(Vector3 origin, Vector3 direction, out RaycastHit hit) 
    {
        Ray ray = new Ray(origin, direction);
        return Physics.Raycast(ray, out hit, maxDistance, collisionLayer);
    }
    
    public bool SphereCast(Vector3 origin, float radius, Vector3 direction, out RaycastHit hit) 
    {
        return Physics.SphereCast(
            origin, radius, direction, out hit, maxDistance, collisionLayer
        );
    }
    
    public RaycastHit[] ConeDetection(Vector3 origin, Vector3 direction, float angle) 
    {
        // 创建锥形检测区域
        float radius = Mathf.Tan(angle * Mathf.Deg2Rad) * maxDistance;
        return Physics.SphereCastAll(
            origin, radius, direction, maxDistance, collisionLayer
        );
    }
}
```

## 十四. 碰撞检测系统

### 14.1 AABB碰撞检测
```csharp
public class AABBCollisionSystem 
{
    public struct AABB 
    {
        public Vector3 min;
        public Vector3 max;
        
        public AABB(Vector3 min, Vector3 max) 
        {
            this.min = min;
            this.max = max;
        }
        
        public bool Intersects(AABB other) 
        {
            return (min.x <= other.max.x && max.x >= other.min.x) &&
                   (min.y <= other.max.y && max.y >= other.min.y) &&
                   (min.z <= other.max.z && max.z >= other.min.z);
        }
        
        public bool Contains(Vector3 point) 
        {
            return point.x >= min.x && point.x <= max.x &&
                   point.y >= min.y && point.y <= max.y &&
                   point.z >= min.z && point.z <= max.z;
        }
        
        public AABB Merge(AABB other) 
        {
            return new AABB(
                Vector3.Min(min, other.min),
                Vector3.Max(max, other.max)
            );
        }
    }
}
```

### 14.2 OBB碰撞检测
```csharp
public class OBBCollisionSystem 
{
    public struct OBB 
    {
        public Vector3 center;
        public Vector3 extents;
        public Quaternion orientation;
        
        public Vector3[] GetCorners() 
        {
            Vector3[] corners = new Vector3[8];
            Vector3[] axes = new Vector3[3] {
                orientation * Vector3.right,
                orientation * Vector3.up,
                orientation * Vector3.forward
            };
            
            for (int i = 0; i < 8; i++) 
            {
                corners[i] = center;
                corners[i] += axes[0] * extents.x * ((i & 1) != 0 ? 1 : -1);
                corners[i] += axes[1] * extents.y * ((i & 2) != 0 ? 1 : -1);
                corners[i] += axes[2] * extents.z * ((i & 4) != 0 ? 1 : -1);
            }
            
            return corners;
        }
        
        public bool Intersects(OBB other) 
        {
            // 使用分离轴定理检测碰撞
            // 实现省略...
            return true;
        }
    }
}
```

## 十五. 3D建模工具

### 15.1 程序化网格生成
```csharp
public class ProceduralMeshGenerator 
{
    public static Mesh CreateCube(Vector3 size) 
    {
        Mesh mesh = new Mesh();
        
        // 顶点
        Vector3[] vertices = new Vector3[8];
        vertices[0] = new Vector3(-size.x, -size.y, -size.z);
        vertices[1] = new Vector3(size.x, -size.y, -size.z);
        vertices[2] = new Vector3(size.x, size.y, -size.z);
        vertices[3] = new Vector3(-size.x, size.y, -size.z);
        vertices[4] = new Vector3(-size.x, -size.y, size.z);
        vertices[5] = new Vector3(size.x, -size.y, size.z);
        vertices[6] = new Vector3(size.x, size.y, size.z);
        vertices[7] = new Vector3(-size.x, size.y, size.z);
        
        // 三角形
        int[] triangles = new int[] {
            0, 2, 1, 0, 3, 2, // 前面
            1, 2, 6, 1, 6, 5, // 右面
            5, 6, 7, 5, 7, 4, // 后面
            4, 7, 3, 4, 3, 0, // 左面
            3, 7, 6, 3, 6, 2, // 上面
            4, 0, 1, 4, 1, 5  // 下面
        };
        
        // UV坐标
        Vector2[] uvs = new Vector2[8];
        uvs[0] = new Vector2(0, 0);
        uvs[1] = new Vector2(1, 0);
        uvs[2] = new Vector2(1, 1);
        uvs[3] = new Vector2(0, 1);
        uvs[4] = new Vector2(0, 0);
        uvs[5] = new Vector2(1, 0);
        uvs[6] = new Vector2(1, 1);
        uvs[7] = new Vector2(0, 1);
        
        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.uv = uvs;
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();
        
        return mesh;
    }
}
```

### 15.2 曲面生成器
```csharp
public class SurfaceGenerator 
{
    public static Mesh CreateSphere(float radius, int segments) 
    {
        Mesh mesh = new Mesh();
        
        // 计算顶点数量
        int verticalSegments = segments;
        int horizontalSegments = segments * 2;
        int vertexCount = (verticalSegments + 1) * (horizontalSegments + 1);
        
        // 生成顶点
        Vector3[] vertices = new Vector3[vertexCount];
        Vector2[] uvs = new Vector2[vertexCount];
        int index = 0;
        
        for (int y = 0; y <= verticalSegments; y++) 
        {
            for (int x = 0; x <= horizontalSegments; x++) 
            {
                float xSegment = (float)x / horizontalSegments;
                float ySegment = (float)y / verticalSegments;
                float xPos = Mathf.Cos(xSegment * Mathf.PI * 2) * 
                           Mathf.Sin(ySegment * Mathf.PI);
                float yPos = Mathf.Cos(ySegment * Mathf.PI);
                float zPos = Mathf.Sin(xSegment * Mathf.PI * 2) * 
                           Mathf.Sin(ySegment * Mathf.PI);
                
                vertices[index] = new Vector3(xPos, yPos, zPos) * radius;
                uvs[index] = new Vector2(xSegment, ySegment);
                index++;
            }
        }
        
        // 生成三角形
        int[] triangles = new int[verticalSegments * horizontalSegments * 6];
        int triIndex = 0;
        
        for (int y = 0; y < verticalSegments; y++) 
        {
            for (int x = 0; x < horizontalSegments; x++) 
            {
                triangles[triIndex] = (y * (horizontalSegments + 1)) + x;
                triangles[triIndex + 1] = ((y + 1) * (horizontalSegments + 1)) + x;
                triangles[triIndex + 2] = (y * (horizontalSegments + 1)) + x + 1;
                triangles[triIndex + 3] = ((y + 1) * (horizontalSegments + 1)) + x;
                triangles[triIndex + 4] = ((y + 1) * (horizontalSegments + 1)) + x + 1;
                triangles[triIndex + 5] = (y * (horizontalSegments + 1)) + x + 1;
                triIndex += 6;
            }
        }
        
        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.uv = uvs;
        mesh.RecalculateNormals();
        
        return mesh;
    }
}
```

## 十六. 几何处理算法

### 16.1 三角形处理
```csharp
public class TriangleProcessor 
{
    // 计算三角形面积
    public static float CalculateArea(Vector3 v1, Vector3 v2, Vector3 v3) 
    {
        Vector3 cross = Vector3.Cross(v2 - v1, v3 - v1);
        return cross.magnitude * 0.5f;
    }
    
    // 计算重心坐标
    public static Vector3 CalculateBarycentricCoordinates(
        Vector3 point, Vector3 v1, Vector3 v2, Vector3 v3) 
    {
        Vector3 v0 = v2 - v1;
        Vector3 v1v = v3 - v1;
        Vector3 v2v = point - v1;
        
        float d00 = Vector3.Dot(v0, v0);
        float d01 = Vector3.Dot(v0, v1v);
        float d11 = Vector3.Dot(v1v, v1v);
        float d20 = Vector3.Dot(v2v, v0);
        float d21 = Vector3.Dot(v2v, v1v);
        
        float denom = d00 * d11 - d01 * d01;
        float v = (d11 * d20 - d01 * d21) / denom;
        float w = (d00 * d21 - d01 * d20) / denom;
        float u = 1.0f - v - w;
        
        return new Vector3(u, v, w);
    }
}
```

### 16.2 网格简化
```csharp
public class MeshSimplification 
{
    public struct Edge 
    {
        public int v1, v2;
        public float cost;
        
        public Edge(int v1, int v2, float cost) 
        {
            this.v1 = v1;
            this.v2 = v2;
            this.cost = cost;
        }
    }
    
    public static Mesh SimplifyMesh(Mesh mesh, float quality) 
    {
        // 实现省略...
        // 1. 计算每条边的代价
        // 2. 按代价排序
        // 3. 合并顶点
        // 4. 更新拓扑
        return mesh;
    }
}
```

## 十七. 空间分割系统

### 17.1 八叉树
```csharp
public class Octree 
{
    public class OctreeNode 
    {
        public AABB bounds;
        public List<GameObject> objects;
        public OctreeNode[] children;
        public bool isLeaf;
        
        public OctreeNode(AABB bounds) 
        {
            this.bounds = bounds;
            this.objects = new List<GameObject>();
            this.children = new OctreeNode[8];
            this.isLeaf = true;
        }
        
        public void Split() 
        {
            Vector3 center = (bounds.min + bounds.max) * 0.5f;
            Vector3 extents = (bounds.max - bounds.min) * 0.5f;
            
            // 创建8个子节点
            for (int i = 0; i < 8; i++) 
            {
                Vector3 min = bounds.min;
                Vector3 max = center;
                
                if ((i & 1) != 0) { min.x = center.x; max.x = bounds.max.x; }
                if ((i & 2) != 0) { min.y = center.y; max.y = bounds.max.y; }
                if ((i & 4) != 0) { min.z = center.z; max.z = bounds.max.z; }
                
                children[i] = new OctreeNode(new AABB(min, max));
            }
            
            isLeaf = false;
        }
    }
}
```

### 17.2 BSP树
```csharp
public class BSPTree 
{
    public class BSPNode 
    {
        public Plane3D splitPlane;
        public BSPNode front;
        public BSPNode back;
        public List<Triangle3D> triangles;
        
        public BSPNode(List<Triangle3D> triangles) 
        {
            this.triangles = triangles;
        }
        
        public void Split() 
        {
            // 选择最佳分割平面
            splitPlane = ChooseSplitPlane();
            
            List<Triangle3D> frontList = new List<Triangle3D>();
            List<Triangle3D> backList = new List<Triangle3D>();
            
            // 分割三角形
            foreach (Triangle3D tri in triangles) 
            {
                SplitTriangle(tri, splitPlane, frontList, backList);
            }
            
            // 创建子节点
            if (frontList.Count > 0) 
                front = new BSPNode(frontList);
            
            if (backList.Count > 0) 
                back = new BSPNode(backList);
            
            triangles.Clear();
        }
        
        private Plane3D ChooseSplitPlane() 
        {
            // 实现省略...
            return new Plane3D();
        }
        
        private void SplitTriangle(
            Triangle3D triangle, 
            Plane3D plane, 
            List<Triangle3D> frontList, 
            List<Triangle3D> backList) 
        {
            // 实现省略...
        }
    }
} 

## 十八. 高级粒子系统
### 18.1 GPU粒子系统
```csharp
public class GPUParticleSystem
{
    private struct Particle
    {
        public Vector3 position;
        public Vector3 velocity;
        public Vector4 color;
        public float size;
        public float life;
        public float rotation;
    }
    
    private ComputeShader computeShader;
    private ComputeBuffer particleBuffer;
    private int particleCount;
    
    public void Initialize(int count)
    {
        particleCount = count;
        
        // 创建计算缓冲区
        particleBuffer = new ComputeBuffer(
            count, 
            sizeof(float) * 13
        );
        
        // 初始化粒子
        Particle[] particles = new Particle[count];
        for (int i = 0; i < count; i++)
        {
            particles[i] = CreateRandomParticle();
        }
        
        particleBuffer.SetData(particles);
    }
    
    public void Update()
    {
        // 设置计算着色器参数
        computeShader.SetFloat("deltaTime", Time.deltaTime);
        computeShader.SetBuffer(0, "particles", particleBuffer);
        
        // 调度计算
        int threadGroups = Mathf.CeilToInt(particleCount / 256.0f);
        computeShader.Dispatch(0, threadGroups, 1, 1);
    }
    
    public void Render(Camera camera)
    {
        // 设置材质参数
        material.SetBuffer("particleBuffer", particleBuffer);
        material.SetMatrix("viewMatrix", camera.worldToCameraMatrix);
        material.SetMatrix("projectionMatrix", 
            camera.projectionMatrix);
        
        // 绘制粒子
        Graphics.DrawProcedural(
            material, 
            new Bounds(Vector3.zero, Vector3.one * 100),
            MeshTopology.Points, 
            particleCount
        );
    }
}
```

## 十九. 布料模拟
### 19.1 弹簧质点系统
```csharp
public class ClothSimulation
{
    private struct Vertex
    {
        public Vector3 position;
        public Vector3 oldPosition;
        public Vector3 velocity;
        public bool isFixed;
        public float mass;
    }
    
    private struct Spring
    {
        public int vertexA;
        public int vertexB;
        public float restLength;
        public float stiffness;
    }
    
    private Vertex[] vertices;
    private Spring[] springs;
    private Vector3 gravity = new Vector3(0, -9.81f, 0);
    private float damping = 0.01f;
    
    public void Initialize(int width, int height)
    {
        // 创建顶点网格
        vertices = new Vertex[width * height];
        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int index = y * width + x;
                vertices[index] = new Vertex
                {
                    position = new Vector3(x, height, y),
                    oldPosition = new Vector3(x, height, y),
                    mass = 1.0f,
                    isFixed = y == height - 1 // 固定顶部顶点
                };
            }
        }
        
        // 创建弹簧约束
        List<Spring> springList = new List<Spring>();
        
        // 结构弹簧
        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int index = y * width + x;
                
                if (x < width - 1)
                    AddSpring(springList, index, index + 1);
                    
                if (y < height - 1)
                    AddSpring(springList, index, index + width);
            }
        }
        
        // 剪切弹簧
        for (int y = 0; y < height - 1; y++)
        {
            for (int x = 0; x < width - 1; x++)
            {
                int index = y * width + x;
                AddSpring(springList, index, index + width + 1);
                AddSpring(springList, index + 1, index + width);
            }
        }
        
        springs = springList.ToArray();
    }
    
    private void AddSpring(
        List<Spring> springs, 
        int vertexA, 
        int vertexB)
    {
        float restLength = Vector3.Distance(
            vertices[vertexA].position,
            vertices[vertexB].position
        );
        
        springs.Add(new Spring
        {
            vertexA = vertexA,
            vertexB = vertexB,
            restLength = restLength,
            stiffness = 100.0f
        });
    }
    
    public void Update(float deltaTime)
    {
        // Verlet积分
        for (int i = 0; i < vertices.Length; i++)
        {
            if (vertices[i].isFixed) continue;
            
            Vector3 temp = vertices[i].position;
            Vector3 velocity = vertices[i].position - 
                vertices[i].oldPosition;
            
            vertices[i].position += velocity * (1.0f - damping) + 
                gravity * deltaTime * deltaTime;
            vertices[i].oldPosition = temp;
        }
        
        // 约束求解
        const int iterations = 5;
        for (int i = 0; i < iterations; i++)
        {
            SolveConstraints();
        }
    }
    
    private void SolveConstraints()
    {
        foreach (var spring in springs)
        {
            Vector3 delta = vertices[spring.vertexB].position - 
                vertices[spring.vertexA].position;
            float currentLength = delta.magnitude;
            float correction = (currentLength - spring.restLength) / 
                currentLength;
            
            if (!vertices[spring.vertexA].isFixed)
                vertices[spring.vertexA].position += 
                    delta * correction * 0.5f;
                    
            if (!vertices[spring.vertexB].isFixed)
                vertices[spring.vertexB].position -= 
                    delta * correction * 0.5f;
        }
    }
}
```

## 二十. 流体模拟
### 20.1 SPH流体模拟
```csharp
public class SPHFluid
{
    private struct Particle
    {
        public Vector3 position;
        public Vector3 velocity;
        public float density;
        public float pressure;
        public Vector3 force;
    }
    
    private Particle[] particles;
    private float smoothingLength;
    private float particleMass;
    private float restDensity;
    private float pressureConstant;
    private float viscosity;
    
    private Dictionary<Vector3Int, List<int>> grid;
    private float cellSize;
    
    public void Initialize(int particleCount)
    {
        particles = new Particle[particleCount];
        grid = new Dictionary<Vector3Int, List<int>>();
        
        // 初始化参数
        smoothingLength = 1.0f;
        particleMass = 1.0f;
        restDensity = 1000.0f;
        pressureConstant = 1000.0f;
        viscosity = 0.1f;
        cellSize = smoothingLength;
        
        // 初始化粒子
        for (int i = 0; i < particleCount; i++)
        {
            particles[i] = new Particle
            {
                position = Random.insideUnitSphere * 5,
                velocity = Vector3.zero,
                density = 0,
                pressure = 0,
                force = Vector3.zero
            };
        }
    }
    
    public void Update(float deltaTime)
    {
        UpdateGrid();
        CalculateDensityPressure();
        CalculateForces();
        IntegrateParticles(deltaTime);
    }
    
    private void UpdateGrid()
    {
        grid.Clear();
        
        for (int i = 0; i < particles.Length; i++)
        {
            Vector3Int cell = GetCell(particles[i].position);
            
            if (!grid.ContainsKey(cell))
                grid[cell] = new List<int>();
                
            grid[cell].Add(i);
        }
    }
    
    private Vector3Int GetCell(Vector3 position)
    {
        return new Vector3Int(
            Mathf.FloorToInt(position.x / cellSize),
            Mathf.FloorToInt(position.y / cellSize),
            Mathf.FloorToInt(position.z / cellSize)
        );
    }
    
    private void CalculateDensityPressure()
    {
        float h2 = smoothingLength * smoothingLength;
        
        for (int i = 0; i < particles.Length; i++)
        {
            float density = 0;
            Vector3Int cell = GetCell(particles[i].position);
            
            // 检查相邻格子
            for (int x = -1; x <= 1; x++)
            for (int y = -1; y <= 1; y++)
            for (int z = -1; z <= 1; z++)
            {
                Vector3Int nearCell = cell + new Vector3Int(x, y, z);
                
                if (!grid.ContainsKey(nearCell)) continue;
                
                foreach (int j in grid[nearCell])
                {
                    Vector3 rij = particles[i].position - 
                        particles[j].position;
                    float r2 = rij.sqrMagnitude;
                    
                    if (r2 < h2)
                    {
                        density += particleMass * 
                            Kernel(Mathf.Sqrt(r2), smoothingLength);
                    }
                }
            }
            
            particles[i].density = density;
            particles[i].pressure = pressureConstant * 
                (density - restDensity);
        }
    }
    
    private float Kernel(float r, float h)
    {
        if (r > h) return 0;
        
        float volume = Mathf.PI * Mathf.Pow(h, 6) / 64;
        return (1.0f / volume) * Mathf.Pow(h * h - r * r, 3);
    }
    
    private Vector3 KernelGradient(Vector3 r, float h)
    {
        float length = r.magnitude;
        if (length > h) return Vector3.zero;
        
        float scale = -945.0f / (32.0f * Mathf.PI * 
            Mathf.Pow(h, 9)) * Mathf.Pow(h * h - length * length, 2);
        return r * scale;
    }
    
    private void CalculateForces()
    {
        for (int i = 0; i < particles.Length; i++)
        {
            Vector3 force = Vector3.zero;
            Vector3Int cell = GetCell(particles[i].position);
            
            // 压力和粘性力
            for (int x = -1; x <= 1; x++)
            for (int y = -1; y <= 1; y++)
            for (int z = -1; z <= 1; z++)
            {
                Vector3Int nearCell = cell + new Vector3Int(x, y, z);
                
                if (!grid.ContainsKey(nearCell)) continue;
                
                foreach (int j in grid[nearCell])
                {
                    if (i == j) continue;
                    
                    Vector3 rij = particles[i].position - 
                        particles[j].position;
                    float length = rij.magnitude;
                    
                    if (length < smoothingLength)
                    {
                        // 压力力
                        Vector3 pressureForce = -rij.normalized * 
                            particleMass * 
                            (particles[i].pressure + 
                             particles[j].pressure) / 
                            (2 * particles[j].density) * 
                            KernelGradient(rij, smoothingLength).magnitude;
                        
                        // 粘性力
                        Vector3 viscosityForce = viscosity * 
                            particleMass * 
                            (particles[j].velocity - 
                             particles[i].velocity) / 
                            particles[j].density * 
                            KernelGradient(rij, smoothingLength).magnitude;
                        
                        force += pressureForce + viscosityForce;
                    }
                }
            }
            
            // 重力
            force += Vector3.down * 9.81f * particles[i].density;
            
            particles[i].force = force;
        }
    }
    
    private void IntegrateParticles(float deltaTime)
    {
        for (int i = 0; i < particles.Length; i++)
        {
            // 更新速度和位置
            particles[i].velocity += particles[i].force / 
                particles[i].density * deltaTime;
            particles[i].position += particles[i].velocity * deltaTime;
            
            // 边界处理
            HandleBoundaryCollisions(i);
        }
    }
    
    private void HandleBoundaryCollisions(int index)
    {
        const float BOUNDARY = 10.0f;
        const float DAMPING = 0.5f;
        
        Vector3 position = particles[index].position;
        Vector3 velocity = particles[index].velocity;
        
        if (Mathf.Abs(position.x) > BOUNDARY)
        {
            position.x = BOUNDARY * Mathf.Sign(position.x);
            velocity.x = -velocity.x * DAMPING;
        }
        
        if (Mathf.Abs(position.y) > BOUNDARY)
        {
            position.y = BOUNDARY * Mathf.Sign(position.y);
            velocity.y = -velocity.y * DAMPING;
        }
        
        if (Mathf.Abs(position.z) > BOUNDARY)
        {
            position.z = BOUNDARY * Mathf.Sign(position.z);
            velocity.z = -velocity.z * DAMPING;
        }
        
        particles[index].position = position;
        particles[index].velocity = velocity;
    }
}
```

## 二十一. 破碎效果
### 21.1 Voronoi分解
```csharp
public class VoronoiFracture
{
    public struct Cell
    {
        public Vector3 site;
        public List<Vector3> vertices;
        public List<int> triangles;
    }
    
    private List<Cell> cells;
    private Bounds bounds;
    
    public void GenerateFracture(
        Mesh mesh, 
        int cellCount, 
        float noiseScale)
    {
        cells = new List<Cell>();
        bounds = mesh.bounds;
        
        // 生成Voronoi站点
        List<Vector3> sites = GenerateRandomSites(cellCount);
        
        // 为每个顶点找到最近的站点
        Vector3[] vertices = mesh.vertices;
        int[] triangles = mesh.triangles;
        
        Dictionary<int, List<int>> cellTriangles = 
            new Dictionary<int, List<int>>();
            
        for (int i = 0; i < triangles.Length; i += 3)
        {
            Vector3 center = (vertices[triangles[i]] + 
                vertices[triangles[i + 1]] + 
                vertices[triangles[i + 2]]) / 3;
                
            int nearestSite = FindNearestSite(center, sites);
            
            if (!cellTriangles.ContainsKey(nearestSite))
                cellTriangles[nearestSite] = new List<int>();
                
            cellTriangles[nearestSite].Add(triangles[i]);
            cellTriangles[nearestSite].Add(triangles[i + 1]);
            cellTriangles[nearestSite].Add(triangles[i + 2]);
        }
        
        // 创建单元格网格
        for (int i = 0; i < sites.Count; i++)
        {
            if (!cellTriangles.ContainsKey(i))
                continue;
                
            Cell cell = new Cell
            {
                site = sites[i],
                vertices = new List<Vector3>(),
                triangles = new List<int>()
            };
            
            // 重建顶点和三角形
            Dictionary<int, int> vertexMap = 
                new Dictionary<int, int>();
            
            foreach (int oldTriIndex in cellTriangles[i])
            {
                if (!vertexMap.ContainsKey(oldTriIndex))
                {
                    vertexMap[oldTriIndex] = cell.vertices.Count;
                    cell.vertices.Add(vertices[oldTriIndex]);
                }
                
                cell.triangles.Add(vertexMap[oldTriIndex]);
            }
            
            cells.Add(cell);
        }
    }
    
    private List<Vector3> GenerateRandomSites(int count)
    {
        List<Vector3> sites = new List<Vector3>();
        
        for (int i = 0; i < count; i++)
        {
            Vector3 site = new Vector3(
                Random.Range(bounds.min.x, bounds.max.x),
                Random.Range(bounds.min.y, bounds.max.y),
                Random.Range(bounds.min.z, bounds.max.z)
            );
            
            sites.Add(site);
        }
        
        return sites;
    }
    
    private int FindNearestSite(Vector3 point, List<Vector3> sites)
    {
        int nearest = 0;
        float minDist = float.MaxValue;
        
        for (int i = 0; i < sites.Count; i++)
        {
            float dist = Vector3.Distance(point, sites[i]);
            if (dist < minDist)
            {
                minDist = dist;
                nearest = i;
            }
        }
        
        return nearest;
    }
}
```

## 二十二. 天气系统
### 22.1 体积云渲染
```csharp
public class VolumetricClouds
{
    private struct CloudData
    {
        public float density;
        public float temperature;
        public float humidity;
        public Vector3 windVelocity;
    }
    
    private const int GRID_SIZE = 64;
    private CloudData[,,] grid;
    private float cellSize = 100.0f;
    private Vector3 windDirection = Vector3.right;
    private float windSpeed = 10.0f;
    
    public void Initialize()
    {
        grid = new CloudData[GRID_SIZE, GRID_SIZE, GRID_SIZE];
        
        // 初始化云层数据
        for (int x = 0; x < GRID_SIZE; x++)
        for (int y = 0; y < GRID_SIZE; y++)
        for (int z = 0; z < GRID_SIZE; z++)
        {
            float height = y / (float)GRID_SIZE;
            
            grid[x, y, z] = new CloudData
            {
                density = GenerateBaseDensity(x, y, z),
                temperature = 20.0f - height * 40.0f,
                humidity = Mathf.Lerp(0.3f, 0.9f, height),
                windVelocity = windDirection * windSpeed
            };
        }
    }
    
    private float GenerateBaseDensity(int x, int y, int z)
    {
        float height = y / (float)GRID_SIZE;
        
        // 使用柏林噪声生成基础云层
        float baseNoise = Mathf.PerlinNoise(
            x * 0.1f,
            z * 0.1f
        );
        
        // 添加细节噪声
        float detailNoise = Mathf.PerlinNoise(
            x * 0.3f + 100,
            z * 0.3f + 100
        );
        
        // 高度衰减
        float heightFalloff = Mathf.Exp(-height * 2.0f);
        
        return Mathf.Clamp01(
            (baseNoise * 0.7f + detailNoise * 0.3f) * 
            heightFalloff
        );
    }
    
    public void Update(float deltaTime)
    {
        CloudData[,,] newGrid = new CloudData[GRID_SIZE, 
            GRID_SIZE, GRID_SIZE];
            
        // 模拟云层演变
        for (int x = 0; x < GRID_SIZE; x++)
        for (int y = 0; y < GRID_SIZE; y++)
        for (int z = 0; z < GRID_SIZE; z++)
        {
            CloudData cell = grid[x, y, z];
            
            // 应用风力
            Vector3 windOffset = cell.windVelocity * deltaTime;
            int newX = Mathf.RoundToInt(x + windOffset.x);
            int newZ = Mathf.RoundToInt(z + windOffset.z);
            
            newX = (newX + GRID_SIZE) % GRID_SIZE;
            newZ = (newZ + GRID_SIZE) % GRID_SIZE;
            
            // 温度对流
            float tempDiff = y < GRID_SIZE - 1 ? 
                grid[x, y + 1, z].temperature - cell.temperature : 0;
            cell.temperature += tempDiff * 0.1f * deltaTime;
            
            // 湿度扩散
            float humidityDiff = 0;
            if (x > 0) humidityDiff += 
                grid[x-1, y, z].humidity - cell.humidity;
            if (x < GRID_SIZE-1) humidityDiff += 
                grid[x+1, y, z].humidity - cell.humidity;
            if (z > 0) humidityDiff += 
                grid[x, y, z-1].humidity - cell.humidity;
            if (z < GRID_SIZE-1) humidityDiff += 
                grid[x, y, z+1].humidity - cell.humidity;
            
            cell.humidity += humidityDiff * 0.1f * deltaTime;
            
            // 云密度变化
            float densityChange = (cell.humidity - 0.5f) * 
                Mathf.Exp(-Mathf.Abs(cell.temperature)) * 
                deltaTime;
            cell.density = Mathf.Clamp01(
                cell.density + densityChange
            );
            
            newGrid[newX, y, newZ] = cell;
        }
        
        grid = newGrid;
    }
    
    public float SampleDensity(Vector3 worldPosition)
    {
        Vector3 gridPosition = worldPosition / cellSize;
        
        int x = Mathf.FloorToInt(gridPosition.x);
        int y = Mathf.FloorToInt(gridPosition.y);
        int z = Mathf.FloorToInt(gridPosition.z);
        
        if (x < 0 || x >= GRID_SIZE - 1 ||
            y < 0 || y >= GRID_SIZE - 1 ||
            z < 0 || z >= GRID_SIZE - 1)
            return 0;
            
        Vector3 fraction = gridPosition - 
            new Vector3(x, y, z);
            
        // 三线性插值
        return TrilinearInterpolation(
            grid[x, y, z].density,
            grid[x + 1, y, z].density,
            grid[x, y + 1, z].density,
            grid[x + 1, y + 1, z].density,
            grid[x, y, z + 1].density,
            grid[x + 1, y, z + 1].density,
            grid[x, y + 1, z + 1].density,
            grid[x + 1, y + 1, z + 1].density,
            fraction
        );
    }
    
    private float TrilinearInterpolation(
        float c000, float c100,
        float c010, float c110,
        float c001, float c101,
        float c011, float c111,
        Vector3 fraction)
    {
        float c00 = Mathf.Lerp(c000, c100, fraction.x);
        float c01 = Mathf.Lerp(c001, c101, fraction.x);
        float c10 = Mathf.Lerp(c010, c110, fraction.x);
        float c11 = Mathf.Lerp(c011, c111, fraction.x);
        
        float c0 = Mathf.Lerp(c00, c10, fraction.y);
        float c1 = Mathf.Lerp(c01, c11, fraction.y);
        
        return Mathf.Lerp(c0, c1, fraction.z);
    }
}
```

## 二十三. 刚体动力学系统
### 23.1 基础刚体系统
```csharp
public class RigidBody3D
{
    public Vector3 Position { get; private set; }
    public Quaternion Rotation { get; private set; }
    public Vector3 LinearVelocity { get; private set; }
    public Vector3 AngularVelocity { get; private set; }
    public float Mass { get; private set; }
    public Matrix3x3 InertiaTensor { get; private set; }
    
    public void ApplyForce(Vector3 force, Vector3 point)
    {
        // 计算线性加速度
        Vector3 linearAcceleration = force / Mass;
        LinearVelocity += linearAcceleration * Time.deltaTime;
        
        // 计算力矩和角加速度
        Vector3 torque = Vector3.Cross(point - Position, force);
        Vector3 angularAcceleration = InertiaTensor.Inverse * torque;
        AngularVelocity += angularAcceleration * Time.deltaTime;
    }
    
    public void Integrate(float deltaTime)
    {
        // 更新位置
        Position += LinearVelocity * deltaTime;
        
        // 更新旋转
        Quaternion angularRotation = new Quaternion(
            AngularVelocity.x * deltaTime,
            AngularVelocity.y * deltaTime,
            AngularVelocity.z * deltaTime,
            0
        );
        Rotation = (Rotation + (angularRotation * Rotation) * 0.5f).normalized;
    }
}
```

### 23.2 高级刚体特性
```csharp
public class AdvancedRigidBody : RigidBody3D
{
    private float restitution;
    private float friction;
    private Vector3 gravity = new Vector3(0, -9.81f, 0);
    
    public void ApplyGravity()
    {
        ApplyForce(Mass * gravity, Position);
    }
    
    public void HandleCollision(AdvancedRigidBody other, Vector3 normal, Vector3 point)
    {
        // 计算相对速度
        Vector3 relativeVel = LinearVelocity - other.LinearVelocity;
        
        // 计算冲量
        float normalVel = Vector3.Dot(relativeVel, normal);
        if (normalVel > 0) return; // 物体已经分离
        
        float j = -(1 + restitution) * normalVel;
        j /= 1/Mass + 1/other.Mass;
        
        // 应用冲量
        Vector3 impulse = j * normal;
        LinearVelocity += impulse / Mass;
        other.LinearVelocity -= impulse / other.Mass;
        
        // 处理摩擦力
        Vector3 tangent = relativeVel - (Vector3.Dot(relativeVel, normal) * normal);
        if(tangent.magnitude > 0.0001f)
        {
            tangent.Normalize();
            float jt = -Vector3.Dot(relativeVel, tangent);
            jt /= 1/Mass + 1/other.Mass;
            
            Vector3 frictionImpulse = friction * jt * tangent;
            LinearVelocity += frictionImpulse / Mass;
            other.LinearVelocity -= frictionImpulse / other.Mass;
        }
    }
}
```

## 二十四. 高级碰撞检测
### 24.1 分离轴定理（SAT）实现
```csharp
public class SATCollisionDetector
{
    public struct Projection
    {
        public float min, max;
    }
    
    public static bool TestCollision(ConvexHull hullA, ConvexHull hullB)
    {
        // 获取所有可能的分离轴
        List<Vector3> axes = GetSeparatingAxes(hullA, hullB);
        
        foreach(Vector3 axis in axes)
        {
            // 在轴上投影两个凸包
            Projection projA = Project(hullA, axis);
            Projection projB = Project(hullB, axis);
            
            // 检查投影是否重叠
            if(!OverlapOnAxis(projA, projB))
            {
                return false; // 找到分离轴，不相交
            }
        }
        
        return true; // 所有轴都重叠，存在碰撞
    }
    
    private static Projection Project(ConvexHull hull, Vector3 axis)
    {
        float min = float.MaxValue;
        float max = float.MinValue;
        
        foreach(Vector3 vertex in hull.vertices)
        {
            float proj = Vector3.Dot(vertex, axis);
            min = Mathf.Min(min, proj);
            max = Mathf.Max(max, proj);
        }
        
        return new Projection { min = min, max = max };
    }
    
    private static bool OverlapOnAxis(Projection projA, Projection projB)
    {
        return projA.max >= projB.min && projB.max >= projA.min;
    }
}
```

## 二十五. 约束求解系统
### 25.1 基础约束系统
```csharp
public abstract class Constraint
{
    protected RigidBody3D bodyA;
    protected RigidBody3D bodyB;
    
    public abstract void Solve();
    public abstract void Initialize();
}

public class DistanceConstraint : Constraint
{
    private float targetDistance;
    private float stiffness;
    
    public override void Solve()
    {
        Vector3 direction = bodyB.Position - bodyA.Position;
        float currentDistance = direction.magnitude;
        direction.Normalize();
        
        float error = currentDistance - targetDistance;
        Vector3 correction = direction * error * stiffness;
        
        bodyA.Position += correction * 0.5f;
        bodyB.Position -= correction * 0.5f;
    }
}
```

## 二十六. 连续碰撞检测
### 26.1 扫掠测试
```csharp
public class SweepTest
{
    public struct SweepResult
    {
        public float time;      // 碰撞时间 [0,1]
        public Vector3 point;   // 碰撞点
        public Vector3 normal;  // 碰撞法线
    }
    
    public static SweepResult SweepSpheres(
        Vector3 posA, float radiusA, Vector3 velocityA,
        Vector3 posB, float radiusB, Vector3 velocityB)
    {
        Vector3 relativeVel = velocityA - velocityB;
        Vector3 relativePos = posA - posB;
        float combinedRadius = radiusA + radiusB;
        
        // 求解二次方程
        float a = Vector3.Dot(relativeVel, relativeVel);
        float b = 2.0f * Vector3.Dot(relativeVel, relativePos);
        float c = Vector3.Dot(relativePos, relativePos) - 
                 combinedRadius * combinedRadius;
        
        float discriminant = b * b - 4.0f * a * c;
        
        if(discriminant < 0)
            return new SweepResult { time = float.MaxValue };
            
        float time = (-b - Mathf.Sqrt(discriminant)) / (2.0f * a);
        
        if(time < 0 || time > 1)
            return new SweepResult { time = float.MaxValue };
            
        Vector3 point = posA + velocityA * time;
        Vector3 normal = (point - (posB + velocityB * time)).normalized;
        
        return new SweepResult 
        {
            time = time,
            point = point,
            normal = normal
        };
    }
}
```

## 二十七. 物理引擎优化
### 27.1 空间分区系统
```csharp
public class OctreeNode
{
    public Bounds bounds;
    public List<RigidBody3D> objects;
    public OctreeNode[] children;
    private const int MAX_OBJECTS = 8;
    private const int MAX_DEPTH = 8;
    
    public void Insert(RigidBody3D obj)
    {
        if (!bounds.Contains(obj.Position))
            return;
            
        if (objects.Count < MAX_OBJECTS || depth >= MAX_DEPTH)
        {
            objects.Add(obj);
            return;
        }
        
        if (children == null)
            Split();
            
        foreach (var child in children)
            child.Insert(obj);
    }
    
    private void Split()
    {
        Vector3 center = bounds.center;
        Vector3 extents = bounds.extents * 0.5f;
        children = new OctreeNode[8];
        
        for (int i = 0; i < 8; i++)
        {
            Vector3 newCenter = center;
            newCenter.x += ((i & 1) == 0 ? -extents.x : extents.x);
            newCenter.y += ((i & 2) == 0 ? -extents.y : extents.y);
            newCenter.z += ((i & 4) == 0 ? -extents.z : extents.z);
            
            children[i] = new OctreeNode
            {
                bounds = new Bounds(newCenter, extents * 2),
                objects = new List<RigidBody3D>()
            };
        }
        
        // 重新分配现有对象
        foreach (var obj in objects)
            foreach (var child in children)
                child.Insert(obj);
                
        objects.Clear();
    }
}
```

## 二十八. 光线追踪系统
### 28.1 基础光线追踪器
```csharp
public class RayTracer
{
    public struct Ray
    {
        public Vector3 origin;
        public Vector3 direction;
        
        public Vector3 GetPoint(float t)
        {
            return origin + direction * t;
        }
    }
    
    public struct RayHit
    {
        public float distance;
        public Vector3 point;
        public Vector3 normal;
        public Material material;
    }
    
    public Color TraceRay(Ray ray, int depth)
    {
        if (depth <= 0) return Color.black;
        
        RayHit hit;
        if (!Scene.Intersect(ray, out hit))
            return GetEnvironmentColor(ray);
            
        // 计算直接光照
        Color directLight = CalculateDirectLighting(hit);
        
        // 计算反射
        Ray reflectedRay = new Ray
        {
            origin = hit.point + hit.normal * 0.001f,
            direction = Vector3.Reflect(ray.direction, hit.normal)
        };
        
        Color reflectedColor = TraceRay(reflectedRay, depth - 1);
        
        return directLight + reflectedColor * hit.material.reflectivity;
    }
    
    private Color CalculateDirectLighting(RayHit hit)
    {
        Color totalLight = Color.black;
        
        foreach (Light light in Scene.lights)
        {
            Vector3 lightDir = (light.position - hit.point).normalized;
            float diffuse = Mathf.Max(0, Vector3.Dot(hit.normal, lightDir));
            
            // 检查阴影
            Ray shadowRay = new Ray
            {
                origin = hit.point + hit.normal * 0.001f,
                direction = lightDir
            };
            
            if (!Scene.Intersect(shadowRay, out _))
                totalLight += light.color * diffuse;
        }
        
        return totalLight;
    }
}
```

### 28.2 路径追踪
```csharp
public class PathTracer : RayTracer
{
    public Color TracePath(Ray ray, int depth)
    {
        if (depth <= 0) return Color.black;
        
        RayHit hit;
        if (!Scene.Intersect(ray, out hit))
            return GetEnvironmentColor(ray);
            
        // 俄罗斯轮盘赌
        float survivalProbability = 0.8f;
        if (Random.value > survivalProbability)
            return Color.black;
            
        // 生成随机方向
        Vector3 randomDir = GenerateRandomDirection(hit.normal);
        Ray bounceRay = new Ray
        {
            origin = hit.point + hit.normal * 0.001f,
            direction = randomDir
        };
        
        Color incomingLight = TracePath(bounceRay, depth - 1);
        float cosTheta = Vector3.Dot(randomDir, hit.normal);
        
        return (hit.material.albedo * incomingLight * cosTheta) / 
               (survivalProbability * Mathf.PI);
    }
    
    private Vector3 GenerateRandomDirection(Vector3 normal)
    {
        // 在法线半球上生成随机方向
        float u1 = Random.value;
        float u2 = Random.value;
        
        float r = Mathf.Sqrt(u1);
        float theta = 2 * Mathf.PI * u2;
        
        float x = r * Mathf.Cos(theta);
        float y = r * Mathf.Sin(theta);
        float z = Mathf.Sqrt(1 - u1);
        
        // 将方向对齐到法线空间
        Vector3 tangent = Vector3.Cross(normal, 
            Mathf.Abs(normal.x) > 0.9f ? Vector3.up : Vector3.right);
        Vector3 bitangent = Vector3.Cross(normal, tangent);
        
        return (tangent * x + bitangent * y + normal * z).normalized;
    }
}
```

## 二十九. 全局光照
### 29.1 光照探针系统
```csharp
public class LightProbeSystem
{
    public struct ProbeData
    {
        public Vector3 position;
        public SphericalHarmonics3 sh;
    }
    
    private List<ProbeData> probes = new List<ProbeData>();
    
    public void BakeProbes()
    {
        foreach (var probe in probes)
        {
            SphericalHarmonics3 sh = new SphericalHarmonics3();
            
            // 在球面上采样
            for (int i = 0; i < 64; i++)
            {
                Vector3 dir = GetSphericalDirection(i);
                Color radiance = SampleEnvironment(probe.position, dir);
                
                // 投影到球谐函数
                sh.AddDirectionalLight(dir, radiance, 1.0f);
            }
            
            probe.sh = sh;
        }
    }
    
    public Color SampleProbes(Vector3 position, Vector3 normal)
    {
        // 找到最近的探针
        List<ProbeData> nearestProbes = FindNearestProbes(position);
        
        // 三线性插值
        Color result = Color.black;
        float totalWeight = 0;
        
        foreach (var probe in nearestProbes)
        {
            float weight = 1.0f / (position - probe.position).magnitude;
            totalWeight += weight;
            
            Color probeLight = probe.sh.EvaluateLight(normal);
            result += probeLight * weight;
        }
        
        return result / totalWeight;
    }
}
```

## 三十. 实时阴影
### 30.1 级联阴影贴图
```csharp
public class CascadedShadowMapping
{
    private struct Cascade
    {
        public Matrix4x4 viewProjection;
        public float splitDistance;
        public RenderTexture shadowMap;
    }
    
    private Cascade[] cascades;
    
    public void UpdateCascades(Camera camera)
    {
        float nearClip = camera.nearClipPlane;
        float farClip = camera.farClipPlane;
        int cascadeCount = cascades.Length;
        
        for (int i = 0; i < cascadeCount; i++)
        {
            // 计算分割距离
            float splitStart = i == 0 ? nearClip : 
                cascades[i-1].splitDistance;
            float splitEnd = i == cascadeCount-1 ? farClip :
                CalculateSplitDistance(nearClip, farClip, i, cascadeCount);
                
            cascades[i].splitDistance = splitEnd;
            
            // 计算包围盒
            Bounds bounds = CalculateCascadeBounds(camera, splitStart, splitEnd);
            
            // 设置阴影相机
            Matrix4x4 view = CalculateLightViewMatrix();
            Matrix4x4 proj = CalculateOrthographicProjection(bounds);
            cascades[i].viewProjection = proj * view;
        }
    }
    
    private float CalculateSplitDistance(
        float near, float far, int cascadeIndex, int cascadeCount)
    {
        float lambda = 0.75f;
        float ratio = cascadeIndex / (float)cascadeCount;
        
        float uniformSplit = near + (far - near) * ratio;
        float logarithmicSplit = near * Mathf.Pow(far/near, ratio);
        
        return logarithmicSplit * lambda + uniformSplit * (1 - lambda);
    }
    
    public void RenderShadowMaps(Light light)
    {
        foreach (var cascade in cascades)
        {
            // 设置阴影相机
            Graphics.SetRenderTarget(cascade.shadowMap);
            GL.Clear(true, true, Color.white);
            
            // 渲染场景到阴影贴图
            RenderShadowCasters(cascade.viewProjection);
        }
    }
}
```

## 三十一. PBR渲染
### 31.1 基于物理的材质系统
```csharp
public class PBRMaterial
{
    public Color albedo;
    public float metallic;
    public float roughness;
    public Vector3 normal;
    
    public Color CalculateBRDF(
        Vector3 lightDir, 
        Vector3 viewDir, 
        Color lightColor)
    {
        Vector3 halfVector = (lightDir + viewDir).normalized;
        
        float NdotL = Mathf.Max(0, Vector3.Dot(normal, lightDir));
        float NdotV = Mathf.Max(0, Vector3.Dot(normal, viewDir));
        float NdotH = Mathf.Max(0, Vector3.Dot(normal, halfVector));
        float HdotV = Mathf.Max(0, Vector3.Dot(halfVector, viewDir));
        
        // 菲涅尔项
        Color F0 = Color.Lerp(
            new Color(0.04f, 0.04f, 0.04f), 
            albedo, 
            metallic
        );
        Color F = FresnelSchlick(HdotV, F0);
        
        // 几何项
        float G = GeometrySmith(NdotV, NdotL);
        
        // 法线分布
        float D = DistributionGGX(NdotH);
        
        // 镜面反射项
        Color specular = (F * G * D) / 
            (4.0f * NdotV * NdotL + 0.001f);
            
        // 漫反射项
        Color kD = (Color.white - F) * (1 - metallic);
        Color diffuse = kD * albedo / Mathf.PI;
        
        return (diffuse + specular) * lightColor * NdotL;
    }
    
    private float DistributionGGX(float NdotH)
    {
        float a = roughness * roughness;
        float a2 = a * a;
        float NdotH2 = NdotH * NdotH;
        
        float nom = a2;
        float denom = NdotH2 * (a2 - 1.0f) + 1.0f;
        denom = Mathf.PI * denom * denom;
        
        return nom / denom;
    }
    
    private float GeometrySmith(float NdotV, float NdotL)
    {
        float r = roughness + 1.0f;
        float k = (r * r) / 8.0f;
        
        float ggx1 = NdotV / (NdotV * (1 - k) + k);
        float ggx2 = NdotL / (NdotL * (1 - k) + k);
        
        return ggx1 * ggx2;
    }
    
    private Color FresnelSchlick(float cosTheta, Color F0)
    {
        return F0 + (Color.white - F0) * 
            Mathf.Pow(1.0f - cosTheta, 5.0f);
    }
}
```

## 三十二. 后处理效果
### 32.1 屏幕空间环境光遮蔽
```csharp
public class SSAO
{
    private const int SAMPLE_COUNT = 64;
    private Vector3[] sampleKernel;
    private Texture2D noiseTexture;
    
    public void Initialize()
    {
        // 生成采样核心
        sampleKernel = new Vector3[SAMPLE_COUNT];
        for (int i = 0; i < SAMPLE_COUNT; i++)
        {
            Vector3 sample = new Vector3(
                Random.Range(-1f, 1f),
                Random.Range(-1f, 1f),
                Random.Range(0f, 1f)
            ).normalized;
            
            float scale = (float)i / SAMPLE_COUNT;
            scale = Mathf.Lerp(0.1f, 1.0f, scale * scale);
            sampleKernel[i] = sample * scale;
        }
        
        // 生成噪声纹理
        GenerateNoiseTexture();
    }
    
    public void Render(
        RenderTexture source, 
        RenderTexture destination,
        Camera camera)
    {
        Material ssaoMaterial = new Material(Shader.Find("Hidden/SSAO"));
        
        ssaoMaterial.SetVectorArray("_Samples", 
            Array.ConvertAll(sampleKernel, v => (Vector4)v));
        ssaoMaterial.SetTexture("_NoiseTex", noiseTexture);
        ssaoMaterial.SetMatrix("_ProjectionMatrix", 
            camera.projectionMatrix);
        
        Graphics.Blit(source, destination, ssaoMaterial);
    }
    
    private void GenerateNoiseTexture()
    {
        const int noiseSize = 4;
        noiseTexture = new Texture2D(noiseSize, noiseSize, 
            TextureFormat.RGB24, false);
        
        Color[] noiseData = new Color[noiseSize * noiseSize];
        for (int i = 0; i < noiseSize * noiseSize; i++)
        {
            Vector3 noise = new Vector3(
                Random.Range(-1f, 1f),
                Random.Range(-1f, 1f),
                0
            ).normalized;
            
            noiseData[i] = new Color(noise.x, noise.y, noise.z);
        }
        
        noiseTexture.SetPixels(noiseData);
        noiseTexture.Apply();
    }
}
```

## 三十三. 空间搜索算法
### 33.1 八叉树空间搜索
```csharp
public class OctreeSearch<T> where T : class
{
    public class OctreeNode
    {
        public Bounds bounds;
        public List<T> objects;
        public OctreeNode[] children;
        
        public OctreeNode(Bounds bounds)
        {
            this.bounds = bounds;
            this.objects = new List<T>();
        }
    }
    
    private OctreeNode root;
    private int maxDepth;
    private int maxObjectsPerNode;
    
    public List<T> SphereQuery(Vector3 center, float radius)
    {
        List<T> result = new List<T>();
        SphereQuery(root, center, radius, result);
        return result;
    }
    
    private void SphereQuery(
        OctreeNode node, 
        Vector3 center, 
        float radius, 
        List<T> result)
    {
        if (node == null) return;
        
        // 检查节点边界是否与球体相交
        if (!IntersectsSphere(node.bounds, center, radius))
            return;
            
        // 添加当前节点中的对象
        foreach (var obj in node.objects)
        {
            Vector3 objPos = GetObjectPosition(obj);
            if (Vector3.Distance(center, objPos) <= radius)
                result.Add(obj);
        }
        
        // 递归检查子节点
        if (node.children != null)
        {
            foreach (var child in node.children)
                SphereQuery(child, center, radius, result);
        }
    }
    
    private bool IntersectsSphere(Bounds bounds, Vector3 center, float radius)
    {
        // 计算包围盒到球心的最近点
        Vector3 closest = bounds.ClosestPoint(center);
        return Vector3.Distance(closest, center) <= radius;
    }
}
```

### 33.2 KD树搜索
```csharp
public class KDTree<T>
{
    public class KDNode
    {
        public Vector3 position;
        public T data;
        public KDNode left;
        public KDNode right;
        public int splitAxis;
        
        public KDNode(Vector3 position, T data, int splitAxis)
        {
            this.position = position;
            this.data = data;
            this.splitAxis = splitAxis;
        }
    }
    
    private KDNode root;
    
    public void Insert(Vector3 position, T data)
    {
        root = Insert(root, position, data, 0);
    }
    
    private KDNode Insert(
        KDNode node, 
        Vector3 position, 
        T data, 
        int depth)
    {
        if (node == null)
            return new KDNode(position, data, depth % 3);
            
        int axis = depth % 3;
        float compare = position[axis] - node.position[axis];
        
        if (compare < 0)
            node.left = Insert(node.left, position, data, depth + 1);
        else
            node.right = Insert(node.right, position, data, depth + 1);
            
        return node;
    }
    
    public List<T> FindNearest(Vector3 position, float maxDistance)
    {
        List<T> result = new List<T>();
        FindNearest(root, position, maxDistance, result);
        return result;
    }
    
    private void FindNearest(
        KDNode node, 
        Vector3 position, 
        float maxDistance, 
        List<T> result)
    {
        if (node == null) return;
        
        float distance = Vector3.Distance(position, node.position);
        if (distance <= maxDistance)
            result.Add(node.data);
            
        int axis = node.splitAxis;
        float delta = position[axis] - node.position[axis];
        
        // 递归搜索最可能包含近邻的子树
        KDNode first = delta < 0 ? node.left : node.right;
        KDNode second = delta < 0 ? node.right : node.left;
        
        FindNearest(first, position, maxDistance, result);
        
        // 如果可能在另一侧找到更近的点，也搜索另一侧
        if (Mathf.Abs(delta) <= maxDistance)
            FindNearest(second, position, maxDistance, result);
    }
}
```

## 三十四. 智能寻路系统
### 34.1 导航网格系统
```csharp
public class NavigationMesh
{
    public class Triangle
    {
        public Vector3[] vertices;
        public List<Triangle> neighbors;
        public Vector3 center;
        public Vector3 normal;
        
        public Triangle(Vector3[] vertices)
        {
            this.vertices = vertices;
            this.neighbors = new List<Triangle>();
            CalculateProperties();
        }
        
        private void CalculateProperties()
        {
            // 计算中心点
            center = (vertices[0] + vertices[1] + vertices[2]) / 3f;
            
            // 计算法线
            Vector3 edge1 = vertices[1] - vertices[0];
            Vector3 edge2 = vertices[2] - vertices[0];
            normal = Vector3.Cross(edge1, edge2).normalized;
        }
    }
    
    private List<Triangle> triangles;
    
    public List<Vector3> FindPath(Vector3 start, Vector3 end)
    {
        Triangle startTri = FindContainingTriangle(start);
        Triangle endTri = FindContainingTriangle(end);
        
        if (startTri == null || endTri == null)
            return null;
            
        // A*寻路
        List<Triangle> path = AStarSearch(startTri, endTri);
        
        // 路径平滑化
        return SmoothPath(path, start, end);
    }
    
    private List<Triangle> AStarSearch(Triangle start, Triangle end)
    {
        var openSet = new PriorityQueue<Triangle>();
        var closedSet = new HashSet<Triangle>();
        var cameFrom = new Dictionary<Triangle, Triangle>();
        var gScore = new Dictionary<Triangle, float>();
        var fScore = new Dictionary<Triangle, float>();
        
        openSet.Enqueue(start, 0);
        gScore[start] = 0;
        fScore[start] = Vector3.Distance(start.center, end.center);
        
        while (openSet.Count > 0)
        {
            Triangle current = openSet.Dequeue();
            
            if (current == end)
                return ReconstructPath(cameFrom, end);
                
            closedSet.Add(current);
            
            foreach (var neighbor in current.neighbors)
            {
                if (closedSet.Contains(neighbor))
                    continue;
                    
                float tentativeGScore = gScore[current] + 
                    Vector3.Distance(current.center, neighbor.center);
                    
                if (!gScore.ContainsKey(neighbor) || 
                    tentativeGScore < gScore[neighbor])
                {
                    cameFrom[neighbor] = current;
                    gScore[neighbor] = tentativeGScore;
                    fScore[neighbor] = gScore[neighbor] + 
                        Vector3.Distance(neighbor.center, end.center);
                        
                    if (!openSet.Contains(neighbor))
                        openSet.Enqueue(neighbor, fScore[neighbor]);
                }
            }
        }
        
        return null;
    }
    
    private List<Vector3> SmoothPath(
        List<Triangle> trianglePath, 
        Vector3 start, 
        Vector3 end)
    {
        List<Vector3> path = new List<Vector3> { start };
        Vector3 current = start;
        int lookAhead = 2;
        
        for (int i = 0; i < trianglePath.Count; i++)
        {
            // 尝试直接连接到更远的点
            for (int j = Mathf.Min(i + lookAhead, trianglePath.Count - 1); 
                 j > i; j--)
            {
                Vector3 target = j == trianglePath.Count - 1 ? 
                    end : trianglePath[j].center;
                    
                if (CanWalkDirectly(current, target, trianglePath))
                {
                    path.Add(target);
                    current = target;
                    i = j;
                    break;
                }
            }
        }
        
        if (path[path.Count - 1] != end)
            path.Add(end);
            
        return path;
    }
}
```

## 三十五. 行为决策系统
### 35.1 行为树系统
```csharp
public abstract class BehaviorNode
{
    public enum Status
    {
        Success,
        Failure,
        Running
    }
    
    public abstract Status Execute();
}

public class Sequence : BehaviorNode
{
    private List<BehaviorNode> children = new List<BehaviorNode>();
    private int currentChild = 0;
    
    public override Status Execute()
    {
        if (currentChild >= children.Count)
            return Status.Success;
            
        Status childStatus = children[currentChild].Execute();
        
        switch (childStatus)
        {
            case Status.Running:
                return Status.Running;
                
            case Status.Success:
                currentChild++;
                return currentChild >= children.Count ? 
                    Status.Success : Status.Running;
                    
            case Status.Failure:
                return Status.Failure;
                
            default:
                return Status.Success;
        }
    }
}

public class Selector : BehaviorNode
{
    private List<BehaviorNode> children = new List<BehaviorNode>();
    private int currentChild = 0;
    
    public override Status Execute()
    {
        if (currentChild >= children.Count)
            return Status.Failure;
            
        Status childStatus = children[currentChild].Execute();
        
        switch (childStatus)
        {
            case Status.Running:
                return Status.Running;
                
            case Status.Success:
                return Status.Success;
                
            case Status.Failure:
                currentChild++;
                return currentChild >= children.Count ? 
                    Status.Failure : Status.Running;
                    
            default:
                return Status.Failure;
        }
    }
}
```

## 三十六. 机器学习应用
### 36.1 强化学习系统
```csharp
public class QLearning
{
    private Dictionary<string, Dictionary<string, float>> QTable;
    private float learningRate = 0.1f;
    private float discountFactor = 0.9f;
    
    public string GetBestAction(string state)
    {
        if (!QTable.ContainsKey(state))
            return null;
            
        var actions = QTable[state];
        return actions.OrderByDescending(x => x.Value)
            .First().Key;
    }
    
    public void Learn(
        string state, 
        string action, 
        float reward, 
        string nextState)
    {
        // 确保状态存在于Q表中
        if (!QTable.ContainsKey(state))
            QTable[state] = new Dictionary<string, float>();
            
        if (!QTable.ContainsKey(nextState))
            QTable[nextState] = new Dictionary<string, float>();
            
        // 获取当前Q值
        float currentQ = QTable[state].ContainsKey(action) ? 
            QTable[state][action] : 0;
            
        // 获取下一状态的最大Q值
        float maxNextQ = QTable[nextState].Count > 0 ? 
            QTable[nextState].Values.Max() : 0;
            
        // 更新Q值
        float newQ = currentQ + learningRate * 
            (reward + discountFactor * maxNextQ - currentQ);
            
        QTable[state][action] = newQ;
    }
}
```

## 三十七. 神经网络在3D中的应用
### 37.1 3D姿态估计
```csharp
public class PoseEstimator
{
    private NeuralNetwork network;
    private const int INPUT_SIZE = 1024; // 32x32 深度图
    private const int OUTPUT_SIZE = 7;   // 位置(3) + 四元数(4)
    
    public struct Pose
    {
        public Vector3 position;
        public Quaternion rotation;
    }
    
    public Pose EstimatePose(float[] depthMap)
    {
        // 预处理深度图
        float[] processedInput = PreprocessDepthMap(depthMap);
        
        // 运行神经网络
        float[] output = network.Forward(processedInput);
        
        // 解析输出
        return ParseOutput(output);
    }
    
    private float[] PreprocessDepthMap(float[] depthMap)
    {
        float[] processed = new float[INPUT_SIZE];
        
        // 归一化
        float min = depthMap.Min();
        float max = depthMap.Max();
        
        for (int i = 0; i < depthMap.Length; i++)
        {
            processed[i] = (depthMap[i] - min) / (max - min);
        }
        
        return processed;
    }
    
    private Pose ParseOutput(float[] output)
    {
        Pose pose = new Pose();
        
        // 解析位置
        pose.position = new Vector3(
            output[0],
            output[1],
            output[2]
        );
        
        // 解析旋转（四元数）
        pose.rotation = new Quaternion(
            output[3],
            output[4],
            output[5],
            output[6]
        ).normalized;
        
        return pose;
    }
}
```