---
title: "Software Testing Glossary: Every SDET Term in Plain English"
description: "Plain-English meanings of every testing and automation term used on Zero to SDET, each linked to the lesson that teaches it."
tags:
  - Quick reference
updated: "2026-11-16"
nav_title: "Glossary"
order: 40
nav_section: "toolbox"
summary: "Every testing word on this site, in plain English."
---

# Glossary

Every testing word on this site, in plain English. Each one links to the lesson
that teaches it.

!!! tip "Two quick ways to use it"
    - **Hover** over a short form like API or BDD on any page to see what it means.
    - **Search** with the box at the top: type a word and it shows the meaning here.

<!-- BEGIN glossary (generated from data/glossary.yml, do not edit by hand) -->

<nav class="zts-az" aria-label="Jump to a letter" markdown>[A](#a) [B](#b) [C](#c) [D](#d) [E](#e) [F](#f) [G](#g) [H](#h) [I](#i) [J](#j) [L](#l) [M](#m) [N](#n) [O](#o) [P](#p) [Q](#q) [R](#r) [S](#s) [T](#t) [U](#u) [V](#v) [W](#w)</nav>

## A

[](){ #acceptance-criteria }**Acceptance criteria**
:   The list of things a feature must do before the team calls it finished. Testers turn each one into tests.

    Learn more: [Test cases](think-like-a-tester/test-cases/index.md)

[](){ #accessibility }**Accessibility**
:   How easy the app is to use for everyone, including people who use a screen reader, a keyboard only, or large text.

    Learn more: [Accessibility testing](advanced-testing/accessibility-testing/index.md)

[](){ #ambiguity }**Ambiguity**
:   Words that two people can read in different ways, like "fast" or "recent". Testers ask for a number or a clear rule instead.

    Learn more: [Finding ambiguity and missing cases](think-like-a-tester/static-testing-and-reviews/finding-ambiguity-and-missing-cases.md)

[](){ #api }**API (Application Programming Interface)**
:   A way for one program to ask another program for data or to do something. Like a waiter who takes your order to the kitchen and brings back your food.

    Learn more: [API testing](core-automation/api-testing/index.md)

[](){ #api-test }**API test**
:   A test that sends a real request to the app's API and checks the status code and the data that come back.

    Learn more: [The test levels](think-like-a-tester/test-levels-and-the-pyramid/the-test-levels.md)

[](){ #assertion }**Assertion**
:   The line in a test that checks the result. If the check is false, the test fails.

    Learn more: [pytest framework](core-automation/pytest-framework/index.md)

[](){ #automation }**Automation**
:   Letting a program do a check that a person would otherwise do by hand, so it can run again and again in seconds.

    Learn more: [The SDET role](think-like-a-tester/the-sdet-role/index.md)

## B

[](){ #bdd }**BDD (Behavior-Driven Development)**
:   A way of writing tests as plain English examples, like "Given I am logged in, When I add a book, Then my cart has 1 item".

    Learn more: [BDD testing](core-automation/bdd-testing/index.md)

[](){ #boundary-value }**Boundary value**
:   A value right at the edge of what is allowed, like 0, 1, 99 and 100 for "1 to 99". Bugs love edges.

    Learn more: [Boundary values](think-like-a-tester/test-design-techniques/boundary-values.md)

[](){ #branch-coverage }**Branch coverage**
:   The share of ways through each if (yes and no) that the tests took. It finds paths that line coverage misses.

    Learn more: [Statement and branch coverage](think-like-a-tester/test-design-techniques/statement-and-branch-coverage.md)

[](){ #bug-lifecycle }**Bug lifecycle**
:   The states a bug moves through, like new, triaged, in progress, fixed, verified and closed.

    Learn more: [The bug lifecycle](think-like-a-tester/bug-reports/bug-lifecycle.md)

[](){ #bug-report }**Bug report**
:   A short note that tells a developer what went wrong, how to make it happen again, and what should have happened instead.

    Learn more: [Bug reports](think-like-a-tester/bug-reports/index.md)

## C

[](){ #checklist-based-testing }**Checklist-based testing**
:   Testing with a short list of things that must be true for every feature of one kind, like every web form.

    Learn more: [Checklist-based testing](think-like-a-tester/test-design-techniques/checklist-based-testing.md)

[](){ #cicd }**CI/CD (Continuous Integration and Continuous Delivery)**
:   A setup that builds the app and runs the tests every time someone changes the code, then helps ship it.

    Learn more: [CI/CD (teaching topic)](infrastructure/ci-cd/index.md)

[](){ #container }**Container**
:   A small, sealed box that holds an app and everything it needs, so it runs the same way on every computer.

    Learn more: [Docker for testers](infrastructure/docker-for-testers/index.md)

[](){ #contract-testing }**Contract testing**
:   Checking that two services still agree on the shape of the messages they send each other.

    Learn more: [Contract testing](advanced-testing/contract-testing/index.md)

## D

[](){ #database }**Database**
:   An organized store of data that an app saves to and reads from, like a set of very large tables.

    Learn more: [Database testing](core-automation/database-testing/index.md)

[](){ #decision-table }**Decision table**
:   A table that lists every mix of conditions, like "member" and "order over $50", with the result for each. Each row becomes a test.

    Learn more: [Decision tables](think-like-a-tester/test-design-techniques/decision-tables.md)

[](){ #defect-clustering }**Defect clustering**
:   Most bugs hide in a few parts of a system. When you find one bug, look for more nearby.

    Learn more: [The seven testing principles](think-like-a-tester/the-sdet-role/seven-testing-principles.md)

[](){ #docker }**Docker**
:   The most common tool for building and running containers.

    Learn more: [Docker for testers](infrastructure/docker-for-testers/index.md)

[](){ #dynamic-testing }**Dynamic testing**
:   Testing by running the software and checking what it does.

    Learn more: [What static testing is](think-like-a-tester/static-testing-and-reviews/what-is-static-testing.md)

## E

[](){ #e2e }**E2E (End-to-end)**
:   A test that goes through the whole app the way a real user would, from the web page down to the database and back.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #edge-case }**Edge case**
:   A test right at a limit, like a code used at exactly 10 minutes. Bugs often hide at limits.

    Learn more: [The 9-step playbook](think-like-a-tester/learning-a-new-testing-area/the-9-step-playbook.md)

[](){ #endpoint }**Endpoint**
:   One address of an API that you can send a request to, like /products or /orders/42.

    Learn more: [API testing](core-automation/api-testing/index.md)

[](){ #environment }**Environment**
:   One full copy of the app for a purpose, like your own computer, a shared test copy, or the live site.

    Learn more: [CI/CD (teaching topic)](infrastructure/ci-cd/index.md)

[](){ #equivalence-partitioning }**Equivalence partitioning**
:   Splitting inputs into groups that should behave the same, then testing one value from each group instead of all of them.

    Learn more: [Equivalence partitioning](think-like-a-tester/test-design-techniques/equivalence-partitioning.md)

[](){ #error-guessing }**Error guessing**
:   Trying the inputs and actions that often break software, like emoji, double clicks or 29 February.

    Learn more: [Error guessing](think-like-a-tester/test-design-techniques/error-guessing.md)

[](){ #expected-result }**Expected result**
:   Exactly what should happen when you run a test, and what must not. The most important line of a test case.

    Learn more: [Anatomy of a test case](think-like-a-tester/test-cases/anatomy-of-a-test-case.md)

[](){ #exploratory-testing }**Exploratory testing**
:   Testing by learning the app as you go, trying ideas and following anything that looks odd, instead of following a script.

    Learn more: [Exploratory testing](think-like-a-tester/test-design-techniques/exploratory-testing.md)

## F

[](){ #fixture }**Fixture**
:   In pytest, a small helper that gets something ready for a test, like a logged-in user, and cleans it up afterwards.

    Learn more: [pytest framework](core-automation/pytest-framework/index.md)

[](){ #flaky-test }**Flaky test**
:   A test that sometimes passes and sometimes fails without any change to the code.

    Learn more: [Flaky tests and speed](advanced-testing/flaky-tests-and-speed/index.md)

[](){ #framework }**Framework**
:   The shared structure of a test project, such as folders, settings and helpers, so every test is written the same way.

    Learn more: [pytest framework](core-automation/pytest-framework/index.md)

## G

[](){ #gherkin }**Gherkin**
:   The plain-English format BDD tests are written in, using the words Given, When and Then.

    Learn more: [BDD testing](core-automation/bdd-testing/index.md)

[](){ #git }**Git**
:   A tool that saves every change to your code, so you can go back in time and work with others safely.

    Learn more: [Git in a team](professional-sdet/git-in-a-team/index.md)

## H

[](){ #happy-path }**Happy path**
:   The normal way a user uses a feature, with good data and no mistakes. It is usually the first thing you test.

    Learn more: [The 9-step playbook](think-like-a-tester/learning-a-new-testing-area/the-9-step-playbook.md)

[](){ #http }**HTTP (Hypertext Transfer Protocol)**
:   The set of rules web browsers and APIs use to send requests and answers.

    Learn more: [Networking for testers](infrastructure/networking-for-testers/index.md)

## I

[](){ #ice-cream-cone }**Ice cream cone**
:   A test suite shaped like an upside-down pyramid, with many slow UI tests and very few unit tests. It is slow and often flaky.

    Learn more: [The test pyramid](think-like-a-tester/test-levels-and-the-pyramid/the-test-pyramid.md)

[](){ #inspection }**Inspection**
:   The most formal kind of review, with set roles, a checklist, prepared reviewers and a written list of findings.

    Learn more: [Review types](think-like-a-tester/static-testing-and-reviews/review-types.md)

[](){ #integration-test }**Integration test**
:   A test that checks two or more parts of the app work together, like the API and the database.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #istqb }**ISTQB (International Software Testing Qualifications Board)**
:   A group that writes testing exams and a shared list of testing words, used in many countries.

    Learn more: [The seven testing principles](think-like-a-tester/the-sdet-role/seven-testing-principles.md)

## J

[](){ #json }**JSON (JavaScript Object Notation)**
:   A simple text format for data, made of names and values in curly brackets. Most APIs send and receive JSON.

    Learn more: [API testing](core-automation/api-testing/index.md)

## L

[](){ #linter }**Linter**
:   A tool that reads code and points at bugs and risky patterns, like an unused import or an assert that can never fail.

    Learn more: [Static analysis tools](think-like-a-tester/static-testing-and-reviews/static-analysis-tools.md)

[](){ #load-testing }**Load testing**
:   Checking how the app behaves when many people use it at the same time.

    Learn more: [Performance testing](advanced-testing/performance-testing/index.md)

[](){ #locator }**Locator**
:   The instruction that tells a UI test which button, box or link on the page to use.

    Learn more: [UI automation](core-automation/ui-automation/index.md)

## M

[](){ #manual-testing }**Manual testing**
:   Testing by using the app yourself, by hand, and checking what happens.

    Learn more: [The SDET role](think-like-a-tester/the-sdet-role/index.md)

[](){ #marker }**Marker**
:   A label on a pytest test, like unit or ui, so you can run only the tests with that label.

    Learn more: [The test pyramid](think-like-a-tester/test-levels-and-the-pyramid/the-test-pyramid.md)

[](){ #microservice }**Microservice**
:   One small service that does one job. A big app can be made of many microservices talking to each other.

    Learn more: [Testing microservices](advanced-testing/testing-microservices/index.md)

[](){ #mock }**Mock**
:   A fake version of a real service, used in a test so you control exactly what it answers.

    Learn more: [Mocking and stubbing](advanced-testing/mocking-and-stubbing/index.md)

## N

[](){ #negative-test }**Negative test**
:   A test that sends bad input on purpose, like a wrong code or a short password, to check the app refuses it.

    Learn more: [The 9-step playbook](think-like-a-tester/learning-a-new-testing-area/the-9-step-playbook.md)

[](){ #non-functional-testing }**Non-functional testing**
:   Testing how well the app works, not what it does. For example, how fast it is, how easy it is to use, and whether it stays up.

    Learn more: [Non-functional testing](think-like-a-tester/test-levels-and-the-pyramid/non-functional-testing.md)

## O

[](){ #off-by-one-bug }**Off-by-one bug**
:   A bug where a limit is out by one step, like refusing age 18 when 18 should be allowed. Often caused by mixing up < and <=.

    Learn more: [Boundary values](think-like-a-tester/test-design-techniques/boundary-values.md)

## P

[](){ #page-object }**Page Object**
:   A class that holds everything a UI test needs about one page, so tests stay short and a page change is fixed in one place.

    Learn more: [UI automation](core-automation/ui-automation/index.md)

[](){ #pairwise-testing }**Pairwise testing**
:   Picking a small set of tests where every pair of settings, like Safari with PayPal, appears together at least once.

    Learn more: [Pairwise testing](think-like-a-tester/test-design-techniques/pairwise-testing.md)

[](){ #parametrize }**Parametrize**
:   A pytest feature that runs the same test many times, once for each row of values you give it.

    Learn more: [Equivalence partitioning](think-like-a-tester/test-design-techniques/equivalence-partitioning.md)

[](){ #percentile }**Percentile**
:   A way to describe speed. The 95th percentile is the time that 95 out of 100 requests were as fast as, or faster than.

    Learn more: [Non-functional testing](think-like-a-tester/test-levels-and-the-pyramid/non-functional-testing.md)

[](){ #performance-testing }**Performance testing**
:   Measuring how fast the app is and how much it can handle before it slows down or breaks.

    Learn more: [Performance testing](advanced-testing/performance-testing/index.md)

[](){ #pesticide-paradox }**Pesticide paradox**
:   Running the same tests again and again finds fewer new bugs over time. New tests and new data find new bugs.

    Learn more: [The seven testing principles](think-like-a-tester/the-sdet-role/seven-testing-principles.md)

[](){ #playbook }**Playbook**
:   A list of steps a team follows every time for the same kind of job, so nobody has to invent the plan again.

    Learn more: [The 9-step playbook](think-like-a-tester/learning-a-new-testing-area/the-9-step-playbook.md)

[](){ #playwright }**Playwright**
:   A tool that controls a real web browser from code, so a test can click, type and check a page.

    Learn more: [UI automation](core-automation/ui-automation/index.md)

[](){ #positive-test }**Positive test**
:   A test that checks something works when it should, like a refund within 30 days going through.

    Learn more: [Positive and negative cases](think-like-a-tester/test-cases/positive-and-negative-cases.md)

[](){ #practice-app }**Practice App**
:   The small online shop built for this site. It runs on your own computer and has bugs planted on purpose for you to find.

    Learn more: [Practice App tour](start-here/practice-app-tour/index.md)

[](){ #pre-commit }**pre-commit**
:   A tool that runs checks automatically every time you commit, and stops the commit if something is wrong.

    Learn more: [Static analysis tools](think-like-a-tester/static-testing-and-reviews/static-analysis-tools.md)

[](){ #precondition }**Precondition**
:   The state the system must be in before a test starts, like "a customer with one delivered item".

    Learn more: [Anatomy of a test case](think-like-a-tester/test-cases/anatomy-of-a-test-case.md)

[](){ #priority }**Priority**
:   How soon the team will fix a bug. The team decides it in triage, and the reporter can suggest one.

    Learn more: [Severity and priority](think-like-a-tester/bug-reports/severity-and-priority.md)

[](){ #pull-request }**Pull request**
:   A request to add your code changes to the team's main code. Others review it first.

    Learn more: [Git in a team](professional-sdet/git-in-a-team/index.md)

[](){ #pytest }**pytest**
:   The most popular tool for writing and running tests in Python.

    Learn more: [pytest framework](core-automation/pytest-framework/index.md)

## Q

[](){ #qa }**QA (Quality Assurance)**
:   All the work a team does to make sure the product is good, including testing.

    Learn more: [The SDET role](think-like-a-tester/the-sdet-role/index.md)

## R

[](){ #regression-testing }**Regression testing**
:   Running tests again after a change, to make sure things that worked before still work.

    Learn more: [Regression, hotfixes and incidents](professional-sdet/regression-hotfixes-and-incidents/index.md)

[](){ #rest }**REST (Representational State Transfer)**
:   The most common style of web API. You use web addresses for things and HTTP methods like GET and POST for actions.

    Learn more: [API testing](core-automation/api-testing/index.md)

[](){ #risk }**Risk**
:   Something that could go wrong, and how much it would hurt users or the company. Testers test the biggest risks first.

    Learn more: [Learning a new testing area](think-like-a-tester/learning-a-new-testing-area/index.md)

## S

[](){ #scope }**Scope**
:   What is part of a task, and what is not. Writing it down stops you from testing the wrong thing.

    Learn more: [Asking the right questions](think-like-a-tester/learning-a-new-testing-area/asking-the-right-questions.md)

[](){ #sdet }**SDET (Software Development Engineer in Test)**
:   A tester who writes code to test software.

    Learn more: [The SDET role](think-like-a-tester/the-sdet-role/index.md)

[](){ #severity }**Severity**
:   How badly a bug hurts the people using the app, from critical (money, data or security) to trivial (a typo). The reporter sets it.

    Learn more: [Severity and priority](think-like-a-tester/bug-reports/severity-and-priority.md)

[](){ #smoke-test }**Smoke test**
:   A few quick tests that check the most important things work, before you spend time on deeper testing.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #sql }**SQL (Structured Query Language)**
:   The language used to ask a database for data or change it, like SELECT * FROM orders.

    Learn more: [Database testing](core-automation/database-testing/index.md)

[](){ #state-transition }**State transition**
:   A move from one status to another, like an order going from paid to shipped. Testing them checks allowed moves work and the rest are refused.

    Learn more: [State transitions](think-like-a-tester/test-design-techniques/state-transitions.md)

[](){ #statement-coverage }**Statement coverage**
:   The share of code lines that ran at least once during the tests. 100% means every line ran, not that every line was checked.

    Learn more: [Statement and branch coverage](think-like-a-tester/test-design-techniques/statement-and-branch-coverage.md)

[](){ #static-analysis }**Static analysis**
:   Checking code for mistakes without running it, like a spell checker for code.

    Learn more: [Static analysis tools](think-like-a-tester/static-testing-and-reviews/static-analysis-tools.md)

[](){ #static-testing }**Static testing**
:   Checking work without running it, by reading stories, specs, plans and code, or by letting a tool read the code.

    Learn more: [What static testing is](think-like-a-tester/static-testing-and-reviews/what-is-static-testing.md)

[](){ #status-code }**Status code**
:   The number an API sends back to say how a request went, like 200 for OK or 404 for not found.

    Learn more: [API testing](core-automation/api-testing/index.md)

[](){ #steps-to-reproduce }**Steps to reproduce**
:   The numbered actions in a bug report that make the bug happen again, written so someone else can follow them.

    Learn more: [What makes a great bug report](think-like-a-tester/bug-reports/what-makes-a-great-bug-report.md)

[](){ #stub }**Stub**
:   A very simple fake that always gives the same ready answer, so a test does not need the real thing.

    Learn more: [Mocking and stubbing](advanced-testing/mocking-and-stubbing/index.md)

## T

[](){ #test-case }**Test case**
:   One check written down step by step, with the expected result, so anyone can run it the same way.

    Learn more: [Anatomy of a test case](think-like-a-tester/test-cases/anatomy-of-a-test-case.md)

[](){ #test-charter }**Test charter**
:   One sentence that sets the goal of an exploratory testing session. Explore something, with some idea, to find out something.

    Learn more: [Exploratory testing](think-like-a-tester/test-design-techniques/exploratory-testing.md)

[](){ #test-condition }**Test condition**
:   One thing worth testing, found by reading the story. For example, "a code older than 10 minutes must not work".

    Learn more: [The test process and testware](think-like-a-tester/the-sdet-role/test-process-and-testware.md)

[](){ #test-data }**Test data**
:   The users, products, orders and other data a test needs to run.

    Learn more: [Data-driven testing](core-automation/data-driven-testing/index.md)

[](){ #test-level }**Test level**
:   How much of the app a test uses at once, from one small function (unit) up to the whole system (end-to-end).

    Learn more: [The test levels](think-like-a-tester/test-levels-and-the-pyramid/the-test-levels.md)

[](){ #test-plan }**Test plan**
:   A short document that says what will be tested, how, by whom and when.

    Learn more: [Test strategy and planning](think-like-a-tester/test-strategy-and-planning/index.md)

[](){ #test-pyramid }**Test pyramid**
:   A picture of a healthy test mix. Many small, fast unit tests at the bottom, fewer integration tests, and only a few slow end-to-end tests at the top.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #testing-trophy }**Testing trophy**
:   Another picture of a healthy test mix, with static checks at the base and most tests checking parts working together.

    Learn more: [The testing trophy](think-like-a-tester/test-levels-and-the-pyramid/the-testing-trophy.md)

[](){ #testware }**Testware**
:   Everything testing produces, such as plans, test cases, test data, scripts, results and reports.

    Learn more: [The test process and testware](think-like-a-tester/the-sdet-role/test-process-and-testware.md)

[](){ #traceability }**Traceability**
:   The link between each requirement and the tests that check it, so you can see what has no test.

    Learn more: [Traceability](think-like-a-tester/test-cases/traceability.md)

[](){ #traceability-matrix }**Traceability matrix**
:   A table with one row per requirement and the test cases that cover it. Empty rows are gaps.

    Learn more: [Traceability](think-like-a-tester/test-cases/traceability.md)

[](){ #triage }**Triage**
:   Looking at new bugs, checking they are real and clear, and deciding how soon each one gets fixed.

    Learn more: [Severity and priority](think-like-a-tester/bug-reports/severity-and-priority.md)

## U

[](){ #ui }**UI (User Interface)**
:   The part of an app people see and use, like pages, buttons and forms.

    Learn more: [UI automation](core-automation/ui-automation/index.md)

[](){ #unit-test }**Unit test**
:   A small, fast test that checks one piece of code on its own.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #user-story }**User story**
:   A short description of a feature from the user's side, like "As a customer, I want to request a refund, so that I get my money back".

    Learn more: [Reviewing user stories](think-like-a-tester/static-testing-and-reviews/reviewing-user-stories.md)

## V

[](){ #virtual-environment }**Virtual environment**
:   A private folder of Python packages for one project, so projects do not mix up each other's versions.

    Learn more: [Environment setup](start-here/environment-setup/index.md)

## W

[](){ #walkthrough }**Walkthrough**
:   A review where the author takes others through their work, explaining it and taking questions.

    Learn more: [Review types](think-like-a-tester/static-testing-and-reviews/review-types.md)

[](){ #white-box-testing }**White-box testing**
:   Testing with a view of the code inside, for example to see which lines and branches the tests run.

    Learn more: [Statement and branch coverage](think-like-a-tester/test-design-techniques/statement-and-branch-coverage.md)

<!-- END glossary -->

Missing a word? [Tell us which one](https://github.com/arshaduzzaman-sm/zero-to-sdet/issues/new?template=content-error.yml&title=Glossary%3A%20add%20a%20word)
and we will add it.
