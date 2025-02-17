from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class WecommitPresskitagent():
	"""WecommitPresskitagent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff
	def before_kickoff_function(self, inputs):
		print(f"Before kickoff function with inputs: {inputs}")
		return inputs # You can return the inputs or modify them as needed

	@after_kickoff
	def after_kickoff_function(self, result):
		print(f"After kickoff function with result: {result}")
		return result # You can return the result or modify it as needed

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def presskit_content_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['presskit_content_generator'],
			verbose=True
		)

	@agent
	def presskit_quality_review_optimization_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['presskit_quality_review_optimization_agent'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def generate_intial_presskit_draft(self) -> Task:
		return Task(
			config=self.tasks_config['generate_intial_presskit_draft'],
		)

	@task
	def review_optimize_presskit_draft(self) -> Task:
		return Task(
			config=self.tasks_config['review_optimize_presskit_draft'],
			context = [self.generate_intial_presskit_draft()],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the WecommitPresskitagent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
