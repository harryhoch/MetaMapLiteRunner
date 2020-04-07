#!/usr/bin/env bash

METAMAP_RUNNER_SCRIPT=/IdeaProjects/MetaMapLiteRunner/MetaMapLiteServerRunner.py
METAMAP_PROJECTDIR=/IdeaProjects/public_mm_lite

OPENNLP_MODELS=$METAMAP_PROJECTDIR/data
CONFIGDIR=$METAMAP_PROJECTDIR/config
METAMAP_SERVER_SCRIPT=$METAMAP_PROJECTDIR/metamapliteserver.sh
PROJECTDIR=$(dirname $0)


mkdir -p ./mml/data
cp -a $OPENNLP_MODELS/* ./mml/data/
mkdir -p ./mml/data/models/config
cp -a $CONFIGDIR/*  ./mml/data/models/config/
mkdir -p ./mml/target
cp -a   $METAMAP_PROJECTDIR/target/* ./mml/target/
cp -a $METAMAP_RUNNER_SCRIPT ./mml/
cp -a $METAMAP_SERVER_SCRIPT ./mml/

tar cvzf mml.tgz ./mml

rm -rf ./mml