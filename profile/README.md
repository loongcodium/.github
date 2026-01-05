# LoongCodium

Making VSCodium extensions work on LoongArch! We test extensions for compatibility and port them when necessary.

> Note: All extensions listed are from [Open VSX Registry](https://open-vsx.org/), which is the default marketplace for VSCodium.

## Extension Status

| Extension | Status | Notes |
|-----------|---------|-------|
| [clangd](https://open-vsx.org/extension/llvm-vs-code-extensions/vscode-clangd) | ✅ Working | Requires `clangd` to be installed on the system beforehand |
| [CodeLLDB](https://open-vsx.org/extension/vadimcn/vscode-lldb) | 🔄 Alternative | Use [LLDB DAP](https://open-vsx.org/extension/llvm-vs-code-extensions/lldb-dap) or [Native Debug](https://open-vsx.org/extension/webfreak/debug) instead |
| [Even Better TOML](https://open-vsx.org/extension/tamasfe/even-better-toml) | ✅ Working | Once installed, configure `Bundled` to `false` |
| [Go](https://open-vsx.org/extension/golang/Go) | ✅ Working | Works out of the box, automatically install related binaries |
| [Python](https://open-vsx.org/extension/ms-python/python) | ✅ Working | Works out of the box |
| Pylance | 🔄 Alternative | Use [BasedPyright](https://open-vsx.org/extension/detachhead/basedpyright) instead, see https://github.com/VSCodium/vscodium/discussions/1641 |
| Remote - SSH | 🔄 Alternative | Use [Open Remote - SSH](https://open-vsx.org/extension/jeanp413/open-remote-ssh) instead |
| [Tinymist Typst](https://open-vsx.org/extension/myriad-dreamin/tinymist) | 😭 Not Working | Unsupported architecture |
| [rust-analyzer](https://open-vsx.org/extension/rust-lang/rust-analyzer) | 🔄 Alternative | Use [rust-analyzer-no-server](https://open-vsx.org/extension/loong-vsx/rust-analyzer) instead, see [loongcodium/rust-analyzer-no-server](https://github.com/loongcodium/rust-analyzer-no-server) |

## Contributing

- Test extensions and report compatibility
- Help port extensions to LoongArch
- Improve documentation

## Resources

- [GitHub Discussions](https://github.com/orgs/loongcodium/discussions)
