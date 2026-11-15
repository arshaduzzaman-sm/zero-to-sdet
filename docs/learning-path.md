---
title: "SDET Learning Path: From Manual Tester to Senior SDET"
description: "The full SDET learning path on one map: what to learn first, what comes next, and four step-by-step paths for your role."
tags:
  - Getting started
  - Career
updated: "2026-11-15"
nav_title: "Learning Path"
order: 60
nav_section: "start-here"
summary: "The whole journey on one map, plus step-by-step paths for your role."
---

# SDET Learning Path

This page shows the whole journey on one map, then gives you a step-by-step path for where you are today.

!!! info "In plain words"
    Learning to be an SDET is like learning to drive. First you learn the car and the rules.
    Then you drive on quiet roads. Later you handle motorways, bad weather and long trips.
    Each stage builds on the one before, but you can always go back and practise.

## The whole journey

Each box is a group of topics. Follow the arrows from top to bottom.

```mermaid
---
config:
  flowchart:
    wrappingWidth: 360
    nodeSpacing: 30
    rankSpacing: 34
---
flowchart TD
    A("<b>1. Start Here</b><br/>Set up your computer · Python for testers")
    B("<b>2. Think Like a Tester</b><br/>Test design · test cases · bug reports · plans")
    C("<b>3. Core Automation</b><br/>pytest · API · database · BDD · Playwright<br/><i>You are now a junior SDET</i>")
    D("<b>4. Infrastructure</b><br/>CI/CD · Docker · Linux · debugging<br/><i>You are now a mid-level SDET</i>")
    E("<b>5. Advanced Testing</b><br/>Performance · security · contracts · microservices<br/><i>You are now a senior SDET</i>")
    F("<b>6. The Professional SDET</b><br/>Releases · metrics · leading quality<br/><i>Ready to lead a team</i>")
    A --> B --> C --> D --> E --> F
```

The line in italics shows roughly which level you reach after each stage.
Everyone moves at their own speed, and that is fine.

!!! tip "Check where you are"
    The [Skills Matrix](start-here/skills-matrix.md) lists every skill by level. Tick what you know, then pick the path below that fits.

---

## Manual tester to automation

**For you if:** you test by hand today and have never written code.
**Goal:** write and run your first automated tests with confidence.

1. [How to use this site](start-here/how-to-use-this-site/index.md)
2. [Environment setup](start-here/environment-setup/index.md): Python, VS Code and a virtual environment
3. [Python for testers](start-here/python-for-testers/index.md): just enough Python to write tests
4. [Practice App tour](start-here/practice-app-tour/index.md): the shop you will test in every lesson
5. [The SDET role](think-like-a-tester/the-sdet-role/index.md)
6. [Test design techniques](think-like-a-tester/test-design-techniques/index.md)
7. [pytest framework](core-automation/pytest-framework/index.md): your first automated test
8. [API testing](core-automation/api-testing/index.md)
9. [Database testing](core-automation/database-testing/index.md)
10. [Git in a team](professional-sdet/git-in-a-team/index.md)
11. [Debugging toolkit](infrastructure/debugging-toolkit/index.md)

---

## Junior to mid-level

**For you if:** you can write tests, but someone else designs the framework.
**Goal:** build and run a whole test suite on your own.

1. [API + database](core-automation/api-and-database/index.md)
2. [Data-driven testing](core-automation/data-driven-testing/index.md)
3. [BDD testing](core-automation/bdd-testing/index.md): with behave and with pytest-bdd
4. [UI automation](core-automation/ui-automation/index.md) with Playwright
5. [Reporting and logging](core-automation/reporting-and-logging/index.md)
6. [CI/CD](infrastructure/ci-cd/index.md): run your tests on every change
7. [Docker for testers](infrastructure/docker-for-testers/index.md)
8. [Multi-database testing](core-automation/multi-database-testing/index.md)
9. [Mocking and stubbing](advanced-testing/mocking-and-stubbing/index.md)
10. [Flaky tests and speed](advanced-testing/flaky-tests-and-speed/index.md)
11. [Test strategy and planning](think-like-a-tester/test-strategy-and-planning/index.md)
12. [Clean test code](professional-sdet/clean-test-code/index.md)

---

## Mid-level to senior

**For you if:** you build test suites on your own and want to design how a team tests.
**Goal:** own quality for a product, and be trusted to say a release is safe.

1. [Performance testing](advanced-testing/performance-testing/index.md): Locust, k6 and JMeter
2. [Security testing basics](advanced-testing/security-testing/index.md)
3. [Contract testing](advanced-testing/contract-testing/index.md)
4. [Testing microservices](advanced-testing/testing-microservices/index.md)
5. [Data and ETL testing](advanced-testing/data-and-etl-testing/index.md)
6. [Cloud and Kubernetes basics](infrastructure/cloud-and-kubernetes/index.md)
7. [Observability](infrastructure/observability/index.md)
8. [Quality metrics](professional-sdet/quality-metrics/index.md)
9. [Release sign-off](professional-sdet/release-sign-off/index.md)
10. [Leading quality](professional-sdet/leading-quality/index.md)
11. [Capstone project](professional-sdet/capstone-project/index.md): build a full framework

---

## Interview prep in 4 weeks

**For you if:** you have an SDET interview coming up.
**Goal:** walk in knowing the common questions, and with a project to show.

| Week | Focus | Lessons |
| --- | --- | --- |
| 1 | Testing basics and Python | [Test design techniques](think-like-a-tester/test-design-techniques/index.md), [Bug reports](think-like-a-tester/bug-reports/index.md), [Python for testers](start-here/python-for-testers/index.md) |
| 2 | API and database | [API testing](core-automation/api-testing/index.md), [Database testing](core-automation/database-testing/index.md), [pytest framework](core-automation/pytest-framework/index.md) |
| 3 | UI, CI and frameworks | [UI automation](core-automation/ui-automation/index.md), [CI/CD](infrastructure/ci-cd/index.md), [Clean test code](professional-sdet/clean-test-code/index.md) |
| 4 | Interview practice | [Interview preparation](professional-sdet/interview-preparation/index.md), [Portfolio and resume](professional-sdet/portfolio-and-resume/index.md), [Career roadmap](professional-sdet/career-roadmap/index.md) |

!!! warning "Be honest with yourself"
    Four weeks is enough to prepare, but not to learn everything from zero.
    If you are new to coding, start with the [manual tester path](#manual-tester-to-automation) first.
