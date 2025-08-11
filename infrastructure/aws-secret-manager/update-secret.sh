SECRET_ID=""
SECRET_STRING=""

aws secretsmanager update-secret \
    --secret-id "$SECRET_ID" \
    --secret-string "$SECRET_STRING"
