---
name: paper-repository-bootstrapper
description: "Scaffold an explicitly approved independent paper repository with a manifest, exact shared pin, local authority and reproducibility hooks."
---

# Paper Repository Bootstrapper

1. Read the approved idea/promotion decision and intended repository authority. Record title, scope, repository URL, shared commit and publication/license choices. Do not promote an idea merely because it appears in a backlog.

2. Run `python3 .agent/shared/tools/bootstrap_project.py --destination NEW_PATH --id PROJECT_ID --repository HTTPS_URL --revision SHA --title TITLE`. The destination must not exist. The scaffold creates infrastructure only and deliberately leaves manuscript files uncreated.

3. Initialize the recorded shared submodule with Git and install tracked hooks. Add manuscript source only under a later explicit manuscript-authoring request; the current manuscript freeze takes precedence over a skeleton template.

4. Fill the manifest from actual local authority and selected licenses. The scaffold always installs the companion-site Pages workflow (`.github/workflows/pages.yml`, pinned to the same shared revision as the submodule); keep it, and enable repository Pages with build type "GitHub Actions" so a push to the default branch deploys the site without further action. Do not defer or remove this workflow. Label untested launch links and environments accurately. Keep paper-specific skills local with distinct names.

5. Test the scaffold in a clean temporary clone, including pin initialization, hooks and manifest checks once the real manuscript exists. Register the paper in the program only after the independent repository is established; record unfulfilled prerequisites.
