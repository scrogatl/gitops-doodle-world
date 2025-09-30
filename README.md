# GitOps Microservice Example

## This is the world for doodle

Must add annotation to have New Relic scrape prometheus metrics like so

``` POD=`k get pods -n supreme-doodle | grep -i world | grep -v  ruby | grep Running | awk '{print $1}' `; k annotate pods $POD -n supreme-doodle   newrelic.io/scrape="true" ```
