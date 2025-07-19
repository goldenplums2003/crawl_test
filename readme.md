# CaptchaSolver 验证码解决工具

## 功能概述
这个类提供了自动化解决验证码的功能，支持通过ChatGPT和豆包AI解决点击坐标验证码和输入字符验证码。

## 方法说明

### `ask_gpt_captcha(captcha_img_path, width, height)`
- 功能：通过ChatGPT解决点击坐标验证码
- 参数：
  - captcha_img_path: 验证码图片路径
  - width: 图片宽度
  - height: 图片高度
- 返回：坐标列表，格式如[(x1,y1),(x2,y2)]

### `ask_doubao_click_captcha(captcha_img_path)`
- 功能：通过豆包AI解决点击坐标验证码
- 参数：captcha_img_path - 验证码图片路径
- 返回：坐标列表，格式如[(x1,y1),(x2,y2)]

### `ask_doubao_input_captcha(captcha_img_path)`
- 功能：通过豆包AI解决输入字符验证码
- 参数：captcha_img_path - 验证码图片路径
- 返回：识别出的字符

### `close()`
- 功能：关闭浏览器标签页

## 使用示例

```python
solver = CaptchaSolver()

# 解决点击坐标验证码
coordinates = solver.ask_doubao_click_captcha('captcha.png')
print(coordinates)

# 解决字符验证码 
chars = solver.ask_doubao_input_captcha('char_captcha.png')
print(chars)

solver.close()
```

## 依赖要求
- Python 3.6+
- DrissionPage库

## 注意事项
1. 使用前需要确保能访问ChatGPT或豆包AI网站
2. 可能需要登录账号
3. 验证码识别准确率取决于AI模型

---

# English README

## CaptchaSolver Class

### Overview
This class provides automated CAPTCHA solving functionality, supporting both coordinate-click and character-input CAPTCHAs via ChatGPT and Doubao AI.

### Methods

#### `ask_gpt_captcha(captcha_img_path, width, height)`
- Purpose: Solve coordinate-click CAPTCHA using ChatGPT
- Parameters:
  - captcha_img_path: Path to CAPTCHA image
  - width: Image width
  - height: Image height
- Returns: List of coordinates in format [(x1,y1),(x2,y2)]

#### `ask_doubao_click_captcha(captcha_img_path)`
- Purpose: Solve coordinate-click CAPTCHA using Doubao AI
- Parameter: captcha_img_path - Path to CAPTCHA image
- Returns: List of coordinates in format [(x1,y1),(x2,y2)]

#### `ask_doubao_input_captcha(captcha_img_path)`
- Purpose: Solve character-input CAPTCHA using Doubao AI
- Parameter: captcha_img_path - Path to CAPTCHA image
- Returns: Recognized characters

#### `close()`
- Purpose: Close browser tab

### Usage Example

```python
solver = CaptchaSolver()

# Solve coordinate CAPTCHA
coordinates = solver.ask_doubao_click_captcha('captcha.png')
print(coordinates)

# Solve character CAPTCHA
chars = solver.ask_doubao_input_captcha('char_captcha.png')
print(chars)

solver.close()
```

### Requirements
- Python 3.6+
- DrissionPage library

### Notes
1. Ensure access to ChatGPT or Doubao AI websites
2. May require logged-in accounts
3. Accuracy depends on AI models