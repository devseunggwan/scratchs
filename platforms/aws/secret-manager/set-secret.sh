SECRET_ID=""
SECRET_STRING=""

aws secretsmanager create-secret \
    --name "$SECRET_ID" \
    --secret-string "$SECRET_STRING"
