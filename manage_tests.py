#!/usr/bin/env python3
"""
Adversarial Trial Test Suite Manager

This script helps manage and run the adversarial test suite.
It can list tests, check completion status, and generate reports.
"""

import os
import glob
from pathlib import Path
import argparse

class TestSuiteManager:
    def __init__(self, suite_path):
        self.suite_path = Path(suite_path)
        self.judges = ['chatgpt5_1', 'deepseek', 'gemini', 'grok4', 'kimi']

    def list_tests(self, judge=None):
        """List all tests in the suite"""
        print("Adversarial Trial Test Suite - Test List")
        print("=" * 50)

        judges_to_check = [judge] if judge else self.judges

        for judge_name in judges_to_check:
            judge_path = self.suite_path / judge_name
            if not judge_path.exists():
                continue

            tests_path = judge_path / 'tests'
            if not tests_path.exists():
                continue

            print(f"\n{judge_name.upper()}:")
            test_files = sorted(tests_path.glob('*.md'))
            for test_file in test_files:
                print(f"  - {test_file.name}")

    def check_completion(self, judge=None):
        """Check which tests have results filled in"""
        print("Test Completion Status")
        print("=" * 50)

        judges_to_check = [judge] if judge else self.judges

        total_tests = 0
        completed_tests = 0

        for judge_name in judges_to_check:
            judge_path = self.suite_path / judge_name
            if not judge_path.exists():
                continue

            tests_path = judge_path / 'tests'
            results_path = judge_path / 'results'

            if not tests_path.exists():
                continue

            print(f"\n{judge_name.upper()}:")

            test_files = sorted(tests_path.glob('*.md'))
            for test_file in test_files:
                total_tests += 1
                test_name = test_file.stem

                # Check if result placeholder is filled
                result_file = results_path / f"JUDGE_{judge_name.upper()}_LOG.md"
                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '[Placeholder' not in content:
                            completed_tests += 1
                            status = "✅ COMPLETED"
                        else:
                            status = "⏳ PENDING"
                else:
                    status = "❌ NO RESULTS FILE"

                print(f"  - {test_file.name}: {status}")

        print(f"\nOverall Progress: {completed_tests}/{total_tests} tests completed")

    def generate_report(self, output_file=None):
        """Generate a summary report of the test suite"""
        report = []
        report.append("# Adversarial Trial Test Suite Report")
        report.append(f"Generated: {os.popen('date').read().strip()}")
        report.append("")

        judges_to_check = self.judges

        total_tests = 0
        completed_tests = 0

        for judge_name in judges_to_check:
            judge_path = self.suite_path / judge_name
            if not judge_path.exists():
                continue

            tests_path = judge_path / 'tests'
            results_path = judge_path / 'results'

            if not tests_path.exists():
                continue

            report.append(f"## {judge_name.upper()}")

            test_files = sorted(tests_path.glob('*.md'))
            judge_completed = 0
            judge_total = len(test_files)

            for test_file in test_files:
                total_tests += 1
                test_name = test_file.stem

                # Check completion
                result_file = results_path / f"JUDGE_{judge_name.upper()}_LOG.md"
                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '[Placeholder' not in content:
                            completed_tests += 1
                            judge_completed += 1
                            status = "✅ COMPLETED"
                        else:
                            status = "⏳ PENDING"
                else:
                    status = "❌ NO RESULTS FILE"

                report.append(f"- {test_file.name}: {status}")

            report.append(f"**{judge_name.upper()} Progress:** {judge_completed}/{judge_total}")
            report.append("")

        report.append("## Overall Statistics")
        report.append(f"- Total Tests: {total_tests}")
        report.append(f"- Completed Tests: {completed_tests}")
        report.append(f"- Completion Rate: {completed_tests/total_tests*100:.1f}%" if total_tests > 0 else "0%")

        report_text = "\n".join(report)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"Report saved to {output_file}")
        else:
            print(report_text)

def main():
    parser = argparse.ArgumentParser(description='Manage Adversarial Trial Test Suite')
    parser.add_argument('--suite-path', default='.', help='Path to test suite directory')
    parser.add_argument('--judge', help='Specific judge to operate on')
    parser.add_argument('action', choices=['list', 'status', 'report'], help='Action to perform')
    parser.add_argument('--output', help='Output file for report')

    args = parser.parse_args()

    manager = TestSuiteManager(args.suite_path)

    if args.action == 'list':
        manager.list_tests(args.judge)
    elif args.action == 'status':
        manager.check_completion(args.judge)
    elif args.action == 'report':
        manager.generate_report(args.output)

if __name__ == '__main__':
    main()
