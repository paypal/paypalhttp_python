configatron.product_name = "BraintreeHttp Python"

def clean
  CommandProcessor.command("rm -rf dist")
end

def test
  tag = Time.now.to_i
  _test_with_dockerfile("DockerfilePython2", tag)
  _test_with_dockerfile("DockerfilePython3", tag + 1)
end

def _test_with_dockerfile(dockerfile, tag)
  CommandProcessor.command("docker build -f #{dockerfile} -t #{tag}"
  CommandProcessor.command("docker run #{tag}")
end

def validate_version_match
	if package_version != @current_release.version
		Printer.fail("package version #{package_version} does not match changelog version #{@current_release.version}.")
		abort()
	end

	Printer.success("package version #{package_version} matches latest changelog version #{@current_release.version}.")
end

def package_version
  File.open("setup.py", 'r') do |f|
		f.each_line do |line|
			if line.match (/^version = "\d+.\d+.\d+"$/)
				return line.strip.split('"')[1]
			end
		end
	end
end

def build_method
  clean
  CommandProcessor.command("python setup.py sdist bdist_wheel --universal")
end

def publish_to_package_manager(version)
  # CommandProcessor.command("twine upload dist/*")
  abort("please implement publish_to_package_manager method")
end

def wait_for_package_manager(version)
end

# True if publishing the root repo to GitHub.  Required.
configatron.release_to_github = true

configatron.custom_validation_methods = [
	method(:validate_version_match),
  method(:test),
]

configatron.build_method = method(:build_method)

# The method that publishes the project to the package manager.  Required.
configatron.publish_to_package_manager_method = method(:publish_to_package_manager)

# The method that waits for the package manager to be done.  Required.
configatron.wait_for_package_manager_method = method(:wait_for_package_manager)
