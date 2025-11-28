"""
MAGIC PROJECT STATUS DIAGNOSTIC TOOL
Tests everything about your current MAGIC state
"""

import os
import sys
import json
import importlib
from pathlib import Path
from typing import Dict, List, Any

class MagicDiagnostic:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = {
            "overall_status": "UNKNOWN",
            "stage_progress": {},
            "critical_issues": [],
            "recommendations": [],
            "metrics": {}
        }

    def run_full_diagnostic(self) -> Dict[str, Any]:
        """Run complete diagnostic of MAGIC project"""
        print("🔍 RUNNING MAGIC PROJECT DIAGNOSTIC...")

        tests = [
            self.test_project_structure,
            self.test_script_generation,
            self.test_import_stability,
            self.test_shim_implementation,
            self.test_smoke_test_status,
            self.test_stage1_completion,
            self.test_infrastructure_readiness
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                self.results["critical_issues"].append(f"Test failed: {test.__name__}: {e}")

        self._calculate_overall_status()
        return self.results

    def test_project_structure(self):
        """Test if basic project structure exists"""
        print("📁 Checking project structure...")

        essential_dirs = [
            "scripts",
            "tests",
            "tools",
            "outputs"
        ]

        essential_files = [
            "scripts/__init__.py",
            "tests/smoke",
            "tools/run_generate_magic_scripts.ps1"
        ]

        found_dirs = []
        missing_dirs = []

        for dir_path in essential_dirs:
            if (self.project_root / dir_path).exists():
                found_dirs.append(dir_path)
            else:
                missing_dirs.append(dir_path)

        self.results["metrics"]["essential_dirs_found"] = len(found_dirs)
        self.results["metrics"]["essential_dirs_missing"] = len(missing_dirs)
        self.results["stage_progress"]["project_structure"] = f"{len(found_dirs)}/{len(essential_dirs)}"

        if missing_dirs:
            self.results["critical_issues"].append(f"Missing directories: {missing_dirs}")

    def test_script_generation(self):
        """Test if all 1450 scripts were generated"""
        print("📄 Checking script generation...")

        scripts_dir = self.project_root / "scripts"
        if not scripts_dir.exists():
            self.results["critical_issues"].append("scripts/ directory not found")
            return

        # Count _READY.py files
        ready_files = list(scripts_dir.rglob("*_READY.py"))
        total_files = len(ready_files)

        # Check if files are empty stubs
        empty_files = 0
        non_empty_files = 0

        for file_path in ready_files[:50]:  # Sample first 50 files
            try:
                content = file_path.read_text(encoding='utf-8')
                # Count non-comment, non-empty lines
                code_lines = [line for line in content.split('\n')
                             if line.strip() and not line.strip().startswith('#')]
                if len(code_lines) < 5:  # Less than 5 real lines = empty stub
                    empty_files += 1
                else:
                    non_empty_files += 1
            except:
                empty_files += 1

        self.results["metrics"]["total_scripts"] = total_files
        self.results["metrics"]["empty_scripts"] = empty_files
        self.results["metrics"]["non_empty_scripts"] = non_empty_files
        self.results["stage_progress"]["script_generation"] = f"{total_files}/1450"

        if total_files < 100:
            self.results["critical_issues"].append(f"Only {total_files} scripts found, expected ~1450")
        if empty_files > non_empty_files:
            self.results["critical_issues"].append("Most scripts are empty stubs")

    def test_import_stability(self):
        """Test if imports work without errors"""
        print("🔗 Testing import stability...")

        test_modules = [
            "scripts._html5lib",
            "scripts._socket",
            "scripts._run",
            "scripts._github_workflows_placeholder_READY"
        ]

        successful_imports = 0
        failed_imports = []

        for module_name in test_modules:
            try:
                importlib.import_module(module_name)
                successful_imports += 1
                print(f"  ✅ {module_name}")
            except Exception as e:
                failed_imports.append(f"{module_name}: {e}")
                print(f"  ❌ {module_name}: {e}")

        self.results["metrics"]["successful_imports"] = successful_imports
        self.results["metrics"]["failed_imports"] = len(failed_imports)
        self.results["stage_progress"]["import_stability"] = f"{successful_imports}/{len(test_modules)}"

        if failed_imports:
            self.results["critical_issues"].extend([f"Import failed: {f}" for f in failed_imports])

    def test_shim_implementation(self):
        """Test if key shims are implemented"""
        print("🛡️ Checking shim implementation...")

        shim_files = [
            "scripts/_html5lib.py",
            "scripts/_socket.py",
            "scripts/_github_workflows_placeholder_READY.py"
        ]

        implemented_shims = 0
        for shim_path in shim_files:
            full_path = self.project_root / shim_path
            if full_path.exists():
                content = full_path.read_text(encoding='utf-8')
                # Check if it's more than just a stub
                if len(content.strip()) > 200:  # More than 200 chars = probably implemented
                    implemented_shims += 1
                    print(f"  ✅ {shim_path} - IMPLEMENTED")
                else:
                    print(f"  ⚠️ {shim_path} - STUB ONLY")
            else:
                print(f"  ❌ {shim_path} - MISSING")

        self.results["metrics"]["implemented_shims"] = implemented_shims
        self.results["stage_progress"]["shim_implementation"] = f"{implemented_shims}/{len(shim_files)}"

    def test_smoke_test_status(self):
        """Test if smoke tests pass"""
        print("🚬 Checking smoke test status...")

        smoke_test_dir = self.project_root / "tests" / "smoke"
        if not smoke_test_dir.exists():
            self.results["critical_issues"].append("Smoke tests directory not found")
            return

        # Count smoke test files
        smoke_test_files = list(smoke_test_dir.glob("test_*.py"))
        self.results["metrics"]["smoke_test_files"] = len(smoke_test_files)

        # Try to run a simple import test
        try:
            # This is a simplified check - in reality you'd run pytest
            sys.path.insert(0, str(self.project_root))
            test_imports = []
            for test_file in smoke_test_files[:3]:  # Sample first 3
                spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    test_imports.append(test_file.name)

            self.results["metrics"]["smoke_tests_importable"] = len(test_imports)
            print(f"  ✅ {len(test_imports)} smoke tests can import")

        except Exception as e:
            self.results["critical_issues"].append(f"Smoke test check failed: {e}")
            print(f"  ❌ Smoke test check failed: {e}")

    def test_stage1_completion(self):
        """Estimate Stage 1 completion percentage"""
        print("📊 Estimating Stage 1 completion...")

        completion_indicators = {
            "scripts_generated": 0.3,
            "imports_working": 0.3,
            "shims_implemented": 0.2,
            "smoke_tests_green": 0.2
        }

        stage1_score = 0

        # Script generation (30%)
        total_scripts = self.results["metrics"].get("total_scripts", 0)
        if total_scripts >= 1000:
            stage1_score += completion_indicators["scripts_generated"]
        elif total_scripts >= 500:
            stage1_score += completion_indicators["scripts_generated"] * 0.7
        elif total_scripts >= 100:
            stage1_score += completion_indicators["scripts_generated"] * 0.3

        # Imports working (30%)
        successful_imports = self.results["metrics"].get("successful_imports", 0)
        total_import_tests = 4  # From our test above
        if successful_imports == total_import_tests:
            stage1_score += completion_indicators["imports_working"]
        elif successful_imports >= total_import_tests * 0.7:
            stage1_score += completion_indicators["imports_working"] * 0.7
        elif successful_imports >= total_import_tests * 0.5:
            stage1_score += completion_indicators["imports_working"] * 0.5

        # Shims implemented (20%)
        implemented_shims = self.results["metrics"].get("implemented_shims", 0)
        total_shims = 3  # From our test above
        if implemented_shims == total_shims:
            stage1_score += completion_indicators["shims_implemented"]
        elif implemented_shims >= total_shims * 0.7:
            stage1_score += completion_indicators["shims_implemented"] * 0.7

        # Smoke tests (20%)
        smoke_tests_importable = self.results["metrics"].get("smoke_tests_importable", 0)
        if smoke_tests_importable >= 3:
            stage1_score += completion_indicators["smoke_tests_green"]
        elif smoke_tests_importable >= 1:
            stage1_score += completion_indicators["smoke_tests_green"] * 0.5

        stage1_percentage = round(stage1_score * 100, 1)
        self.results["stage_progress"]["stage1_completion"] = f"{stage1_percentage}%"

        if stage1_percentage >= 80:
            self.results["recommendations"].append("Stage 1 nearly complete - proceed to Stage 2")
        elif stage1_percentage >= 50:
            self.results["recommendations"].append("Stage 1 halfway - focus on critical imports")
        else:
            self.results["critical_issues"].append("Stage 1 less than 50% complete")

    def test_infrastructure_readiness(self):
        """Check if infrastructure tools exist"""
        print("🛠️ Checking infrastructure readiness...")

        infrastructure_files = [
            "tools/run_generate_magic_scripts.ps1",
            "Dockerfile",
            "requirements.txt",
            ".github/workflows"
        ]

        found_infra = 0
        for infra_path in infrastructure_files:
            full_path = self.project_root / infra_path
            if full_path.exists():
                found_infra += 1
                print(f"  ✅ {infra_path}")
            else:
                print(f"  ❌ {infra_path}")

        self.results["metrics"]["infrastructure_files"] = found_infra
        self.results["stage_progress"]["infrastructure"] = f"{found_infra}/{len(infrastructure_files)}"

    def _calculate_overall_status(self):
        """Calculate overall project status"""
        critical_issues = len(self.results["critical_issues"])
        stage1_completion = self.results["stage_progress"].get("stage1_completion", "0%")
        stage1_percentage = float(stage1_completion.rstrip('%'))

        if critical_issues == 0 and stage1_percentage >= 80:
            self.results["overall_status"] = "HEALTHY"
        elif critical_issues <= 2 and stage1_percentage >= 50:
            self.results["overall_status"] = "STABLE"
        elif critical_issues <= 5:
            self.results["overall_status"] = "UNSTABLE"
        else:
            self.results["overall_status"] = "CRITICAL"

    def generate_report(self):
        """Generate a comprehensive report"""
        report = f"""
🎯 MAGIC PROJECT STATUS REPORT
================================

OVERALL STATUS: {self.results["overall_status"]}

📊 PROGRESS METRICS:
-------------------
Stage 1 Completion: {self.results["stage_progress"].get('stage1_completion', 'Unknown')}
Scripts Generated: {self.results["metrics"].get('total_scripts', 0)}/1450
Successful Imports: {self.results["metrics"].get('successful_imports', 0)}/4
Implemented Shims: {self.results["metrics"].get('implemented_shims', 0)}/3

🚨 CRITICAL ISSUES ({len(self.results['critical_issues'])}):
-----------------------
""" + "\n".join([f"• {issue}" for issue in self.results["critical_issues"]]) + """

💡 RECOMMENDATIONS ({len(self.results['recommendations'])}):
------------------------
""" + "\n".join([f"• {rec}" for rec in self.results["recommendations"]]) + """

📈 DETAILED PROGRESS:
--------------------
""" + "\n".join([f"{key}: {value}" for key, value in self.results["stage_progress"].items()])

        return report

def main():
    """Run the diagnostic and print report"""
    diagnostic = MagicDiagnostic()
    results = diagnostic.run_full_diagnostic()

    print("\n" + "="*60)
    print(diagnostic.generate_report())
    print("="*60)

    # Save detailed results
    output_file = "magic_status_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Detailed report saved to: {output_file}")

if __name__ == "__main__":
    main()
