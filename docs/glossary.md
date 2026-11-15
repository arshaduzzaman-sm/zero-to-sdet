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

<nav class="zts-az" aria-label="Jump to a letter" markdown>[A](#a) [B](#b) [C](#c) [D](#d) [E](#e) [F](#f) [G](#g) [H](#h) [I](#i) [J](#j) [L](#l) [M](#m) [N](#n) [P](#p) [Q](#q) [R](#r) [S](#s) [T](#t) [U](#u) [V](#v)</nav>

## A

[](){ #acceptance-criteria }**Acceptance criteria**
:   The list of things a feature must do before the team calls it finished. Testers turn each one into tests.

    Learn more: [Test cases](think-like-a-tester/test-cases/index.md)

[](){ #accessibility }**Accessibility**
:   How easy the app is to use for everyone, including people who use a screen reader, a keyboard only, or large text.

    Learn more: [Accessibility testing](advanced-testing/accessibility-testing/index.md)

[](){ #api }**API (Application Programming Interface)**
:   A way for one program to ask another program for data or to do something. Like a waiter who takes your order to the kitchen and brings back your food.

    Learn more: [API testing](core-automation/api-testing/index.md)

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

    Learn more: [Test design techniques](think-like-a-tester/test-design-techniques/index.md)

[](){ #bug-report }**Bug report**
:   A short note that tells a developer what went wrong, how to make it happen again, and what should have happened instead.

    Learn more: [Bug reports](think-like-a-tester/bug-reports/index.md)

## C

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

[](){ #defect-clustering }**Defect clustering**
:   Most bugs hide in a few parts of a system. When you find one bug, look for more nearby.

    Learn more: [The seven testing principles](think-like-a-tester/the-sdet-role/seven-testing-principles.md)

[](){ #docker }**Docker**
:   The most common tool for building and running containers.

    Learn more: [Docker for testers](infrastructure/docker-for-testers/index.md)

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

    Learn more: [Test design techniques](think-like-a-tester/test-design-techniques/index.md)

[](){ #exploratory-testing }**Exploratory testing**
:   Testing by learning the app as you go, trying ideas and following anything that looks odd, instead of following a script.

    Learn more: [Test design techniques](think-like-a-tester/test-design-techniques/index.md)

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

## P

[](){ #page-object }**Page Object**
:   A class that holds everything a UI test needs about one page, so tests stay short and a page change is fixed in one place.

    Learn more: [UI automation](core-automation/ui-automation/index.md)

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

[](){ #practice-app }**Practice App**
:   The small online shop built for this site. It runs on your own computer and has bugs planted on purpose for you to find.

    Learn more: [Practice App tour](start-here/practice-app-tour/index.md)

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

[](){ #smoke-test }**Smoke test**
:   A few quick tests that check the most important things work, before you spend time on deeper testing.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #sql }**SQL (Structured Query Language)**
:   The language used to ask a database for data or change it, like SELECT * FROM orders.

    Learn more: [Database testing](core-automation/database-testing/index.md)

[](){ #status-code }**Status code**
:   The number an API sends back to say how a request went, like 200 for OK or 404 for not found.

    Learn more: [API testing](core-automation/api-testing/index.md)

[](){ #stub }**Stub**
:   A very simple fake that always gives the same ready answer, so a test does not need the real thing.

    Learn more: [Mocking and stubbing](advanced-testing/mocking-and-stubbing/index.md)

## T

[](){ #test-case }**Test case**
:   One check written down step by step, with the expected result, so anyone can run it the same way.

    Learn more: [Test cases](think-like-a-tester/test-cases/index.md)

[](){ #test-condition }**Test condition**
:   One thing worth testing, found by reading the story. For example, "a code older than 10 minutes must not work".

    Learn more: [The test process and testware](think-like-a-tester/the-sdet-role/test-process-and-testware.md)

[](){ #test-data }**Test data**
:   The users, products, orders and other data a test needs to run.

    Learn more: [Data-driven testing](core-automation/data-driven-testing/index.md)

[](){ #test-plan }**Test plan**
:   A short document that says what will be tested, how, by whom and when.

    Learn more: [Test strategy and planning](think-like-a-tester/test-strategy-and-planning/index.md)

[](){ #test-pyramid }**Test pyramid**
:   A picture of a healthy test mix. Many small, fast unit tests at the bottom, fewer integration tests, and only a few slow end-to-end tests at the top.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

[](){ #testware }**Testware**
:   Everything testing produces, such as plans, test cases, test data, scripts, results and reports.

    Learn more: [The test process and testware](think-like-a-tester/the-sdet-role/test-process-and-testware.md)

## U

[](){ #ui }**UI (User Interface)**
:   The part of an app people see and use, like pages, buttons and forms.

    Learn more: [UI automation](core-automation/ui-automation/index.md)

[](){ #unit-test }**Unit test**
:   A small, fast test that checks one piece of code on its own.

    Learn more: [Test levels and the pyramid](think-like-a-tester/test-levels-and-the-pyramid/index.md)

## V

[](){ #virtual-environment }**Virtual environment**
:   A private folder of Python packages for one project, so projects do not mix up each other's versions.

    Learn more: [Environment setup](start-here/environment-setup/index.md)

<!-- END glossary -->

Missing a word? [Tell us which one](https://github.com/arshaduzzaman-sm/zero-to-sdet/issues/new?template=content-error.yml&title=Glossary%3A%20add%20a%20word)
and we will add it.
