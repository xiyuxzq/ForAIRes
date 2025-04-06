# 3D数学实际应用案例集合（第二部分）

## 目录
1. 极坐标系统应用
2. 球坐标系统应用
3. 圆柱坐标系统应用
4. 3D旋转应用
5. 高级相机系统
6. 粒子系统应用

## 1. 极坐标系统应用

### 1.1 基础极坐标系统
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

### 1.2 环形运动系统
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

### 1.3 雷达扫描效果
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

## 2. 球坐标系统应用

### 2.1 球坐标基础系统
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

### 2.2 高级轨道相机
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

## 3. 圆柱坐标系统应用

### 3.1 圆柱坐标基础系统
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

### 3.2 螺旋楼梯生成器
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

## 4. 3D旋转应用

### 4.1 欧拉角旋转系统
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

### 4.2 四元数旋转插值
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

## 5. 高级相机系统

### 5.1 自由视角相机
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

## 6. 粒子系统应用

### 6.1 螺旋粒子发射器
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