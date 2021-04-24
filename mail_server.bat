set MAIL_SERVER=localhost
set MAIL_PORT=8025
py -m smtpd -n -c DebuggingServer localhost:8025
