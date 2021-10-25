# simple_small_api
## For proper webapi you should probably be using FastAPI or Flask

## Development

Clone the code and install requirements :
```sh
pip install -r requirements_test.txt
```

You need a postgres db with a table. You can create it yourself with :
```sh
CREATE TABLE birthdays (username VARCHAR(255) PRIMARY KEY, birth_date DATE NOT NULL);
```
and supply the connection info via environment variables :
```sh
'PG_HOST' = "127.0.0.1"
'PG_PORT' = "5432"
'PG_USER' = "postgres"
'PG_PASSWORD' = "somePassword"
'PG_DB' = "postgres"
```

Or you can start it and create the table with in docker with :
```sh
./tools/start_postgres.sh
./tools/init_docker_postgres.sh
```
This can be used directly with the default connection settings (without environment variables)

You can run the code from the root of the repo with :
```sh
python src/simple_small_api.py
```
or if you want to see debug info :
```sh
PYLOGLEVEL=DEBUG python src/simple_small_api.py
```
Sample requests while the server is running :
```sh
curl -v -X PUT  localhost/hello/userone -d '{ "dateOfBirth": "1980-02-29" }'
curl -v localhost/hello/userone
```

Also , if you want to run the provided unit tests , use :
```sh
PYLOGLEVEL=DEBUG python -m unittest ../tests/test_logic_hello_functions.py
```

## Build and run docker image

Use the provided Dockerfile for build 
```sh
docker build -t simple_api .
```

You can then start it with :
```sh
docker run -d --rm --name simple -p 80:80  -e "PG_HOST=XX.XX.XX.XX" simple_api
```
Where XX.XX.XX.XX is your local ip ( you are no longer running the code on localhost , so the default postgres connection string does not work)

## Cloud (AWS)

You can use this in aws ( or other cloud).
Some kind of kubernetes deployment and postgres (rds or not) similar to :

![VPC](https://github.com/and-pac/simple_small_api/blob/e76a37a320e3f35393da1febf15fb1886aa5d095/tools/aws_schema/aws_kube_postgres.png)

## Helm

For deploying on kubernetes, you can use the provided helm chart .
The chart has been configured to support rolling updates , and you can fine tune this by the maxSurge and maxUnavailable values.

For a quick deployment , as long as kubectl and helm are configured , you can go to tools\helm_example and fill in the postgress details in the values.yaml and run the install.sh script.


## Ansible Rolling Deployment

If you do not want to use kubernetes , but would stil like to see a rolling deployment , you can use the scritps in the "ansible" folder.


1.	Start by provisioning 4 VMs , 3 to be used for docker and one for haproxy as our main loadbalancer. 
	( You can use the sample_Vagrantfile provided for starting these up in virtualbox. )
2.	Fill in the ansible inventory file with the ip's of the VMs
	( You are responsible for configuring ssh access to the VMs. I add your public key to the vagrant user with the Vagrant provisioner Script, so you should be able to login if you started them like this )
3.	Install docker and haproxy by running :
```sh
ansible-playbook -i inventory install_docker_and_haproxy.yaml -b
```

	This requires sudo permissions (become)
4.	Bring up a temporary postgress on configured docker server :
```sh
ansible-playbook -i inventory temp_postgres_in_docker.yaml
```

5.	Now you are ready to release the app. For this run :
```sh
ansible-playbook -i inventory release_app.yaml
```

	This will promt you for the release tag of the application. 
	It is configured to pick the images from dockerhub : andpac/simple_small_api
	You can use 2 versions : 0.0.2 and 0.0.3 
	The diffrence between the two is the code returned when calling /health 
	( 0.0.2 return 202 and 0.0.3 returns 200 )

	The script disables the server in the backend, updates the running app , checks it's running again, and finally reenables the server in the backend.
	The app is simple , so no need for drain or waiting time.

	Depending on the number of servers , you might want to add a check that we do not take out too much power at one time ( if you modify the serial setting ).

