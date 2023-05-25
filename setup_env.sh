#!/bin/bash

while IFS= read -r line
do
  export "$line"
done < .env
