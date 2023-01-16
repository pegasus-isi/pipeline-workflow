# Pipeline Workflow 

# Dependencies
- Pegasus v5.0+
- Python 3.6+

![pipeline-workflow](https://user-images.githubusercontent.com/36110304/212753866-b3fbb2b2-30ba-4c25-bf8c-816fadaadc8f.png)

# File Description

<b>plan.sh:</b> Consists of all commands to be executed to run the workflow. Takes care of planning the pegasus workflow and initialising where the input files are and where output files should be located after execution of workflow. 

<b>workflow_generator.py:</b> Creates the abstract workflow, the replica catalog, the transformation catalog, and the site catalog. 

# How to run the workflow?
```
# Plan and run the workflow generator to create an abstract workflow for the given input files
./workflow_generator.py 
./plan.sh workflow.yaml
```
