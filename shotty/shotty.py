import boto3
import click
import csv


session = boto3.Session(profile_name='edgar')

ec2 = session.resource('ec2')

@click.command()
@click.option('--project', default=None, help="Only instances for project(tag Project=:<name>)")

def list_instances(project):
	"List EC2 instances"
	instances = []
	

	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()  
	with open('instances.csv', 'w') as csvfile: #esta parte la agregué para que escriba el output en un CSV
		writer = csv.writer(csvfile)
		writer.writerow(['ID', 'Zona', 'Stado', 'DNS', 'Projecto'])		
		for i in instances:
			tags = { t['Key']: t['Value'] for t in i.tags  or []}	
			writer.writerow([i.id, i.placement, i.state, i.public_dns_name, tags.get('Project', '<no project>')])
			print(','.join((
				i.id,
				i.instance_type,
				i.placement['AvailabilityZone'],
				i.state['Name'],
				i.public_dns_name,
				tags.get('Project', '<no project>')
				)))
			#writer.writerow([i.id, i.placement, i.state, i.public_dns_name, tags.get('Project', '<no project>')])

	return

if __name__ == '__main__':
	list_instances()
