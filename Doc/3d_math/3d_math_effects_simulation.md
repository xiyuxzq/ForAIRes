# 3D数学在特殊效果和模拟系统中的应用

## 目录
1. 高级粒子系统
2. 布料模拟
3. 流体模拟
4. 破碎效果
5. 天气系统

## 1. 高级粒子系统
### 1.1 GPU粒子系统
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

## 2. 布料模拟
### 2.1 弹簧质点系统
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

## 3. 流体模拟
### 3.1 SPH流体模拟
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

## 4. 破碎效果
### 4.1 Voronoi分解
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

## 5. 天气系统
### 5.1 体积云渲染
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