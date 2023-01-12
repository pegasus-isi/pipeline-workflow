# Pipeline Workflow 

# Dependencies
- Pegasus v5.0+
- Python 3.6+

![Pipeline](https://user-images.githubusercontent.com/36110304/210929365-0e2f20e1-48dc-48de-a0fd-a2873d1d9b0c.png)

# File Description

<b>plan.sh:</b> Consists of all commands to be executed to run the workflow. Takes care of planning the pegasus workflow and initialising where the input files are and where output files should be located after execution of workflow. 

<b>workflow_generator.py:</b> Creates the abstract workflow, the replica catalog, the transformation catalog, and the site catalog. 

# How to run the workflow?
```
# Plan and run the workflow generator to create an abstract workflow for the given input files
./workflow_generator.py 
./plan.sh workflow.yaml
```
