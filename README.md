
# ComfyUI-JG-GPT-Img2 插件 - AI剑歌

这是一个包含 GPT Image 2 相关节点的 ComfyUI 插件，支持百度翻译和提示词优化功能。

## 包含的节点

1. **GPT_Image_2_异步** - GPT Image 2 图像生成/编辑（文生图、图生图）
2. **GPT_Image_2_官方稳定版** - GPT Image 2 官方稳定版节点
3. **GPT_Image_2_官方4K** - GPT Image 2 官方 4K 版本
4. **GPT_Image_2_综合** - GPT Image 2 综合版（支持对话历史）
5. **GPT_智能对话** - GPT 智能对话节点
6. **⚔️ 提示词翻译/优化** - 翻译中文提示词为英文，或进行优化
7. **⚔️ 配置管理** - 查看配置状态和说明

## 安装方法

1. 将此文件夹复制到 ComfyUI 的 `custom_nodes` 目录中
2. 重启 ComfyUI

## 配置说明

### 1. 创建配置文件

1. 复制 `conf/jg_config.example.json` 为 `conf/jg_config.json`
2. 填入你的 API 密钥：

```json
{
  "baidu_translate": {
    "APP_ID": "你的百度翻译API APP_ID",
    "SECRET_KEY": "你的百度翻译API SECRET_KEY",
    "timeout": 10
  },
  "prompt_optimize": {
    "api_key": "你的GPT提示词优化API密钥",
    "base_url": "https://api.bltcy.ai",
    "model": "gpt-4o-mini",
    "timeout": 30
  }
}
```

### 2. 获取 API 密钥

- **百度翻译 API**：访问 https://fanyi-api.baidu.com/
  - 注册并登录百度翻译开放平台
  - 创建应用获取 APP_ID 和 SECRET_KEY

- **提示词优化 API**：可使用柏拉图 API 或其他兼容的 GPT API
  - 可以直接使用已有的 GPT API Key（和节点中相同的 Key

### 3. 验证配置

在 ComfyUI 中使用 **⚔️ 配置管理节点查看配置状态。

## 使用说明

### API 线路选择

- **柏拉图** - 默认推荐
- **zhenzhen** - 备用线路
- **hk** - 香港线路
- **us** - 美国线路
- **ip** - 自定义地址（需要在"自定义API地址"字段填写）

### 提示词翻译/优化

使用 **⚔️ 提示词翻译/优化节点：

1. **translate** - 仅翻译中文到英文
2. **optimize** - 优化提示词
3. **both** - 先翻译，再优化

### 主要功能

- **文生图** - 根据提示词生成图像
- **图生图** - 根据参考图和提示词编辑图像
- **支持多参考图** - 可以输入多达16张参考图（官方4K节点）
- **遮罩支持** - 支持遮罩编辑
- **多种尺寸选项** - 支持多种分辨率和宽高比
- **种子控制** - 支持固定种子和随机种子

### 节点分类

所有节点在 ComfyUI 的节点菜单中分类为 `🤖GPT-Image-2`。

## 依赖项

- requests
- Pillow
- torch
- numpy

这些依赖项通常已经包含在 ComfyUI 的安装中。如果遇到缺少依赖项的问题，请运行：

```bash
pip install -r requirements.txt
```

## 版本

1.0.0
