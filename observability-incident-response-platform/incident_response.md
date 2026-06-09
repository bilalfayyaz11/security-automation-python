# Incident Response Checklist

## Detection Phase

- [ ] Alert received from monitoring system
- [ ] Alert severity assessed
- [ ] Initial timestamp recorded
- [ ] Affected component identified

## Investigation Phase

- [ ] Check Prometheus metrics for anomalies
- [ ] Review Grafana dashboards
- [ ] Examine application logs through Loki
- [ ] Check system service logs
- [ ] Identify affected services
- [ ] Confirm incident scope

## Response Phase

- [ ] Document initial findings
- [ ] Implement mitigation steps
- [ ] Verify service restoration
- [ ] Continue monitoring for recurrence
- [ ] Escalate if user impact continues

## Resolution Phase

- [ ] Root cause identified
- [ ] Permanent fix applied
- [ ] Documentation updated
- [ ] Post-incident review scheduled

## Investigation Commands

### Check Active Alerts

curl http://localhost:9090/api/v1/alerts | jq

### Query Service Health

curl 'http://localhost:9090/api/v1/query?query=up' | jq

### View Application Logs

tail -f ~/observability-lab/app.log

### Query Loki Logs

curl -s "http://localhost:3100/loki/api/v1/query_range?query={job=\"application\"}&limit=5" | jq

### Check Application Service

systemctl status monitor-app --no-pager

### Check Recent Service Logs

journalctl -u monitor-app -n 50 --no-pager
