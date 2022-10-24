install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install	
	@poetry shell

## mypy: mypy is a static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing. Path: Makefile
## pre-commit: pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. Path: Makefile
## 		Check pre-commit yaml file for more details
## 		https://pre-commit.com/
## 		It invokes the following hooks:
## 		- Requirements.txt checker
## 		- Line endings normalizer
## 		- Tab character checker
## 		- Black code formatter
## 		- isort code formatter
## black: Black is the uncompromising Python code formatter. Path: Makefile
## flake8: Flake8 is a wrapper around these tools: PyFlakes, pycodestyle, Ned Batchelder’s McCabe script. Path: Makefile
## pylint: Pylint is a Python static code analysis tool which looks for programming errors, helps enforcing a coding standard, sniffs for code smells and offers simple refactoring suggestions. Path: Makefile
## isort: isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections and by type. Path: Makefile
check: ## Lint code using pre-commit and run mypy and deptry.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry lock --check

	@echo "🚀 Linting code: Running pre-commit"
	@pre-commit run -a

	@echo "🚀 Checking code formatting: Running mypy"
	@mypy ./src

## pytest: pytest is a mature full-featured Python testing tool that helps you write better programs. Path: Makefile
## 		--doctest-modules: run doctests in all .py modules
## 		--cov: measure coverage for Python modules
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@pytest tests/ 

testcov: ## Test the code with pytest and measure coverage
	@echo "🚀 Testing code: Running pytest with coverage"
	@pytest --cov=src tests/ 

testcovrep: ## Test the code with pytest and measure coverage and generate report
	@echo "🚀 Testing code: Running pytest with coverage and report"
	@pytest --cov-report html:cov_html --cov-report xml:cov_xml--cov=src tests/


add: ## Add new files to track on git
	@git add .

commit: ## Commit changes to git
	@git commit -m "$(m)"

## pull request: Create a pull request on github
## 		-- title: Title of the pull request
## 		-- body: Body of the pull request
## 		-- head: Branch to merge into the base branch
pr: ## Create a pull request
	@git push origin $(b)
	@gh pr create --title "$(m)" --body "$(m)" --base $(b) --head $(b)

push: ## Push changes to git
	@git push

switch: ## Switch to a new branch
	@git checkout -b $(b)

pull: ## Pull changes from git
	@git pull

fetch : ## Fetch changes from git
	@git fetch

merge: ## Merge changes from git
	@git merge $(b)

clean: ## Clean the project
	@echo "🚀 Cleaning project: Removing .pytest_cache, .mypy_cache, .coverage, .cache, .mypy_cache, .DS_Store, __pycache__"
	@rm -rf .pytest_cache .mypy_cache .coverage .cache .mypy_cache .DS_Store __pycache__

## install: Install the poetry environment
## check: Lint code using pre-commit and run mypy
## test: Test the code with pytest
## add: Add new files to track on git
## commit: Commit changes to git
## push: Push changes to git
## switch: Switch to a new branch
## pull: Pull changes from git
## fetch: Fetch changes from git
## merge: Merge changes from git
## clean: Clean the project
.PHONY: help install check test add commit push switch pull fetch merge clean
