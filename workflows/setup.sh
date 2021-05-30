#!/bin/bash

prefect backend cloud

if [ -e ~/.prefect/config.toml ]; then
    
    prefect create project "ml-workflows"
    