#!/usr/bin/env bash
set -ex

if [[ -z $KUBECONTEXT ]]; then
  export KUBECONTEXT=admin@fellow
fi

if [[ -z $IMAGE ]]; then
  echo "\$IMAGE not set, please set it to a git sha with a build container and try again."
  exit 1;
fi

export REVISION=$IMAGE

# gem install kubernetes-deploy to get this tool
kubernetes-deploy \
  --template-dir ./deploy/production \
  --bindings=container_registry=326253947186.dkr.ecr.us-west-2.amazonaws.com \
  polr-production $KUBECONTEXT
