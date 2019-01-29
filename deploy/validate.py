import tempfile
import structlog
import subprocess
import glob
import os
import sys

logger = structlog.get_logger(__name__)
deploy_dir = os.path.dirname(os.path.realpath(__file__))


for environment in ('production',):
    tmpdir = tempfile.mkdtemp()

    deploy_dir_glob = os.path.join(deploy_dir, environment, '*.*')
    logger.info("Scanning environment", glob=deploy_dir_glob)

    for absolute_template in glob.glob(deploy_dir_glob):
        template = os.path.basename(absolute_template)
        tmppath = os.path.join(tmpdir, template)

        logger.info("Rendering template", environment=environment, template=template)
        with open(tmppath, 'w') as f:
            try:
                f.write(
                    subprocess.check_output(
                        [
                            "kubernetes-render",
                            "--template-dir",
                            os.path.join(deploy_dir, environment),
                            "--bindings=container_registry=test-registry.docker.io",
                            template,  # template name
                        ],
                        stderr=sys.stderr,
                    ).decode("utf-8")
                )
            except subprocess.CalledProcessError as e:
                logger.exception(e.output.decode("utf-8"))
                raise

        logger.info("Validating template", environment=environment, template=template)
        subprocess.check_call(["kubeval", "--kubernetes-version", "1.11.1", "--strict", tmppath])
