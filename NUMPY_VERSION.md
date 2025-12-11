# NumPy 版本说明

## 为什么使用 NumPy 1.x 而不是 2.x？

### 兼容性问题

1. **PyTorch 2.2.2 的限制**
   - PyTorch 2.2.2 发布于 NumPy 2.0 之前
   - 编译时链接了旧的 NumPy C API (`PyArray_API`)
   - NumPy 2.0 移除了这个 API，导致运行时错误
   - 可能出现：`RuntimeError: module compiled against NumPy 1.x but running with NumPy 2.x`
   - 可能出现：`UserWarning: Failed to initialize NumPy: _ARRAY_API not found`

2. **NumPy 2.0 的破坏性变更**
   - **C API 变更**: 移除了 `PyArray_API` 结构
   - **数据类型系统**: 某些数据类型行为改变
   - **数组接口**: `__array_interface__` 实现变化
   - **内存共享**: 数组共享机制可能失效

3. **其他依赖库**
   - `numba` 和 `llvmlite` 对 NumPy 版本有特定要求
   - 某些库可能尚未完全支持 NumPy 2.0+

详细问题说明请查看 [NUMPY_COMPATIBILITY_ISSUES.md](NUMPY_COMPATIBILITY_ISSUES.md)

### 当前推荐版本

**NumPy 1.26.4**（1.x 系列最新版本）
- ✅ 与 PyTorch 2.2.2 完全兼容
- ✅ 性能稳定，功能完整
- ✅ 所有依赖库都支持
- ✅ 无兼容性警告

### 版本要求

```txt
numpy>=1.21.0,<2.0
```

这意味着：
- 最低版本：1.21.0
- 最高版本：< 2.0（即 1.26.4 是最新的 1.x 版本）
- 推荐版本：1.26.4

### 如何升级到最新 1.x 版本

```bash
pip install "numpy>=1.26.0,<2.0"
```

### 未来升级路径

如果将来要使用 NumPy 2.0+：

1. **升级 PyTorch**
   ```bash
   pip install torch>=2.3.0  # 或更新版本，支持 NumPy 2.0+
   ```

2. **更新所有依赖**
   - 确保所有依赖库都支持 NumPy 2.0+
   - 测试所有功能是否正常

3. **更新 requirements.txt**
   ```txt
   numpy>=2.0.0
   ```

### 参考资源

- [NumPy 2.0 迁移指南](https://numpy.org/devdocs/numpy_2_0_migration_guide.html)
- [PyTorch 与 NumPy 兼容性](https://pytorch.org/docs/stable/notes/compatibility.html)

