configatron.product_name = "BraintreeHttp Python"

# Custom validations
def test
  tag = Time.now.to_i
  _test_with_dockerfile("DockerfilePython2", tag)
  _test_with_dockerfile("DockerfilePython3", tag + 1)
end

def _test_with_dockerfile(dockerfile, tag)
  CommandProcessor.command("docker build -f #{dockerfile} -t #{tag} .")
  CommandProcessor.command("docker run #{tag}", live_output=true)
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

def validate_version_match
	if package_version != @current_release.version
		Printer.fail("package version #{package_version} does not match changelog version #{@current_release.version}.")
		abort()
	end

	Printer.success("package version #{package_version} matches latest changelog version #{@current_release.version}.")
end

def validate_present(tool, install_command)
  tool_path = `which #{tool}`
  if tool_path.rstrip == ""
    Printer.fail("#{tool} not installed - please run `#{install_command}`")
    abort()
  else
    Printer.success("#{tool} found at #{tool_path}")
  end
end

def validate_virtualenv
  validate_present("virtualenv", "pip install virtualenv")
end

def validate_twine
  validate_present("twine", "pip install twine")
end

configatron.custom_validation_methods = [
	method(:validate_version_match),
  method(:validate_virtualenv),
  method(:validate_twine),
  method(:test),
]

# Build, update version, and publish to PyPi
def clean
  CommandProcessor.command("rm -rf dist")
end

def build_method
  begin
    clean
    command = <<~END
virtualenv venv; \
. ./venv/bin/activate; \
pip install -r requirements.txt; \
python setup.py sdist bdist_wheel --universal
    END
    CommandProcessor.command(command, live_output=true)
  ensure
    CommandProcessor.command("rm -rf venv || true")
  end
end

configatron.build_method = method(:build_method)

def update_version_method(version)
  contents = File.read("setup.py")
  contents = contents.gsub(/^version = "\d+.\d+.\d+"$/, "version = \"#{version}\"")
  File.open("setup.py", "w") do |f|
    f << contents
  end
end

configatron.update_version_method = method(:update_version_method)

def publish_to_package_manager(version)
  CommandProcessor.command("twine upload dist/*", live_output=true)
end

configatron.publish_to_package_manager_method = method(:publish_to_package_manager)

def version_released?(version)
  released_versions = `curl -s https://pypi.python.org/pypi/braintreehttp/json`
  released_versions = JSON.parse(released_versions)

  return released_versions["releases"].include? version
end

def wait_for_package_manager(version)
  seconds = 30
  while !version_released?(version)
    puts "Version #{version} not released. Waiting #{seconds} seconds"
    seconds.times do
      print '.'
      sleep 1
    end
  end
  "Version #{version} on PyPi!"
end

configatron.wait_for_package_manager_method = method(:wait_for_package_manager)

# Miscellania
configatron.release_to_github = true
configatron.prerelease_checklist_items []
