# Operations Runbook

Personal notes for managing the live deployment. Not for public distribution.

---

## Server Access

```bash
# Fix permissions on first use
chmod 600 "<PATH_TO_YOUR_KEY>.pem"

# SSH into VPS
ssh -i "<PATH_TO_YOUR_KEY>.pem" ubuntu@<YOUR_SERVER_IP>

# Verbose SSH (debug hangs)
ssh -vvv -i "<PATH_TO_YOUR_KEY>.pem" ubuntu@<YOUR_SERVER_IP>
```

---

## Initial Server Setup

### Install Docker + Compose plugin

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu noble stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Fix directory ownership

```bash
sudo chown -R 1000:1000 ~/bots/trading-bot/logs
sudo chown -R 1000:1000 ~/bots/trading-bot/backups
sudo chown -R 1000:1000 ~/bots/trading-bot/runtime
sudo chown -R 1000:1000 ~/bots/trading-bot/config
```

### Fix Docker socket permission denied

```bash
sudo usermod -aG docker ubuntu
newgrp docker
```

---

## Daily Operations

### Navigate to project

```bash
cd ~/bots/trading-bot
```

### Start / stop

```bash
docker-compose up -d
docker-compose down
docker-compose up -d bot
```

### Rebuild after file change

```bash
docker-compose build bot
docker-compose up -d --build bot
docker-compose up -d --build --force-recreate bot
```

### View live logs

```bash
docker-compose logs -f bot
docker-compose logs --tail 50 bot
docker-compose logs --since "2025-12-15T18:00:00Z" bot > bot_history.log
```

### Check container health

```bash
docker ps -a
docker inspect --format='{{json .State.Health}}' trading_bot | jq
```

### Run daily summary

```bash
docker exec trading_bot python3 summary.py
```

---

## Log & File Access

### Read logs on server

```bash
cat logs/bot.log
cat logs/trades.csv
grep -i "BUY" logs/bot.log
grep -i "SELL" logs/bot.log
```

### Download logs to Mac

```bash
scp -i "<PATH_TO_YOUR_KEY>.pem" ubuntu@<YOUR_SERVER_IP>:/home/ubuntu/Trading-Bot/Trading-Bot/logs/bot.log ~/Desktop/bot_local.log
scp -i "<PATH_TO_YOUR_KEY>.pem" ubuntu@<YOUR_SERVER_IP>:/home/ubuntu/Trading-Bot/Trading-Bot/logs/trades.csv ~/Desktop/
```

### List container contents

```bash
docker exec -it crypto_bot ls -la /app
```

### Clear log file (without deleting)

```bash
truncate -s 0 ~/Trading-Bot/Trading-Bot/logs/bot_local.log
```

---

## Backups

### Manual backup (skip waiting for midnight cron)

```bash
cd ~/Trading-Bot/Trading-Bot
tar -czf /home/ubuntu/Trading-Bot/Trading-Bot/backups/backup_$(date +\%Y\%m\%d_\%H\%M\%S).tar.gz \
  -C /home/ubuntu/Trading-Bot/Trading-Bot logs configs runtime
```

### Download backups to Mac

```bash
scp -i "<PATH_TO_YOUR_KEY>.pem" ubuntu@<YOUR_SERVER_IP>:/home/ubuntu/Trading-Bot/Trading-Bot/backups/\* ~/Desktop/
```

---

## Weekly Cleanup Routine

```bash
# Run cleanup script
~/cleanup.sh

# Check disk and memory
df -h
free -h

# Remove unused Docker artifacts
docker system prune -af --volumes
docker volume prune -f

# Nuclear option (removes all stopped containers and images)
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -q)
docker system prune -af --volumes

# Clear apt cache
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

# Clear pip cache
sudo rm -rf /root/.cache/pip

# Check log sizes
sudo du -sh /var/log/*
sudo truncate -s 0 /var/log/*.log

# Check Docker disk usage
sudo du -sh /var/lib/docker
docker system df
```

---

## Deploying New Code

Push from Mac — the CI/CD pipeline handles the rest:

```bash
git push origin main
```

The GitHub Actions workflow SSHs into the server, pulls, rebuilds, and restarts the container automatically.

After changing `docker-compose.yml` manually on the server:

```bash
docker-compose up -d --force-recreate bot
```

---

## Troubleshooting

### Remove stale containers / networks

```bash
docker stop hybrid_crypto_bot
docker rm hybrid_crypto_bot
docker network rm crypto-bot_default
docker rmi crypto-bot:latest
```

### Edit a file directly on the server

```bash
nano docker-compose.yml
```

### Verify a specific source file inside the container

```bash
docker exec -it crypto_bot cat /app/src/backup.py
```

### Verify path on the host

```bash
ls -l ~/Trading-Bot/Trading-Bot/src/system/backup.py
```

---

## Monitoring Checklist (Daily)

- `docker ps` → confirm `trading_bot` is running
- `docker logs --tail 50 crypto-bot` → scan for errors
- Check `/app/backups` is populated
- Run `docker system prune -af` once a week

---

## TODO

- Wire up a CloudWatch alarm that sends a Telegram alert whenever the EC2 instance stops or terminates (fallback for when the bot itself can't send a STOPPED message).
