# 小红书小工具工作台

把想法做成离线 H5 小工具，生成小红书创服平台可上传的代码 ZIP。附带「图片转拼豆图纸」模板，可直接修改，也可以作为其他工具的起点。

**v1.0.1 · 预览版**

[中文上手教程](docs/quickstart.md) · [常见问题](docs/quickstart.md#常见问题) · [版本记录](CHANGELOG.md)

[下载 v1.0.1](https://github.com/icoresss/xhs-minitool-studio/releases/tag/v1.0.1)

| 下载文件 | 用途 |
| --- | --- |
| `xhs-minitool-studio-1.0.1.zip` | 技能安装包，解压后将 xhs-minitool-studio 文件夹放入技能目录 |
| `bead-helper-template-1.0.1.zip` | 拼豆小工具示例，用于本地试用和小红书部署 |
| `SHA256SUMS.txt` | 两个 ZIP 的 SHA256 校验值 |

本项目为社区工具。小红书平台接入要求请参考[官方文档](https://miniapp-sandbox.xiaohongshu.com/minitool/doc)。

## 实际效果

小花示例：40 × 40 格，12 色，494 颗豆。

![拼豆小工具桌面操作界面](docs/images/desktop-preview.png)

| 输入图片 | 实际导出的编号图纸 |
| --- | --- |
| <img src="docs/images/sample-input.png" alt="32×32小花输入图片" width="180"> | <img src="docs/images/sample-chart.png" alt="40×40编号图纸与逐色用量" width="340"> |

手机布局与编号视图见[完整教程](docs/quickstart.md#使用拼豆小工具)。

## 安装 skill

克隆仓库，或下载技能安装包，将 xhs-minitool-studio 文件夹放入对应技能目录。

Codex 个人技能目录为 `~/.agents/skills/`。

Windows PowerShell：

```powershell
git clone https://github.com/icoresss/xhs-minitool-studio.git "$env:USERPROFILE/.agents/skills/xhs-minitool-studio"
```

macOS / Linux：

```sh
git clone https://github.com/icoresss/xhs-minitool-studio.git ~/.agents/skills/xhs-minitool-studio
```

Claude Code：在目标项目目录运行。

```sh
git clone https://github.com/icoresss/xhs-minitool-studio.git .claude/skills/xhs-minitool-studio
```

通过 Git 安装后，可在技能目录中运行 `git pull` 更新。

更多安装选项见 [Codex 官方说明](https://developers.openai.com/codex/skills) 和 [Claude Code 官方说明](https://code.claude.com/docs/en/skills)。

## 使用

```text
用 $xhs-minitool-studio 做一个拼豆配色小助手。
保留图片转图纸、配色用量和相册保存，项目写到我指定的新目录。
生成编号图纸，统计每色用量，并输出可部署的代码 ZIP。
```

也可以提供已有项目路径，只做兼容修复和打包。准备好上传页的最新完整改写口令，技能会按它执行官方规范核对。

上面的 `$` 调用适用于 Codex CLI/IDE；其他桌面界面使用自身的技能选择器。Claude Code 可使用 `/xhs-minitool-studio` 再描述需求。

## 直接运行模板

需要 Python 3.8+；脚本仅使用标准库。以下命令在仓库根目录运行，输出目录与文件需尚不存在：

```sh
python scripts/new_tool.py --output ../my-bead-tool --title "拼豆配色小助手"
python scripts/pack_tool.py --source ../my-bead-tool --output ../bead-helper-1.0.1.zip --report ../bead-helper-1.0.1-preflight.json
```

普通浏览器可打开生成目录内的 index.html 试用界面；相册保存等需要小红书容器。浏览器内的保存按钮在无平台接口时显示完整图纸预览。

如系统使用 `python3` 或 `py -3`，请将上述 `python` 替换成可用命令。最终上传前仍需按官方 skill 校验。

## 拼豆模板

- 48 色通用参考色，4–24 色上限，保持图片比例。
- 长边 24–80 格，边缘白底去除、透明像素留空。
- 拼豆预览、编号图纸、颜色定位、用量与尺寸估算。
- 图纸保存到相册，保存和恢复本机草稿。
- 无联网依赖、无需 API key、无构建依赖，使用经典 JavaScript 和 Canvas 2D。

P01–P48 为通用参考编号，购买拼豆时请对照实物色卡。

## 兼容性

预览版，创服平台、Android/iOS 真机及 Chrome 61 兼容性尚待验证。部署方法和常见问题见[中文教程](docs/quickstart.md#上传到小红书)。

## 反馈与贡献

遇到问题请提交 [Issue](https://github.com/icoresss/xhs-minitool-studio/issues)。参与开发请阅读[贡献说明](CONTRIBUTING.md)。

源码与通用模板使用 MIT 许可证。第三方官方技能及文档不属于此许可证授权范围。
