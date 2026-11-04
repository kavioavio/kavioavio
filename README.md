## Hi, I'm Sergei.

Ten years at banks, most of it integration middleware on the IBM WebSphere stack: MQ, Integration Bus, the application server. Kafka architecture since 2024. That work taught me one habit: when something reports success, go look. Now the thing reporting success is an AI agent.

```console
$ agent deploy --prod
✓ Deployed. All checks passed.

$ curl -sf prod/health
curl: (7) Failed to connect

$ agent "prod is down"
You're absolutely right!
I never started the service.
```

## Zidos

I'm building [Zidos](https://zidos.dev), an agent on its own core. Commands run in a sandbox or they don't run. Every step lands in an append-only log, and a crashed run resumes from that log. Anything that touches a real system waits for your yes, and "finished" is decided by a verifier the runtime runs. Works with your Claude, ChatGPT or Gemini subscription. Free beta now. We plan to open the core and apps under Apache-2.0 at launch.

## Open source

**[Zidos Pager](https://github.com/zidos-dev/pager)** puts Claude Code in Telegram. Background sessions get their own topics, tool approvals arrive as buttons, and a mini-app shows history and subagents. It also runs group assistant bots on any model. One Python file, standard library only. [Download for macOS, Windows or Linux](https://github.com/zidos-dev/pager/releases/latest).

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/cc-tgbot-phone-dark.png">
    <source media="(max-width: 600px)" srcset="./assets/cc-tgbot-phone-light.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zidos-dev/pager/main/docs/hero-dark.png">
    <img src="https://raw.githubusercontent.com/zidos-dev/pager/main/docs/hero-light.png" width="720" alt="Zidos Pager mini-app: a session asking which cache to use, with three options as buttons">
  </picture>
</p>

## Rules I learned the hard way

- If the docs claim it, there should be a check that fails when it stops being true.
- Configure, apply, read back, roll back: that's one change, not four.
- Health checks turn green long before the real client works. Test the client.
- Rehearse the restore on a clean host before you need it.
- A green exit code is not a result. Not from a test, not from a script, and definitely not from a model.

## What I know well

- **Banking integration:** IBM MQ and IBM Integration Bus in HA clusters, WebSphere Application Server, SSL, capacity planning.
- **Kafka:** KRaft, quorum and replication factor sizing, SASL with Kerberos, Keycloak, ACL automation in YAML and bash, hardening templates, Strimzi on Kubernetes.
- **CDC and connectors:** Debezium with Kafka Connect.
- **Other messaging:** RabbitMQ quorum queues, on OpenShift too; WSO2.
- **Operations:** Zabbix, Grafana and Prometheus, L3 runbooks, troubleshooting live clusters.
- **Everyday tools:** Linux, Bash, Python, Go, Git.

<details>
<summary>Public GitHub activity</summary>
<br>
<p align="center">
  <img src="./github-metrics.svg" alt="Public GitHub activity and contribution calendar" width="480" />
</p>
</details>

## Say hi

I take consulting work: Kafka, IBM MQ and Integration Bus, and the integration platforms around them. A cluster acting up, a migration, or an agent that keeps "succeeding"? Write to me on [LinkedIn](https://www.linkedin.com/in/sergei-ivanov-73856b3a7).

<!-- github-profile-readme -->
