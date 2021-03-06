#!/usr/bin/env python3
import os
import logging
from pathlib import Path
from argparse import ArgumentParser

logging.basicConfig(level=logging.DEBUG)

# --- Import Pegasus API ------------------------------------------------------
from Pegasus.api import *


class PipelineWorkflow:
    wf = None
    sc = None
    tc = None
    props = None

    dagfile = None
    wf_name = None
    wf_dir = None

    # --- Init ----------------------------------------------------------------
    def __init__(self, dagfile="workflow.yml"):
        self.dagfile = dagfile
        self.wf_name = "pipeline"
        self.wf_dir = str(Path(__file__).parent.resolve())

    # --- Write files in directory --------------------------------------------
    def write(self):
        if not self.sc is None:
            self.sc.write()
        self.props.write()
        self.tc.write()
        self.wf.write()

    # --- Configuration (Pegasus Properties) ----------------------------------
    def create_pegasus_properties(self):
        self.props = Properties()

        # props["pegasus.monitord.encoding"] = "json"
        # self.properties["pegasus.integrity.checking"] = "none"
        return

    # --- Site Catalog --------------------------------------------------------
    def create_sites_catalog(self, exec_site_name="condorpool"):
        self.sc = SiteCatalog()

        shared_scratch_dir = os.path.join(self.wf_dir, "scratch")
        local_storage_dir = os.path.join(self.wf_dir, "output")

        local = Site("local").add_directories(
            Directory(Directory.SHARED_SCRATCH, shared_scratch_dir).add_file_servers(
                FileServer("file://" + shared_scratch_dir, Operation.ALL)
            ),
            Directory(Directory.LOCAL_STORAGE, local_storage_dir).add_file_servers(
                FileServer("file://" + local_storage_dir, Operation.ALL)
            ),
        )

        exec_site = (
            Site(exec_site_name)
            .add_pegasus_profile(style="condor")
            .add_condor_profile(universe="vanilla")
            .add_profiles(Namespace.PEGASUS, key="data.configuration", value="condorio")
        )

        self.sc.add_sites(local, exec_site)

    # --- Transformation Catalog (Executables and Containers) -----------------
    def create_transformation_catalog(self, exec_site_name="condorpool"):
        self.tc = TransformationCatalog()

        curl = Transformation(
            "curl", site=exec_site_name, pfn="/usr/bin/curl", is_stageable=False
        )
        wc = Transformation(
            "wc", site=exec_site_name, pfn="/usr/bin/wc", is_stageable=False,
        )

        self.tc.add_transformations(curl, wc)

    # --- Create Workflow -----------------------------------------------------
    def create_workflow(self):
        self.wf = Workflow(self.wf_name, infer_dependencies=True)

        webpage = File("pegasus.html")

        curl_job = (
            Job("curl")
            .add_args("-o", webpage, "http://pegasus.isi.edu")
            .add_outputs(webpage, stage_out=False, register_replica=False)
        )

        count = File("count.txt")

        wc_job = (
            Job("wc")
            .add_args("-l", webpage)
            .add_inputs(webpage)
            .set_stdout(count, stage_out=True, register_replica=True)
        )

        self.wf.add_jobs(curl_job, wc_job)


if __name__ == "__main__":
    parser = ArgumentParser(description="Pegasus Pipeline Workflow")

    parser.add_argument(
        "-s",
        "--skip_sites_catalog",
        action="store_true",
        help="Skip site catalog creation",
    )
    parser.add_argument(
        "-e",
        "--execution_site_name",
        metavar="STR",
        type=str,
        default="condorpool",
        help="Execution site name (default: condorpool)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="STR",
        type=str,
        default="workflow.yml",
        help="Output file (default: workflow.yml)",
    )

    args = parser.parse_args()

    workflow = PipelineWorkflow(args.output)

    if not args.skip_sites_catalog:
        print("Creating execution sites...")
        workflow.create_sites_catalog(args.execution_site_name)

    print("Creating workflow properties...")
    workflow.create_pegasus_properties()
    
    print("Creating transformation catalog...")
    workflow.create_transformation_catalog(args.execution_site_name)

    print("Creating pipeline workflow dag...")
    workflow.create_workflow()

    workflow.write()
