# 3D数学在人工智能和机器学习中的应用

## 目录
1. 空间搜索算法
2. 智能寻路系统
3. 行为决策系统
4. 机器学习应用
5. 神经网络在3D中的应用

## 1. 空间搜索算法
### 1.1 八叉树空间搜索
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

### 1.2 KD树搜索
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

## 2. 智能寻路系统
### 2.1 导航网格系统
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

## 3. 行为决策系统
### 3.1 行为树系统
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

## 4. 机器学习应用
### 4.1 强化学习系统
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

## 5. 神经网络在3D中的应用
### 5.1 3D姿态估计
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