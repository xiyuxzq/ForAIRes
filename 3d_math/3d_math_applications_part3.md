# 3D数学实际应用案例集合（第三部分）

## 目录
1. 基础几何图元
2. 碰撞检测系统
3. 3D建模工具
4. 几何处理算法
5. 空间分割系统

## 1. 基础几何图元

### 1.1 3D点和向量操作
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

### 1.2 射线和直线系统
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

## 2. 碰撞检测系统

### 2.1 AABB碰撞检测
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

### 2.2 OBB碰撞检测
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

## 3. 3D建模工具

### 3.1 程序化网格生成
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

### 3.2 曲面生成器
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

## 4. 几何处理算法

### 4.1 三角形处理
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

### 4.2 网格简化
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

## 5. 空间分割系统

### 5.1 八叉树
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

### 5.2 BSP树
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
``` 