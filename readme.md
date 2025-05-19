# Training app

This app is just an example app for showcasing github actions

# Connect to Openshift

Before we get started with this training app we want to get connected to openshift, to do that [login](https://cloud.ibm.com) and go to the openshift cluster under `containers` > `clusters` and click on the one called `two-day-course`

This will open a new page which will show you an overview of the cluster, click on the `OpenShift web console` button at the top right.

This will open up a new tab, now click on your name at the top right, then click on the `copy login command` This will take you to a new page with a `Display token` hyperlink, click on that and you will get the oc login command displayed, copy and paste that into your terminal to authenticate against the openshift cluster.

Once you are authenticated you want to create a new project for yourself with the following command, replacing `<user>` with your name

```bash
oc new-project <user>
```

# Setup

## Prerequisites

To get this app running you first want to ensure you have python 3 installed. You can do that by downloading the latest version [from here](https://www.python.org/downloads/)

Once you have that installed you might need to restart your terminal for it to pick up the new install, you can test with:

```python
python --version
```

If everything is working you should see a version number printed out, somehting like `python 3.13.3`.

## Create virtual environment

Once that is working you will need to setup a virtual environment, this will isolate any dependancies from the rest of your system to avoid conflicts. To do that you will run this command:

`python -m venv venv`

This will create a new directory called `venv` which contains all the local depenancies for the virtual environment. To assume it in your terminal you will execute a different command depending on your OS, if you are a linux or mac user then you will run `source venv/bin/activate` If you are running windows it will be `C:\> <venv>\Scripts\activate.bat` if using cmd or `PS C:\> <venv>\Scripts\Activate.ps1` for powershell, if you are having problems have a look at the [docs](https://docs.python.org/3/library/venv.html)

## Install depenancies

once you have assumed your virtual environment you will want to install the dependancies with this command:

```bash
pip install -r requirements.txt
```

If that fails try this command:

```bash
python -m pip install -r requirements.txt
```

That will install the dependancies for running this test app

# Running the app

To start the app run this command:

```bash
python app.py
```

That should start the app and you will see some test in the terminal saying:
```bash
* Running on all address (0.0.0.0)
* Running on http://127.0.0.1:5000
```

So long as there are no errors showing then it should have worked and you can test it by going to the browser and entering in this url:

http://localhost:5000

you should now see a blank page with `{"message":"Hello, World!"}`

That shows the app is working, you can also go to:

http://localhost:5000/add?a=2&b=3

That should show you:

`{"result":5.0}`

You can change the nulbers 2 and 3 at the end of the url to calcualte a different number.

# Containerising

## Build the container image
Now that we have a working app it would be great to put it into a state where we can easily share and deploy it into different environment without haing to struggle. To do that we can use containers. these are small self-contained environments where you can install dependancies in isolation so they will work in any environment either on your development machine or in the cloud without any concern about environments.

A common way to do this is to use a Containerfile (also often called Dockerfile). This file provides instructions on how to build a container, you would usually start from a base container, in this case we start from the slim version of python 3.9:

```bash
FROM python:3.9-slim
```

We could change this version if we have any requirements or security concerns, or need any additional components not included in this image

Next we set a `WORKDIR` this is the home directory that the container will use when running commands. we st it to `/app` with:

```bash
WORKDIR /app
```

next we copy over the requirements file and then run the pip install command to install all the re-requisites our python app needs, pip is already installed as part of the base container so the pip command will work.

```bash
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

next we copy over all the rest of the files from our directory into the container, this works in a very basic app like this but an improvement would be to select specific files to copy over, this would prevent potential security breaches in the future, for example if we created local config files that contain login credentials that we don't want being included in a public image.

```bash
COPY . .
```

next we want to be able to talk to our pod once its up an running, in order to do that we need to `expose` a port, this will allow inbound communications on that port, in this case we are using 5000 but any port would be fine so long as it matches what is used in your code:

```bash
EXPOSE 5000
```

Last thing we need to do is to tell our container what it should do when turned on, we do that with `CMD` in this case we are telling it to use python to run the file app.py:

```bash
CMD["python", "app.py"]
```

Now we can run podman (or docker if using that instead) to build our container image. we will use the build command and pass in the tags we want the container to be built with, this allows us to version our application by having different labels on different versions.

```
podman build -t flask-app -t latest .
```

## Deploy the container image

once that is complete you can check the existing versions you have installed with this command:

```bash
podman images
```

you should see something like this:

```bash
REPOSITORY                                  TAG            IMAGE ID      CREATED             SIZE
localhost/latest                            latest         d4222aaa461e  About a minute ago  171 MB
localhost/flask-app                         latest         d4222aaa461e  About a minute ago  171 MB
```

Now we can deploy this container and check its working, we do that with:

```bash
podman run --name flask-app localhost/flask-app
```

You should see something like:

```bash
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.111:5000
```

Now if you try to go to `http://localhost:5000`... it doesn't work...

This is becuase we haven't specified the port we want to expose when we deployed our podman container. I left that in deliberatly as its something that often trips people over when they first try using docker or podman, the correct way to depoy it is to run this command:

```bash
podman run --name flask-app -p 5000:5000 localhost/flask-app 
```

In this case we are exposing port 5000 on the localhost to port 5000 on the container, if we were deploying a container that had a port of 80 such as nginx or apache then we would use `-p 5000:80` that would then mean when we connect to port 5000 on our browser or call it via api then it would be forwarded to port 80 on the application. The reason we might do that is firstly that anything below port 1000 on most sytems is reserved and cannot be used, the other reason is we might have multiple apps that all listen on the same port. So if we have app 1, app 2 and app 3 all listening on port 80 we could have the first container setup with `-p 5000:80`, the second with `-p 5001:80` and the third on `-p 5002:80` then we can connect on port 5000, 5001 and 5003 and to our containerised apps it would seem we are just connecting on port 80.

## share the container image

Now that we have created our image we could share it to a container registry, this is a place that we can fetch containers from, there are both private registries which can only be accessed by autherised users, this might be something like nexus inside a secure environment, or a cloud based registry like AWS's Elastic Container Registry(ECR)

Github can also host containers so we can publish our container there, to do that we must first login our our github account, to do that we generate a personal access token(classic) by going to your profile in github.com and going to Developer Settings > Personal Access Tokens > Tokens(Classic). From there create a new classic token and give it full acces to `repo`, `workflow`, `write:package` and `delete:package`.

Once you click on save it will show your token on the screen, this will be the only time you see if so if you close or refresh the window it will dissapear, but if this happens you can just delete the token and create a new one.

Once you have copied the token then in the terminal enter this command, replacing `<username>` and `<token>` with your username and token with the one you just generated:

```bash
podman login ghcr.io -u <username> -p <token>
```

If that worked then you should see `Login Succeeded!`

now you are autherised to publish your image, first you want to tag your image with a version, replace the `<username>` with your github username:

```bash
podman tag flask-app:latest ghcr.io/<username>/training-app:latest
podman push ghci.io/<username>/training-app:latest
```

You can test this worked by pulling the image with:

```bash
podman pull ghcr.io/<username>/training-app:latest
```
It might take a few mins for the image to appear so if you don't get it working immediately give it a couple of mins and then try again.

Now we have an image that we can deploy into whatever environments we want and can be accessed from any other source of automation without needing to have our development machines available. We will park this for now and move on to testing

# testing

Rather than manually checking the results in a browser we can automate this with a test file, one has been provided in the `test` directory. it can be run with:

```bash
python test/test_app.py
```

If it works you should see something like this:


```bash
===================================================================================== test session starts =====================================================================================
platform linux -- Python 3.13.3, pytest-8.3.5, pluggy-1.6.0 -- /home/acleveland/repo/training-app/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/acleveland/repo/training-app
collected 2 items

tests/test_app.py::test_hello_world PASSED                                                                                                                                              [ 50%]
tests/test_app.py::test_add PASSED                                                                                                                                                      [100%]

====================================================================================== 2 passed in 0.01s ======================================================================================
```

Which is very cool, saves some time over manually checking. However we can still make this easier by adding these checks into a pipeline, this way every time we make a change and commit it to git we get this check running automatically. To do that we need to create a **github action**

# Pipelines

Github actions can be used in any repo kept in github, there are also similar pipelines that can be run in other git repositories such as gitlab and tools such as Jenkins or ArgoCD are independant of a specific git repo provider.

when using github actions the files need to be created using a set convention, all files live in a directory called `.github` 
>**note** In linux and unix land having a `.` at the begining of a filename makes it a hidden file or directory, so if you are not seeing this directory you may need to turn on `show hidden files` or if using the cli using `ls -a` to show all files which will include hidden files.

Under that directory there will be several other directories, the one we want is `workflows` these are the pipelines that we will be using, other directories here can provide additional features but for now we only care about workflows.

## name

There is a basic pipeline already in place, the top of the file has the name, this is the name that will appear in the workflows tab of github and is used to identifiy pipelines.

## trigger

Next we have the `on` section. This is how we specify what causes this pipeline to run, we have it set to run on push to any branch that matches the naming pattern of `**` which is all branches. This will often have more finegrained controls but for this example its fine to leave it like this, but things you can set it to are on the creation or close of a pull request, manual activation for things like creating or deleting resources and at specific time intervals, such as running long tests over night.

## jobs

Each workflow will have at least one job, there might be multiple jobs on more complex workflows, each job has its own sequence of steps that it will follow in order to complete the pipeline.

## steps

Each step will be a single action, this might be to run some code or it might be to call an `action` which are modular blocks that can do all sorts of things like deploy infrastructure via terraform, run a testing suite or scan for code vulnrabilities. Actions can either be called from a central repo for common tasks, or custom actions can be defined in the `.github/actions` directory which exists alongside the `.github/workflow` directory.

with the current pipeline it will create the image and push it into the github registry everytime we commit code, this is helpful but we can improve the reliability of our application by adding some automated testing, we have already created a test file so lets add that into the existing pipeline so it will run the testing for us each time we commit our code.

To do that we can add this block in a new step below the `Wait for Flask to be ready` so add a new line after line 41 and insert the following:

```yaml
- name: Run API tests
    run: pytest tests/test_app.py -v
```

Ensure that the indentation is inline with the rest of the code, yaml is very sensitive to indents as that is how it seperates out blocks, think of indents in yaml like Brackets in json.

Now we can save this and push the changes into git. This can be done either via the GUI in VSCode or the IDE of your choice or you can do it via the command line, I have this handy little one liner that I use to add, commit and push all in one command, replace `<initials>` with your actual initials, for me its `AC`. In bash the `&&` means if this command is successful then move onto the next one, so if any step fails it will end the chain of commands:

```bash
git add -A && git commit -m "<initals> - added new step to run automated tests" && git push
```

Now if you go to your github page you should see that you have a yellow light next to your latest commit message at the top of the files list, or it might show a green tick ✅ or a red cross ❌ depending on the result of the pipeline. click on it for extra details.

If the pipeline is still in progress you will be able to see which stage it is currently on and what the status is of the previous steps. If any step fails the entire pipeline will be considered a failure.

with that done you have enhanced your first pipeline!

If you want to continue exploring you can look at adding additional pipelines that trigger on specific trigger, like when a pull request is raised, or a pipeline to deploy into github registry when a pull request into main is closed. There are plenty of enchancements available.

