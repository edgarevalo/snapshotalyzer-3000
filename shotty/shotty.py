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
	nombreArchivo=project 
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

	return
def stop_instances():
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
if __name__ == '__main__':
	#list_instances()
	stop_instances()