import setuptools


setuptools.setup(
	name="snapshotalyzer-3000",
	version="1",
	author="Edgar Arevalo",
	author_email="edgarevalo1990@gmail.com",
	description="",
	license="GLP",
	packages=["shotty"],
	url="https://github.com/edgarevalo/snapshotalyzer-3000/",
	install_requires=[
		"click",
		"boto3"],
	entry_points='''
		[console_scripts]
		shotty=shotty.shotty:cli
		''',

)