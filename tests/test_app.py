import pytest
from app.app import dedupe, add  # 导入主程序函数

# 文档要求：包含去重功能测试
def test_dedupe():
    """测试去重函数"""
    assert dedupe([1, 2, 2, 3]) == [1, 2, 3]  # 基础去重验证
    assert dedupe([]) == []  # 空列表验证
    assert dedupe([5, 5, 5]) == [5]  # 单元素重复验证

# 后续功能测试：新增加法功能测试（对应 feature 分支）
def test_add():
    """测试加法函数（示例新增测试）"""
    assert add(2, 3) == 5  # 正整数加法验证
    assert add(-1, 1) == 0  # 正负整数加法验证
    assert add(0, 0) == 0   # 零值加法验证