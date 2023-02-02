# simple-pulumi-crud 0.1.0

This project is a simple CRUD application written in Python. The CRUD application uses DynamoDB as a database and is behind a REST API written with Flask and request validation by marshmallow.
Pulumi is used to define and deploy the stack, which consists of only the DynamoDB table and its indexes for now. A Docker file is included to define the image and deploy containers. Github Actions
is used as the CI/CD tool to run run unit tests, linters, and other various workflow actions.

## Requirements/Libraries:
<details><summary>Expand</summary>

- Python 3.10+
- AWS CLI installed and AWS account configured to user with permissions to create and destroy resources.
- Pulumi and configured Pulumi account to deploy to. 
- venv
- bumpver
- Flask

</details>


## Steps To Run
<details><summary>Expand</summary>
<p>

To run this locally, you will need the above requirements. Install Python 3.10+. Install Pulumi. You will need to create a Pulumi account and using the CLI, set the organization to your account. Install AWS CLI and create an AWS account. Create a user in that account and add to a group with enough permissions to create resources. Get an access token and secret and add it to your environment variables. Configure the AWS CLI to use that account and set the region. [Create a virtual environment with venv and activate it.](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

Once in the virtual environment, run a pip install. All the dependencies are listed here and in the pyproject.toml so install anything you might've missed.

Next step is to create the DynamoDB table. In your command line, navigate into the ./pulumi/ folder and run:
```
pulumi stack select
pulumi preview
pulumi up
```

You will need Pulumi installed and your account/organization set. After running pulumi stack select, it will ask you to create a new stack. Once the stack is created, you can preview the changes the __main__.py file defines and deploy by running a pulumi up. If you have configured your AWS account and CLI, it will create the table under your account and you should be able to see it in the AWS console once Pulumi is finished.  

To start the Flask API locally, run below:

```
flask -e flask.cfg run
```

This will run Flask and give it the flask.cfg file with some variables defined in it to enable debug mode and help it find the flask_api.py file. Open up something you can easily test your API with like Postman and you can use the simple-pulumi-crud-collection JSON file to test out the endpoints. Run the create_user first so that you will have some dummy data to test.
</p>
</details>
