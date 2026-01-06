# LoongCodium

Making VSCodium extensions work on LoongArch! We test extensions for compatibility and port them when necessary.

> [!NOTE]
> All extensions listed are from [Open VSX Registry](https://open-vsx.org/), which is the default marketplace for VSCodium.

## Extension Status

### Status Explanations
- **✅ Working**: Natively supported on LoongArch; works out of the box or with minimal required setup.
- **🚀 Ported**: Official extension not supported, but a community-ported build for LoongArch is functional.
- **🔄 Alternative**: Original extension incompatible; a reliable drop-in replacement is available.
- **😭 Not Working**: Unsupported on LoongArch with no viable alternatives at this time.

| Extension Name | Status | Notes | Latest Version |
|----------------|--------|-------|----------------|
| [clangd](https://open-vsx.org/extension/llvm-vs-code-extensions/vscode-clangd) | ✅ Working | Requires `clangd` to be installed on the system beforehand. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/llvm-vs-code-extensions/vscode-clangd&query=$.version&label=&color=brightgreen) |
| [CodeLLDB](https://open-vsx.org/extension/vadimcn/vscode-lldb) | 🔄 Alternative | Use [LLDB DAP](https://open-vsx.org/extension/llvm-vs-code-extensions/lldb-dap) or [Native Debug](https://open-vsx.org/extension/webfreak/debug) instead. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/llvm-vs-code-extensions/lldb-dap&query=$.version&label=LLDB%20DAP&color=blue) ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/webfreak/debug&query=$.version&label=Native%20Debug&color=blue) |
| [ESLint](https://open-vsx.org/extension/dbaeumer/vscode-eslint) |  ✅ Working | Works out of the box. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/dbaeumer/vscode-eslint&query=$.version&label=&color=brightgreen) |
| [Even Better TOML](https://open-vsx.org/extension/tamasfe/even-better-toml) | ✅ Working | Once installed, configure `Bundled` to `false`. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/tamasfe/even-better-toml&query=$.version&label=&color=brightgreen) |
| [Go](https://open-vsx.org/extension/golang/Go) | ✅ Working | Works out of the box, automatically installs related binaries. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/golang/Go&query=$.version&label=&color=brightgreen) |
| [Jupyter](https://open-vsx.org/extension/ms-toolsai/jupyter) | ✅ Working | Works out of the box. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/ms-toolsai/jupyter&query=$.version&label=&color=brightgreen) |
| Pylance | 🔄 Alternative | Use [BasedPyright](https://open-vsx.org/extension/detachhead/basedpyright) instead. See this [discussion](https://github.com/VSCodium/vscodium/discussions/1641). | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/detachhead/basedpyright&query=$.version&label=&color=blue) |
| [Pylint](https://open-vsx.org/extension/ms-python/pylint) | ✅ Working | Works out of the box. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/ms-python/pylint&query=$.version&label=&color=brightgreen) |
| [Python](https://open-vsx.org/extension/ms-python/python) | ✅ Working | Works out of the box. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/ms-python/python&query=$.version&label=&color=brightgreen) |
| [Python Debugger](https://open-vsx.org/extension/ms-python/debugpy) | 🚀 Ported | Use [Python Debugger for LoongArch](https://open-vsx.org/extension/wubzbz/debugpy) instead. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/wubzbz/debugpy&query=$.version&label=&color=teal) |
| [Python Environments](https://open-vsx.org/extension/ms-python/vscode-python-envs) | ✅ Working | Works out of the box. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/ms-python/vscode-python-envs&query=$.version&label=&color=brightgreen) |
| Remote - SSH | 🔄 Alternative | Use [Open Remote - SSH](https://open-vsx.org/extension/jeanp413/open-remote-ssh) instead. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/jeanp413/open-remote-ssh&query=$.version&label=&color=blue) |
| [Ruff](https://open-vsx.org/extension/charliermarsh/ruff) | 🚀 Ported | Use [Ruff (loong64)](https://open-vsx.org/extension/loong-vsx/ruff) instead. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/loong-vsx/ruff&query=$.version&label=&color=teal) |
| [rust-analyzer](https://open-vsx.org/extension/rust-lang/rust-analyzer) | 🔄 Alternative | Use [rust-analyzer-no-server](https://open-vsx.org/extension/loong-vsx/rust-analyzer) instead. See [loongcodium/rust-analyzer-no-server](https://github.com/loongcodium/rust-analyzer-no-server). | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/loong-vsx/rust-analyzer&query=$.version&label=&color=blue) |
| [Tinymist Typst](https://open-vsx.org/extension/myriad-dreamin/tinymist) | 😭 Not Working | Unsupported architecture. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/myriad-dreamin/tinymist&query=$.version&label=&color=red) |
| [TypeScript + Webpack Problem Matchers](https://open-vsx.org/extension/amodio/tsl-problem-matcher) | ✅ Working | Works out of the box. | ![version](https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/amodio/tsl-problem-matcher&query=$.version&label=&color=brightgreen) |

## Contributing

- Test extensions and report compatibility
- Help port extensions to LoongArch
- Improve documentation

## Resources

- [GitHub Discussions](https://github.com/orgs/loongcodium/discussions)
