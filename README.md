# 小红书小工具工作台

一个可复用的 Codex / Claude Code 技能：制作离线 H5 小工具、修改现有产品、校验与打包。附带可直接使用的「图片转拼豆图纸」模板。

这不是小红书官方技能。平台约束始终以当前上传页改写口令、对应官方 skill 和在线文档为准。本仓库不重新分发官方 skill。

## 安装

将整个仓库作为一个技能目录安装，不要只复制 SKILL.md：

```sh
# Codex
git clone https://github.com/icoresss/xhs-minitool-studio.git ~/.codex/skills/xhs-minitool-studio

# Claude Code：在目标项目中安装
git clone https://github.com/icoresss/xhs-minitool-studio.git .claude/skills/xhs-minitool-studio
```

私有仓库需要有访问权限的 GitHub 登录。已存在目录时不要覆盖，先检查现有技能。

## 使用

```text
用 $xhs-minitool-studio 做一个拼豆配色小助手：
上传图片，生成编号图纸，统计每色用量，并输出小红书可上传的 ZIP。
```

也可以提供已有项目路径，只做兼容修复和打包。准备好上传页的最新完整改写口令，技能会按它执行官方规范核对。

## 不通过 AI 也能试用模板

需要 Python 3.8+，仅用标准库。以下命令在本仓库根目录运行，输出目录必须是全新的：

```sh
python scripts/new_tool.py --output ../my-bead-tool --title "拼豆配色小助手"
python scripts/pack_tool.py --source ../my-bead-tool --output ../my-bead-tool.zip --report ../my-bead-tool-preflight.json
python scripts/test_pack.py
```

普通浏览器可打开生成目录内的 index.html 试用界面；相册保存等需要小红书容器。浏览器内的保存按钮在无平台接口时显示完整图纸预览。

## 拼豆模板

- 48 色通用参考色，4–24 色上限，保持图片比例。
- 长边 24–80 格，边缘白底去除、透明像素留空。
- 拼豆预览、编号图纸、颜色定位、用量与尺寸估算。
- 图纸保存到相册，单份本机草稿，平台缓存升级迁移。
- 无联网依赖、无需 API key、无构建依赖，使用经典 JavaScript 和 Canvas 2D。

P 编号属于模板自身，并非任何品牌官方色号。默认素材是通用小花；用户角色和其他项目资料不在本仓库中。

## 验证边界

打包脚本检查结构、静态资源、常见禁用模式及包体，不能解析全部 JavaScript/CSS 语义，也不能代替官方审计或真机验收。交付后需用同一 ZIP 完成创服平台模拟器、Android 真机与 iOS 真机扫码验证。Chrome 61 与真机性能尚未实测。

源码与通用模板使用 MIT 许可证。第三方官方技能及文档不属于此许可证授权范围。
