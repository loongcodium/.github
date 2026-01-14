# Contribution Guide

## 1. Overview
Welcome to contributing to the LoongCodium extension compatibility list!

Before submitting your contribution, please ensure that you:
-   Adopt a responsible attitude and thoroughly test extension compatibility.
-   Report extension status accurately.
-   Provide detailed information for any ported extensions.

## 2. Submitting Contributions

### 2.1 Automatically Generated Extension List

> [!IMPORTANT]
> The extension list in the README is **automatically generated**. Please do **not** modify the `profile/README.md` file directly.

We employ an automated process to manage the extension list, primarily based on the design philosophy of separating data from presentation. Storing extension information in a structured CSV file makes data maintenance simpler and more suitable for version control, while also providing extensibility for adding new fields in the future (such as test dates, tester information, etc.). In a collaborative setting, modifying CSV file significantly reduces maintenance effort compared to directly editing Markdown tables. The advantages of automation include automatic validation of data format and completeness, real-time fetching of the latest version information for extensions from Open VSX, unified generation of visually appealing version badges and standardized table formatting, as well as automatic alphabetical sorting by extension name.

### 2.2 How It Works
The project updates the extension list through three key files:

| File | Path | Purpose |
|------|------|------|
| **CSV Data File** | `scripts/extensions.csv` | Stores all extension compatibility data. |
| **Python Script** | `scripts/update_readme.py` | Reads the CSV, fetches extension information, and generates the table. |
| **GitHub Actions Configuration** | `.github/workflows/update-readme.yml` | Automated workflow that monitors CSV changes and automatically updates the README. |

**Workflow**:
1. Update `extensions.csv` → 2. GitHub Actions triggers → 3. Runs Python script → 4. Automatically updates `README.md`

### 2.3 Implementation Steps

#### 2.3.1 Fork the Repository and Create a Branch
1.  **Fork the Repository**: Click the "Fork" button in the upper right corner of the page to create a copy of this repository.
2.  **Clone the Repository**: Clone your forked repository to your local machine.
3.  **Create a Feature Branch**: Create a new feature branch based on the `main` branch for your changes.

#### 2.3.2 Update the CSV File
Edit the `scripts/extensions.csv` file. Each row represents one extension. The column descriptions are as follows:

**`original_id`**: Fill in the extension's identifier from the [Open VSX Registry](https://open-vsx.org/) or the [VSCode Marketplace](https://marketplace.visualstudio.com/VSCode), in the format `publisher.extension`, e.g., `ms-python.python`. Typically, an extension's ID is consistent between the Open VSX Registry and the VSCode Marketplace. In the rare case of inconsistency, the ID from Open VSX should be used. For extensions that exist only in the VSCode Marketplace (e.g., Pylance), use its VSCode Marketplace ID directly.

**`status`**: Use a numeric code from 0 to 3 to indicate the extension's compatibility status.
-   Status `0` (✅ Working): The extension natively supports LoongArch.
-   Status `1` (🚀 Ported): The official version does not support it, but there is a community-ported version available.
-   Status `2` (🔄 Alternative): The official version does not support it, but there is a functionally reliable alternative extension available.
-   Status `3` (😭 Not Working): The extension currently cannot run on LoongArch and no alternative is available.

**Example 1**: For the Python extension, its ID is `ms-python.python`, and its status is natively available (Working). Therefore, fill it in as follows.
```csv
original_id, status, actual_ids, notes
ms-python.python, 0, ,
```

**`actual_ids`**: Fill in the extension ID(s) that can actually be installed and used on LoongArch. For cases where `status` is 1 (Ported) or 2 (Alternative), this column should list the ID(s) of the ported or alternative extension(s). If multiple extensions are available, separate them with a vertical bar `|`. For `status` 0 (Working) or 3 (Not Working), this column is usually left empty.

**Example 2**: For the CodeLLDB extension, its ID is `vadimcn.vscode-lldb`. This extension is not available, but there are two alternative extensions: LLDB DAP (ID: `llvm-vs-code-extensions.lldb-dap`) and Native Debug (ID: `webfreak.debug`). Therefore, fill it in as follows.
```csv
original_id, status, actual_ids, notes
vadimcn.vscode-lldb, 2, llvm-vs-code-extensions.lldb-dap|webfreak.debug,
```

**`notes`**: Fill in remarks or additional information. You can use Markdown formatting. The script automatically adds a prefix for certain statuses: 

- "Works out of the box." for status 0, 
- "Use XXX instead." for status 1 and 2, and
- "Unsupported architecture." for status 3. 

Therefore, you do not need to repeat these default descriptions in this column; only provide extra information.

**Example 3**: The unavailable Pylance extension is only provided in the VSCode Marketplace, with ID `ms-python.vscode-pylance`. The alternative extension is BasedPyright (ID: `detachhead.basedpyright`), and an additional note is attached. Therefore, fill it in as follows.
```csv
original_id, status, actual_ids, notes
ms-python.vscode-pylance, 2, detachhead.basedpyright, "See this [discussion](https://github.com/VSCodium/vscodium/discussions/1641)."
```

#### 2.3.3 Local Testing (Optional)
If you wish to verify the changes locally:
1.  **Install Dependencies**:
    ```bash
    pip install tqdm requests
    ```
2.  **Run the Update Script**:
    ```bash
    python scripts/update_readme.py
    ```
3.  Check if the updated `profile/README.md` meets your expectations.

#### 2.3.4 Commit Changes
```bash
# Stage the modified files
git add scripts/extensions.csv

# Commit the changes (please use a meaningful commit message)
git commit -m "docs: Update/Add compatibility info/status for [Extension Name]

- Status: [Working/Ported/Alternative/Not Working]
- Actual ID(s): [Actual usable extension ID(s)]
- Notes: [Brief description]"

# Push to your fork
git push origin docs/extension-name-compatibility-update
```

> [!NOTE]
> After performing the commit, GitHub Actions will be triggered in your forked repository. Before submitting the PR to upstream, be sure to check the Actions tab and working branch in your fork to verify that the workflow completed successfully and produced the expected updates.

#### 2.3.5 Create a Pull Request
On GitHub, navigate to your forked repository, click the "Compare & pull request" button, and create a Pull Request from your feature branch to the `main` branch of the upstream `loongcodium/.github` repository. Please clearly describe the changes and any testing performed. After the PR is merged, GitHub Actions will automatically run the update script and commit the changes to `profile/README.md`.

#### 2.3.6 Frequently Asked Questions (FAQ)
**Q: What if there's a CSV format error?**  
A: Ensure the file uses UTF-8 encoding, uses commas to separate columns, **wraps the entire field in double quotes if the text contains commas**, and that the status codes are only 0, 1, 2, or 3.

**Q: What if extension information retrieval fails?**  
A: Verify the extension ID format is correct (`publisher.extension`), check if the extension exists by visiting the [Open VSX Registry](https://open-vsx.org/), and ensure your network connection is normal.

**Q: What if the GitHub Action fails?**  
A: Check the detailed logs under the "Actions" tab of the repository to locate the failing step and error message.

**Q: What if the table doesn't update?**  
A: Ensure `profile/README.md` contains the correct `<!-- table_start -->` and `<!-- table_end -->` markers, the CSV file path is correct, and that the committed changes have triggered the workflow.

**Q: How to report issues or discuss?**  
A: You can report specific issues by submitting an Issue, or join the [GitHub Discussions](https://github.com/orgs/loongcodium/discussions) to participate. It is recommended to check existing Issues and discussions first to avoid duplication.

