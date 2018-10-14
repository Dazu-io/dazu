FROM flaviostutz/datascience-tools

ADD /notebooks /notebooks

RUN pip install requests
