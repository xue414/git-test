# 文档要求：包含之前练习的去重逻辑（dedupe 函数）
def dedupe(lst):
    """列表去重函数"""
    return list(set(lst))  # 基础去重逻辑（可根据实际需求优化）

# 后续功能开发示例：新增加法功能（对应 feature/add-addition-functionality 分支）
def add(a, b):
    """加法功能函数（示例新增功能）"""
    return a + b

# 程序入口（验证功能）
if __name__ == "__main__":
    print("去重结果：", dedupe([1, 2, 2, 3, 3]))  # 输出：[1,2,3]（顺序可能不同）
    print("加法结果：", add(2, 3))  # 输出：5（新增功能验证）