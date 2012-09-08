restart:
	pkill python; touch ../passenger_wsgi.py

sql:
	mysql -u django_store -p'insecure!' -h mysql.twoevils.net django_store

syncdb:
	python manage.py syncdb

shell:
	python manage.py shell
