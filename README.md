# CI/CD


This project does NOT contain any deployable code. The dummy dockerfile is just attached to avoid confusing failures when the CI runs. 

This Repo is already called for in multiple repos, and changing code here on the master branch could affect numerous repos. It is a primary placement of DevOps-related tools and should be utilized as a centralized place for keeping a well-maintained and organized toolset.


## Current Tools:

Each of these Tools lives in the `/tasks/` directory.
- Gitlab Container Scanning
- Manual Security Code Auditing:
    * Bandit
    * Trivy
    * Vulture
- NPM Auditing
    * `NPM AUDIT PLUS` 
- Terraform Scanning:
     * terrascan
     * tfsec
     * checkov

## Utilizing the CI-CD Repo and Understanding its parts:


To call for and run a "job" created in a remote repo, one needs to do specifically three things:

include the source 
specify the stage *Note, this needs to match the stage name listed in the source `include` and specify the job. From this, you can utilize a specified REPO, in our case, the CI-CD Repo

<u>What makes this complicated:</u>


you need to specify every stage from the include to the child's job, or the pipeline <u>WILL FAIL</u>

Solution:
 One must create separate tasks.

In my case, I have placed these in the dir `/tasks/`

When creating and calling for these "tasks" or "isolated jobs," which follow the same format as a typical .gitlab-ci.yml but can be named whatever, as long as it is a YAML/yml


in my case for the Jira ticket watcher, I set this code on the primary gitlab-ci.yml :

### Add Jira Ticket watcher with include
```
include:
	- project: "URL HERE"
    file: "/tasks/jira-ticket-watcher/.jira-watch.yml"
    ref: master
```

### Specify the stage
```
stages:
  - verify-jira-ticket
```

### Specify the job:
```
check_jira_ticket:
  when: manual # youneed atleast one argument in the job for some reason.
```

Set code in /tasks/jira-ticket-watcher/.jira-watch.yml :

## Verify if Jira Ticket Matches the Name of the Merge Request
```
check_jira_ticket:
  image: python:3.11-alpine
  stage: verify-jira-ticket
  when: manual
  before_script:
    - <Before Script HERE>
  script:
    - export JIRA_TICKET="$(echo $CI_MERGE_REQUEST_TITLE | cut -d ":" -f1 | tr -d " \t" )"
    - echo "$JIRA_TICKET"
    - python3 ./validate_jira.py "$JIRA_TICKET"
  allow_failure: true
  rules:
    - if: $CI_PIPELINE_SOURCE == 'merge_request_event' && $CI_MERGE_REQUEST_SOURCE_BRANCH_NAME != /^(bugfix|devops)(\/).*$/
    - if: $CI_MERGE_REQUEST_SOURCE_BRANCH_NAME =~ /^(bugfix|devops)(\/).*$/
      when: never
      allow_failure: true
    - if: $CI_COMMIT_TAG != "null"
      when: never
    - if: $CI_PIPELINE_SOURCE == "schedule"
      when: never

```
* All this is already specified in the job, see the repo for code

## Utilizing the CI-CD Repo In Remote Repos:

How we can call for these in various places:

You will need to adjust the Repo Security Settings to allow the CI-CD Repo to communicate to the remote Repo

```
include:
  # Add Jira Ticket watcher
  - project: "URL HERE"
    file: "/tasks/jira-ticket-watcher/.jira-watch.yml"
    ref: master

# Specify the stage
stages:
  - verify-jira-ticket

## Verify if Jira Ticket Matches the Name of the Merge Request
check_jira_ticket:
  stage: verify-jira-ticket
  when: always
  allow_failure: false
  tags:
    - <tags-here>
```



* note I change the when  to always , and the `allow_failure` to false  in the remote repo. This will overwrite the initial set of variables in this repo.
