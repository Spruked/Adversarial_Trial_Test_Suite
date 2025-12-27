# Adversarial Trial Test Suite

## Overview

This test suite contains adversarial tests designed to evaluate the robustness of AI models (judges) against various reasoning challenges, including temporal paradoxes, logical contradictions, security vulnerabilities, and cognitive boundary testing.

## Purpose

The suite is intended for:
- AI safety researchers
- Model developers
- Security auditors
- Academic institutions studying AI robustness

## Structure

The test suite is organized by judge (AI model being tested):

- `chatgpt5_1/` - Tests for ChatGPT-5.1
- `deepseek/` - Tests for DeepSeek
- `gemini/` - Tests for Gemini
- `grok4/` - Tests for Grok-4
- `kimi/` - Tests for Kimi

Each judge folder contains:
- `tests/` - Test specifications with placeholders for execution
- `results/` - Placeholder files for results and logs

## Test Categories

- **Temporal Reasoning**: Tests for handling time-based paradoxes and causal inconsistencies
- **Symbolic Cognition**: Pattern recognition and abstraction under noise/contradictions
- **Dual-Mind Cooperation**: Internal consistency between reasoning components
- **Security/Boundary Reasoning**: Resistance to adversarial inputs and boundary violations
- **Ethical Reasoning**: Handling of harmful logic chains and ethical dilemmas

## Usage

1. Select a judge folder
2. Run the tests in the `tests/` directory
3. Record results in the `results/` directory
4. Update logs as needed

## Adding New Tests

To add new tests:
1. Create a new `.md` file in the appropriate judge's `tests/` folder
2. Follow the existing template format
3. Include test specification, pass/fail criteria, and placeholders for results

## Contact

For questions or contributions, please refer to the project documentation.