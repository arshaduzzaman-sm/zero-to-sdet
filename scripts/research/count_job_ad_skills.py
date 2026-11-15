"""Count how many job ads mention each SDET skill, split by level.

Keyword-based: each pattern is a rough signal, so read the numbers as
"often / sometimes / rarely asked for", not exact market share.

Usage:
    python3 scripts/research/count_job_ad_skills.py ADS_DIR INDEX_OUT.json
"""
import json, re, sys, pathlib, collections
ads = [json.loads(p.read_text()) for p in sorted(pathlib.Path(sys.argv[1]).glob("*.json"))]
def level(t):
    t=t.lower()
    if re.search(r"junior|recent graduate|specialist i\b|engineer ii\b|developer in test ii|automation tester", t): return "Junior"
    if re.search(r"lead|staff|principal|engineer iv\b", t): return "Lead"
    if "senior" in t or re.search(r"\bsr\b", t): return "Senior"
    return "Mid"
S = {
 "Python": r"\bpython\b", "Java": r"\bjava\b(?!script)", "JavaScript/TypeScript": r"javascript|typescript|\bjs\b|\bts\b",
 "C#/.NET": r"c#|\.net\b", "Go": r"\bgolang\b|\bgo\b(?= |,)(?=.*(?:python|java))",
 "pytest": r"pytest|py\.test", "unittest/JUnit/TestNG": r"unittest|junit|testng|nunit",
 "Robot Framework": r"robot framework",
 "Playwright": r"playwright", "Selenium": r"selenium|webdriver", "Cypress": r"cypress",
 "Appium / mobile testing": r"appium|espresso|xcuitest|mobile (?:testing|automation|qa)|\bios\b|android",
 "API testing (REST)": r"\bapis?\b|rest(?:ful)?\b", "Postman/Newman/Bruno": r"postman|newman|bruno|insomnia",
 "requests / HTTP": r"\bhttp\b|requests library|\brequests\b",
 "GraphQL": r"graphql", "gRPC": r"grpc|protobuf", "WebSocket": r"websocket",
 "Auth: OAuth/JWT/tokens": r"oauth|jwt|\bsaml\b|\bsso\b|authenticat",
 "Schema/contract (OpenAPI, Pact)": r"openapi|swagger|json schema|\bpact\b|contract test",
 "SQL / databases": r"\bsql\b|postgres|mysql|database|oracle|sql server",
 "NoSQL (MongoDB etc.)": r"nosql|mongo|dynamodb|cassandra|redis",
 "ETL / data validation": r"\betl\b|\belt\b|data pipeline|data validation|data quality|snowflake|spark",
 "BDD / Gherkin / Cucumber": r"\bbdd\b|gherkin|cucumber|behave|pytest-bdd",
 "Test data / Faker / factories": r"test data|faker|synthetic data|data generation",
 "Mocking / service virtualization": r"\bmock|stub|service virtuali|wiremock",
 "Performance (JMeter, k6, Locust)": r"performance test|load test|stress test|jmeter|\bk6\b|locust|gatling|loadrunner",
 "Security testing / OWASP": r"security test|owasp|penetration|vulnerab|\bzap\b|burp",
 "Accessibility (WCAG)": r"accessib|wcag|section 508|\baxe\b",
 "Visual regression": r"visual (?:regression|testing)|percy|applitools",
 "Message queues (Kafka etc.)": r"kafka|rabbitmq|\bsqs\b|pub/?sub|message queue|event-driven",
 "Microservices / distributed": r"microservice|distributed system|distributed architecture",
 "AI/LLM testing or AI tools": r"\bllms?\b|genai|ai[- ](?:assisted|driven|powered) (?:test|automation|coding|development|tool)|(?:test|testing|validat|evaluat)\w* (?:of )?(?:ai|ml|llm)|copilot|cursor|prompt (?:design|engineering)|ai tools",
 "CI/CD (general)": r"ci/cd|continuous integration|pipeline",
 "GitHub Actions": r"github actions", "Jenkins": r"jenkins", "GitLab CI": r"gitlab", "Azure DevOps": r"azure devops",
 "Docker / containers": r"docker|container", "Kubernetes": r"kubernetes|\bk8s\b|helm",
 "Cloud (AWS/Azure/GCP)": r"\baws\b|azure|\bgcp\b|google cloud",
 "Linux / shell": r"linux|unix|bash|shell", "Networking (TCP/IP, DNS)": r"tcp|\bdns\b|networking|\bhttps?\b protocol|load balanc",
 "Git / version control": r"\bgit\b|github|version control|bitbucket",
 "Observability (logs, Grafana, Datadog)": r"observability|grafana|datadog|prometheus|splunk|kibana|monitoring|\btraces?\b",
 "Debugging / root cause": r"debug|root cause|troubleshoot|triage",
 "Reporting (Allure etc.)": r"allure|test report|reporting|dashboards?",
 "Flaky tests / reliability": r"flak|test stabilit|stable tests|reliable (?:test|automation)|test reliab|script stabilit",
 "Parallel / test speed": r"parallel|execution time|xdist|sharding",
 "Framework design / architecture": r"framework (?:design|architect|development)|design(?:ing)? (?:and|&) (?:build|develop|implement)|architect|scalable (?:test|automation)|build(?:ing)? (?:test )?framework",
 "Design patterns / Page Object": r"page object|design pattern|\bpom\b|solid principles",
 "Test design techniques": r"boundary|equivalence|test design|edge case|exploratory",
 "Manual / exploratory testing": r"manual test|exploratory",
 "Test strategy / test planning": r"test strateg|test plan|quality strategy|testing strategy|test approach",
 "Test cases / test management (TestRail, Xray)": r"test case|testrail|xray|zephyr|test management",
 "Bug reports / defect lifecycle": r"\bbugs?\b|defect",
 "Regression / smoke": r"regression|smoke",
 "Risk-based testing": r"risk-based|risk analysis|risk assessment|quality risk|surfac\w* risk|identify\w* risk|testing risk",
 "Test pyramid / unit-integration-e2e": r"pyramid|unit test|integration test|end-to-end|e2e",
 "Shift-left / testability": r"shift-left|shift left|testability",
 "Agile / Scrum": r"agile|scrum|kanban|sprint",
 "Jira": r"\bjira\b",
 "Code review / pull requests": r"code review|pull request|peer review",
 "Clean code / OOP": r"clean code|object[- ]oriented|\boop\b|maintainab|readab",
 "Communication / collaboration": r"communication skills|communicat\w* (?:clearly|effectively|with)|collaborat\w* (?:with|closely|across)|cross-functional",
 "Mentoring / leadership": r"mentor|coach|lead (?:a |the )?team|leadership",
 "Quality metrics / KPIs": r"quality metric|test metric|metrics|kpi|test coverage|code coverage",
 "Release / quality gates": r"release (?:process|cycle|readiness|sign|quality)|quality gate|go/no-go|release",
 "Requirements / acceptance criteria": r"requirement|acceptance criteria|user stor",
 "Compliance (HIPAA, SOC2, PCI)": r"hipaa|soc ?2|pci|gdpr|compliance",
 "Excel/CSV/JSON data handling": r"\bjson\b|\bcsv\b|\byaml\b|excel",
}
lv = collections.Counter(level(a["title"]) for a in ads)
cnt = {k: collections.Counter() for k in S}
for a in ads:
    t = a["title"]+" "+a["text"]; L = level(a["title"])
    for k,p in S.items():
        if re.search(p, t, re.I): cnt[k][L]+=1
n=len(ads); print(f"ADS={n} levels={dict(lv)}")
for k in sorted(S, key=lambda k:-sum(cnt[k].values())):
    c=cnt[k]; tot=sum(c.values())
    print(f"{tot:3} {100*tot//n:3}% | J{c['Junior']:2} M{c['Mid']:2} S{c['Senior']:2} L{c['Lead']:2} | {k}")
print("\nBDD tool mentions:")
for name,p in {"behave":r"\bbehave\b","pytest-bdd":r"pytest-bdd","cucumber":r"cucumber","gherkin":r"gherkin"}.items():
    print(name, sum(bool(re.search(p,a["text"],re.I)) for a in ads))
json.dump([dict(company=a["company"],title=a["title"],location=a["location"],url=a["url"],level=level(a["title"])) for a in ads], open(sys.argv[2],"w"), indent=1)
