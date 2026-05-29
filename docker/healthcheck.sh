FILE=/app/runtime/heartbeat.txt
if [ -f "$FILE" ]; then
    # Must be updated within last 2 minutes
    if test `find "$FILE" -mmin -2`; then
        exit 0
    else
        echo "Heartbeat stale"
        exit 1
    fi
else
    echo "Heartbeat missing"
    exit 1
fi
