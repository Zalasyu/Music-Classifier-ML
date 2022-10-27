install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install	
	@poetry shell


## pytest: pytest is a mature full-featured Python testing tool that helps you write better programs. Path: Makefile
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@pytest tests/ 

## testcov uses pytest-cov to generate a coverage report.
testcov: ## Test the code with pytest and measure coverage
	@echo "🚀 Testing code: Running pytest with coverage"
	@pytest --cov=src tests/ 

testcovrep: ## Test the code with pytest and measure coverage and generate report
	@echo "🚀 Testing code: Running pytest with coverage and report"
	@pytest --cov-report html:cov_html --cov-report xml:cov_xml--cov=src tests/

## Usage: make add
add: ## Add new files to track on git
	@git add .

## Usage: make commit me="Commit message"
commit: ## Commit changes to git
	@git commit -m "$(m)"


## pull request: Create a pull request on github
## 		-- title: Title of the pull request
## 		-- body: Body of the pull request
## 		-- head: Branch to merge into the base branch

## Usage: make pr title="Title of the pull request" body="Body of the pull request" head="Branch to merge into the base branch"
pr: ## Create a pull request
	@git push origin $(b)
	@gh pr create --title "$(m)" --body "$(m)" --base $(b) --head $(b)

## Usage: make push
push: ## Push changes to git
	@git push

## Usage: make checkout b="Branch to checkout"
checkout: ## Checkout a branch
	@git checkout $(b)

## Usage: make switch b="Branch to switch to"
switch: ## Switch to a new branch
	@git checkout -b $(b)

## Usage: make list
list: ## List all branches
	@git branch -a

## Usage: make pull
pull: ## Pull changes from git
	@git pull

# Usage: make fetch
fetch : ## Fetch changes from git
	@git fetch

## Usage: make merge b="Branch to merge"
merge: ## Merge changes from git
	@git merge $(b)

## Usage: make delete b="Branch to delete"
delete: ## Delete a branch
	@git branch -d $(b)


## Usage: make clean
clean: ## Clean the project
	@echo "🚀 Cleaning project: Removing .pytest_cache, .mypy_cache, .coverage, .cache, .mypy_cache, .DS_Store, __pycache__"
	@rm -rf .pytest_cache .mypy_cache .coverage .cache .mypy_cache .DS_Store __pycache__

## install: Install the poetry environment
## check: Lint code using pre-commit and run mypy
## test: Test the code with pytest
## add: Add new files to track on git
## commit: Commit changes to git
## push: Push changes to git
## pr: Create a pull request
## switch: Switch to a new branch
## pull: Pull changes from git
## fetch: Fetch changes from git
## merge: Merge changes from git
## clean: Clean the project

.PHONY: install check test add commit push switch pull fetch merge delete clean pr 