import boto3
import click
import csv
import time


session = boto3.Session(profile_name='edgar')

ec2 = session.resource('ec2')

@click.command()
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
def stop_instances(): #esta parte se encarga de apagar las instancias
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

def start_instances(): #esta parte se encarga de encender las instancias
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

if __name__ == '__main__':
	seleccion = input("escriba el comando: ")
	if seleccion == "list":
		list_instances()
	if seleccion == "stop": 
		stop_instances()
	else: start_instances()