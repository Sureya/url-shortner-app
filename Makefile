push-code:
	git add .
	git commit -m "Automated push at : $(date)"
	git push

start-app:
	gunicorn app:app -b 0.0.0.0:9558 -w 5

