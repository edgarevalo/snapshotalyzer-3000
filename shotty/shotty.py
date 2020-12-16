import boto3
import click
import csv
import time


session = boto3.Session(profile_name='edgar')

ec2 = session.resource('ec2')

#########################################################################

@click.group() #Main group called CLI

def cli():
	#Shotty manages snapshots
	return

@cli.group('volumes') #Branch group attached to CLI

def volumes():
	"""Commands for volumes"""
	return

@volumes.command('list')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def list_volumes(project):
	instances = []
	
	project = input("Cual es el nombre del proyecto? ")
	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all() 
	
	if project == "": 
		nombreArchivo = "lista-instancias"
	else: nombreArchivo=project 
	
	guardarEnArchivo = input("Desea guardar el resultado en un CSV? (si/no): ")
	if guardarEnArchivo == "si":
		with open(nombreArchivo+'.csv', 'w') as csvfile: #esta parte la agregué para que escriba el output en un CSV
			writer = csv.writer(csvfile)
			writer.writerow(['ID', 'Zona', 'Stado', 'DNS', 'Projecto'])		
			for i in instances:
				tags = { t['Key']: t['Value'] for t in i.tags  or []}
				writer.writerow([i.id, i.placement, i.state, i.public_dns_name, tags.get('Project', '<no project>')]) #aqui escribe linea a linea en el archivo
				for v in i.volumes.all():
					print(", ".join((v.id, i.id, v.state, str(v.size) + "GB", v.encrypted and "Encrypted" or "Not Encrypted" )))
			print("\n")		
	else:
		for i in instances:
			tags = { t['Key']: t['Value'] for t in i.tags  or []}
			for v in i.volumes.all():
					print(", ".join((v.id, i.id, v.state, str(v.size) + "GB", v.encrypted and "Encrypted" or "Not Encrypted" )))
			print("\n ")		
	return
###############################################################################
@cli.group('snapshots')

def snapshots():
	"""Commands for snapshots"""
	return

@snapshots.command('list')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def list_snapshots(project):

	instances = []

	instances = ec2.instances.all() 

	snappy = None

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				snappy = s
				print(", ".join((
					s.id,
					v.id,
					i.id,
					s.state,
					s.progress,
					s.start_time.strftime("%c")
					)))
	return

##############################################################################

@snapshots.command('create_project')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def create_snapshot_project(project):
   #"Create snapshots for EC2 instances in a specific project"

	instances = []

	snappy = None
	
	
	project=input("Cual es el nombre del projecto?: ")
	filters = [{'Name':'tag:Project', 'Values':[project]}]
	instances = ec2.instances.filter(Filters=filters)

	for i in instances:
		for v in i.volumes.all():
		
			print(" ")
			print("Creating snapshot for {0}.".format(i.id))
			time.sleep(0.5)
			v.create_snapshot()
			time.sleep(0.5)
			print("Snapshot for {0}.".format(i.id) + "requested")
			print(" ")
	print("Snapshots requested")		

	return



##############################################################################

@snapshots.command('create')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def create_snapshot(project):
   #"Create snapshots for EC2 instances"

	instances = []

	snappy = None
	ID=input("Cual es el id de la instancia?: ").split()
	

	instances = ec2.instances.filter(InstanceIds=ID)
	str1 =  ""
	nombreDeInstancia= str1.join(ID) 

	for i in instances:
		for v in i.volumes.all():
		
			print(" ")
			print("Creating snapshot for {0}.".format(i.id))
			time.sleep(0.5)
			v.create_snapshot()
			time.sleep(0.5)
			print("Snapshot for {0}.".format(i.id) + "requested")
			print(" ")
	print("Snapshots requested")		

	return


###############################################################################

@cli.group('instances') #Branch group attached to CLI

def instances():
	"""Commands for instances"""
	return

###############################################################################################################

@instances.command('list')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def list_instances(project):
	"List EC2 instances"
	instances = []
	
	project = input("Cual es el nombre del proyecto? ")
	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all() 
	
	if project == "": 
		nombreArchivo = "lista-instancias"
	else: nombreArchivo=project 
	
	guardarEnArchivo = input("Desea guardar el resultado en un CSV? (si/no): ")
	if guardarEnArchivo == "si":
		with open(nombreArchivo+'.csv', 'w') as csvfile: #esta parte la agregué para que escriba el output en un CSV
			writer = csv.writer(csvfile)
			writer.writerow(['ID', 'Zona', 'Stado', 'DNS', 'Projecto'])		
			for i in instances:
				tags = { t['Key']: t['Value'] for t in i.tags  or []}
				writer.writerow([i.id, i.placement, i.state, i.public_dns_name, tags.get('Project', '<no project>')]) #aqui escribe linea a linea en el archivo
				print(','.join((
					i.id,
					i.instance_type,
					i.placement['AvailabilityZone'],
					i.state['Name'],
					i.public_dns_name,
					tags.get('Project', '<no project>')
					)))
	else:
		for i in instances:
			tags = { t['Key']: t['Value'] for t in i.tags  or []}
			print(','.join((i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project', '<no project>')
			)))
	return
###############################################################################


@instances.command('stop')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def stop_instances(project): #esta parte se encarga de apagar las instancias
	"Stop instance by ID"

	ID=input("Cual es el id de la instancia?: ").split()
	instances = ec2.instances.filter()
	str1 =  ""
	nombreDeInstancia= str1.join(ID) 
	time.sleep(0.5)
	instances.stop(InstanceIds=ID)
	print("Instance "+ nombreDeInstancia + " stopped")
	
################################################################################
@instances.command('start')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")


def start_instances(project): #esta parte se encarga de apagar las instancias
	"Start instance by ID"


	ID=input("Cual es el id de la instancia?: ").split()
	instances = ec2.instances.filter()
	str1 =  ""
	nombreDeInstancia= str1.join(ID) 
	time.sleep(0.5)
	instances.start(InstanceIds=ID)
	print("Instance "+ nombreDeInstancia + " started")

################################################################################

@instances.command('stop_project')

@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def stop_instances(project): #esta parte se encarga de apagar las instancias
	"Stop instances"
	instances = []
	
	project = input("Cual es el nombre del proyecto? ")
	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all() 
	for i in instances:
		print("Stopping {0}...".format(i.id))
		time.sleep(0.5)
		i.stop()
	print("All Instances stopped")

#################################################################################

@instances.command('start_project')
@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def start_instances(project): #esta parte se encarga de encender las instancias
	"Start instances"
	instances = []
	
	project = input("Cual es el nombre del proyecto? ")
	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all() 
	for i in instances:
		print("Starting {0}...".format(i.id))
		time.sleep(0.5)
		i.start()
	print("All Instances started")	



#################  MAIN ###################

if __name__ == '__main__':
	"""seleccion = input("escriba el comando: ")
	if seleccion == "list":
		list_instances()
	if seleccion == "stop": 
		stop_instances()
	else: start_instances()"""
	#instances()
	cli()