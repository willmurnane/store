restart:
	pkill python; touch ../passenger_wsgi.py

sql:
	if [[ `hostname` == "force" ]]; then mysql -u django_store -p'insecure!' -h mysql.twoevils.net django_store; else sqlite3 store.db; fi

syncdb:
	python manage.py syncdb

shell:
	python manage.py shell
